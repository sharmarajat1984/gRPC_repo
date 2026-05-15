#!/usr/bin/env python3
"""
Decode a Salesforce Pub/Sub API replay_id from its base64 form to a numeric value.

Usage:
    python decode_replay_id.py AAAAAArvySIAAA==
    python decode_replay_id.py AAAAAArvySIAAA== AAAAAAAAwxUAAA==
    echo "AAAAAArvySIAAA==" | python decode_replay_id.py
    python decode_replay_id.py --verbose AAAAAArvySIAAA==

Note:
    Salesforce treats replay IDs as opaque. Use the numeric value for logging
    and monitoring only. To resume a subscription, always pass the original
    bytes back as replay_id with replay_preset=CUSTOM.
"""

import argparse
import base64
import struct
import sys


def decode_replay_id(b64_value: str) -> dict:
    """Decode a base64 replay_id and return its components."""
    raw = base64.b64decode(b64_value)

    if len(raw) < 8:
        raise ValueError(
            f"Replay ID must decode to at least 8 bytes, got {len(raw)}: {raw.hex()}"
        )

    event_position = struct.unpack(">q", raw[:8])[0]
    sub_sequence_bytes = raw[8:]

    return {
        "input": b64_value,
        "hex": raw.hex(),
        "length": len(raw),
        "replay_id": event_position,
        "sub_sequence_hex": sub_sequence_bytes.hex() if sub_sequence_bytes else "(none)",
    }


def main():
    parser = argparse.ArgumentParser(
        description="Decode Salesforce Pub/Sub API replay_id base64 to numeric value.",
        epilog="Example: python decode_replay_id.py AAAAAArvySIAAA==",
    )
    parser.add_argument(
        "replay_ids",
        nargs="*",
        help="One or more base64-encoded replay_id strings. If omitted, reads from stdin.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show hex breakdown and sub-sequence bytes.",
    )
    args = parser.parse_args()

    # Collect inputs: CLI args take priority, otherwise read stdin
    inputs = args.replay_ids
    if not inputs:
        if sys.stdin.isatty():
            parser.print_help()
            sys.exit(1)
        inputs = [line.strip() for line in sys.stdin if line.strip()]

    exit_code = 0
    for value in inputs:
        try:
            result = decode_replay_id(value)
        except (ValueError, base64.binascii.Error) as e:
            print(f"ERROR decoding {value!r}: {e}", file=sys.stderr)
            exit_code = 1
            continue

        if args.verbose:
            print(f"Input:           {result['input']}")
            print(f"Decoded bytes:   {result['length']}")
            print(f"Hex:             {result['hex']}")
            print(f"Replay ID:       {result['replay_id']:,}")
            print(f"Sub-sequence:    {result['sub_sequence_hex']}")
            print("-" * 40)
        else:
            print(result["replay_id"])

    sys.exit(exit_code)


if __name__ == "__main__":
    main()