#!/usr/bin/env python3
"""
AutoScout24 data collector CLI.
Run directly (Selenium + Chrome/Chromium required) or use the Flask API instead.

Usage:
  python collect.py "https://www.autoscout24.com/lst?..." --number 20 --out offers.json
  python collect.py "https://www.autoscout24.com/lst?..." --number 10 --start-page 1 --business-type b2b
"""
import argparse
import json
import sys

from AutoScout24 import AutoScout24


def main():
    parser = argparse.ArgumentParser(
        description="Collect vehicle offers from an AutoScout24 listing URL."
    )
    parser.add_argument("url", help="AutoScout24 listing URL (e.g. /lst?...)")
    parser.add_argument(
        "--number",
        "-n",
        type=int,
        default=20,
        metavar="N",
        help="Max number of offers to collect (default: 20, max: 500)",
    )
    parser.add_argument(
        "--start-page",
        type=int,
        default=1,
        help="Page number to start from (default: 1)",
    )
    parser.add_argument(
        "--waiting-time",
        type=int,
        default=30,
        help="Selenium implicit wait in seconds (default: 30)",
    )
    parser.add_argument(
        "--business-type",
        choices=("b2b", "b2c"),
        default="b2b",
        help="Filter by business type from phone prefix (default: b2b)",
    )
    parser.add_argument(
        "--out",
        "-o",
        metavar="FILE",
        help="Write collected offers to JSON file (default: stdout)",
    )
    parser.add_argument(
        "--no-pretty",
        action="store_true",
        help="Output compact JSON",
    )
    args = parser.parse_args()

    if args.number < 1 or args.number > 500:
        print("Error: --number must be between 1 and 500", file=sys.stderr)
        sys.exit(1)

    try:
        gen = AutoScout24(
            args.url,
            offers=args.number,
            startFromPage=args.start_page,
            waitingTime=args.waiting_time,
            businessType=args.business_type,
        ).format_articles_data()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    collected = []
    result_info = None
    stream_error = None

    for chunk in gen:
        try:
            obj = json.loads(chunk)
        except json.JSONDecodeError:
            continue
        t = obj.get("type")
        if t == "progress":
            continue
        if t == "result_info":
            result_info = obj.get("data") or {}
            continue
        if obj.get("error"):
            stream_error = obj.get("error")
            break
        if "url" in obj and "data" in obj:
            collected.append(obj)

    out = {
        "success": stream_error is None,
        "count": len(collected),
        "data": collected,
        "meta": {
            "num_of_pages": result_info.get("num_of_pages") if result_info else None,
            "num_of_offers": result_info.get("num_of_offers") if result_info else None,
            "start_from_page": result_info.get("start_from_page") if result_info else args.start_page,
            "end_in_page": result_info.get("end_in_page") if result_info else None,
            "offers_requested": args.number,
            "offers_collected": len(collected),
            "errors": (result_info.get("errors_list") or []) if result_info else [],
        },
    }
    if stream_error:
        out["meta"]["errors"] = out["meta"].get("errors") or []
        out["meta"]["errors"].insert(0, stream_error)

    indent = None if args.no_pretty else 2
    payload = json.dumps(out, indent=indent, ensure_ascii=False)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Written {len(collected)} offers to {args.out}", file=sys.stderr)
    else:
        print(payload)

    sys.exit(0 if out["success"] else 1)


if __name__ == "__main__":
    main()
