from flask import Flask, jsonify, request, Response, stream_with_context
from flask_cors import CORS
from AutoScout24 import AutoScout24
from fallback_data import get_fallback_offers
import json
import random
import threading
import time
import os

# If no products collected after this many seconds, return fallback data
SCRAPE_TIMEOUT_SEC = 10
# When returning fallback, wait this many seconds between each item (simulates processing)
FALLBACK_DELAY_PER_ITEM_SEC = 2

app = Flask(__name__)
CORS(app)

# Set AUTOSCOUT24_DEBUG_LOG to a file path to enable request debug logging
_DEBUG_LOG = os.environ.get("AUTOSCOUT24_DEBUG_LOG", "")


def _dbg(loc, msg, data, hid, run_id="run1"):
    if not _DEBUG_LOG:
        return
    try:
        os.makedirs(os.path.dirname(_DEBUG_LOG), exist_ok=True)
        with open(_DEBUG_LOG, "a") as f:
            f.write(
                json.dumps(
                    {
                        "location": loc,
                        "message": msg,
                        "data": data,
                        "timestamp": int(time.time() * 1000),
                        "hypothesisId": hid,
                        "runId": run_id,
                    }
                )
                + "\n"
            )
    except Exception:
        pass


def _stream_ndjson(lines_gen):
    """Stream NDJSON: one JSON object per line. Each item from lines_gen is yielded as a line."""
    for obj in lines_gen:
        yield json.dumps(obj, ensure_ascii=False) + "\n"


def _fallback_stream_gen(offers_number, message, errors, meta_extra=None):
    """Generator: yield one product per line with 2s delay between each (for fallback)."""
    pool = get_fallback_offers()
    n = min(offers_number, len(pool))
    chosen = random.sample(pool, n)
    meta = dict(meta_extra) if meta_extra else {}
    meta['offers_requested'] = offers_number
    meta['offers_collected'] = len(chosen)
    meta['errors'] = list(errors) if errors else meta.get('errors') or []
    yield {"type": "fallback_start", "message": message, "success": True, "fallback": True, "count": len(chosen), "meta": meta}
    for i, item in enumerate(chosen):
        yield {"type": "result", "data": item}
        if i < len(chosen) - 1:
            time.sleep(FALLBACK_DELAY_PER_ITEM_SEC)
    yield {"type": "result_info", "data": meta}


def _build_fallback_response(offers_number, message, errors, meta_extra=None):
    """Return streaming response with random fallback offers, 2 seconds between each product."""
    return Response(
        stream_with_context(_stream_ndjson(_fallback_stream_gen(offers_number, message, errors, meta_extra))),
        mimetype="application/x-ndjson",
        headers={"X-Content-Type-Options": "nosniff"},
    )


def _stream_results_gen(collected, result_info, meta, success):
    """Generator: yield each product then 2s delay, then result_info (for real scrape)."""
    for i, item in enumerate(collected):
        yield {"type": "result", "data": item}
        if i < len(collected) - 1:
            time.sleep(FALLBACK_DELAY_PER_ITEM_SEC)
    yield {"type": "result_info", "data": {**meta, "success": success, "offers_collected": len(collected)}}


def _parse_positive_int(value, default=None, min_val=1, max_val=1000):
    """Parse value as positive integer in [min_val, max_val]. Returns default if invalid."""
    if value is None:
        return default
    try:
        n = int(value)
        if n < min_val or n > max_val:
            return default
        return n
    except (TypeError, ValueError):
        return default


@app.route("/")
def hello():
    return jsonify(
        service="autoscout24-data-collector",
        status="ok",
        docs="POST /scrape with JSON: url (required), number (required), startPage?, waitingTime?, businessType?",
    )


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json(silent=True)
    _dbg('app.py:scrape', 'after get_json', {'data_is_none': data is None, 'content_type': request.content_type}, 'A')

    if data is None:
        return jsonify(success=False, error='Invalid or missing JSON body. Send JSON with "url" and "number".'), 400

    url = data.get('url')
    if not url or not str(url).strip():
        return jsonify(success=False, error='Missing required field "url".'), 400

    # number of offers to collect (required)
    number = data.get('number') if data.get('number') is not None else data.get('offersNumber')
    if number is None:
        return jsonify(success=False, error='Missing required field "number".'), 400
    offers_number = _parse_positive_int(number, default=None, min_val=1, max_val=500)
    if offers_number is None:
        return jsonify(success=False, error='"number" must be an integer between 1 and 500.'), 400

    start_page = _parse_positive_int(data.get('startPage'), default=1, min_val=1, max_val=9999) or 1
    waiting_time = _parse_positive_int(data.get('waitingTime'), default=30, min_val=5, max_val=120) or 30
    business_type = data.get('businessType') in ('b2b', 'b2c') and data.get('businessType') or 'b2b'

    _dbg('app.py:scrape', 'params extracted', {
        'url': url, 'offers_number': offers_number, 'start_page': start_page,
        'waiting_time': waiting_time, 'business_type': business_type
    }, 'B')

    try:
        generator = AutoScout24(
            url, offers=offers_number, startFromPage=start_page,
            waitingTime=waiting_time, businessType=business_type
        ).format_articles_data()
    except Exception as e:
        _dbg('app.py:scrape', 'AutoScout24 init failed', {'error': str(e)}, 'D')
        return _build_fallback_response(
            offers_number,
            'Scraper unavailable (e.g. Chrome not running). Showing sample data so you can see the expected format.',
            ['Scraper failed to start: {}'.format(str(e))],
        )

    # Consume stream with 10s timeout: if no products after 10s, return fallback
    collected = []
    result_holder = {}
    stream_error_holder = [None]
    stream_exception = []

    def consume_generator():
        try:
            for chunk in generator:
                try:
                    obj = json.loads(chunk)
                except json.JSONDecodeError:
                    continue
                t = obj.get('type')
                if t == 'progress':
                    continue
                if t == 'result_info':
                    result_holder['info'] = obj.get('data') or {}
                    continue
                if obj.get('error'):
                    stream_error_holder[0] = obj.get('error')
                    break
                if 'url' in obj and 'data' in obj:
                    collected.append(obj)
        except Exception as e:
            stream_exception.append(str(e))

    thread = threading.Thread(target=consume_generator, daemon=True)
    thread.start()
    thread.join(timeout=SCRAPE_TIMEOUT_SEC)
    if len(collected) == 0:
        errors = list(stream_exception) if stream_exception else ['No products within {} seconds.'.format(SCRAPE_TIMEOUT_SEC)]
        _dbg('app.py:scrape', 'timeout or no data', {'errors': errors}, 'D')
        return _build_fallback_response(
            offers_number,
            'Scraper produced no results in time ({}s). Showing sample data so you can see the expected format.'.format(SCRAPE_TIMEOUT_SEC),
            errors,
        )
    # Wait for thread to finish so we get full result
    thread.join(timeout=300)

    # Build single JSON response
    result_info = result_holder.get('info') or {}
    stream_error = stream_error_holder[0]
    count = len(collected)
    meta = {
        'num_of_pages': result_info.get('num_of_pages'),
        'num_of_offers': result_info.get('num_of_offers'),
        'start_from_page': result_info.get('start_from_page') or start_page,
        'end_in_page': result_info.get('end_in_page'),
        'offers_requested': offers_number,
        'offers_collected': count,
        'errors': result_info.get('errors_list') or [],
    }
    if stream_error:
        meta['errors'] = meta.get('errors') or []
        meta['errors'].insert(0, stream_error)

    success = stream_error is None and (count > 0 or (result_info and result_info.get('num_of_offers', 0) == 0))
    if not success and count == 0:
        errs = meta.get('errors') or []
        return _build_fallback_response(
            offers_number,
            'No offers could be collected (e.g. blocked or no results). Showing sample data so you can see the expected format.',
            errs,
            meta_extra=meta,
        )
    return Response(
        stream_with_context(_stream_ndjson(_stream_results_gen(collected, result_info, meta, success))),
        mimetype="application/x-ndjson",
        headers={"X-Content-Type-Options": "nosniff"},
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
