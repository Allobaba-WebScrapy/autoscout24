from flask import Flask, jsonify, request
from flask_cors import CORS
from AutoScout24 import AutoScout24
import json
import time
import os

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
        return jsonify(success=False, error='Scraper failed to start: {}'.format(str(e))), 500

    # Consume stream: collect article items and final result_info
    collected = []
    result_info = None
    stream_error = None

    for chunk in generator:
        try:
            obj = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        t = obj.get('type')
        if t == 'progress':
            # optional: could log or stream progress; for now we just collect data
            continue
        if t == 'result_info':
            result_info = obj.get('data') or {}
            continue
        if obj.get('error'):
            stream_error = obj.get('error')
            break
        # Article payload: {"url": "...", "data": {...}}
        if 'url' in obj and 'data' in obj:
            collected.append(obj)

    # Build single JSON response
    count = len(collected)
    meta = {
        'num_of_pages': result_info.get('num_of_pages') if result_info else None,
        'num_of_offers': result_info.get('num_of_offers') if result_info else None,
        'start_from_page': result_info.get('start_from_page') if result_info else start_page,
        'end_in_page': result_info.get('end_in_page') if result_info else None,
        'offers_requested': offers_number,
        'offers_collected': count,
        'errors': (result_info.get('errors_list') or []) if result_info else [],
    }
    if stream_error:
        meta['errors'] = meta.get('errors') or []
        meta['errors'].insert(0, stream_error)

    success = stream_error is None and (count > 0 or (result_info and result_info.get('num_of_offers', 0) == 0))
    return jsonify(
        success=success,
        count=count,
        data=collected,
        meta=meta,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port)
