#!/usr/bin/env python3
"""Decode a Salesforce Pub/Sub API Base64 Avro payload using the WOM_Workorder__e schema.

Usage:
    python3 decode_avro.py <base64_payload>

Example:
    python3 decode_avro.py 8IWm7PxlJDAwNWJtMDAwMDBFcE1zckFBRgJCV2VsY29tZSB0byBSYWphdCBCbG9nIG9uIE1lZGl1bSAy
"""

import sys, base64, json, io, avro.schema, avro.io

SCHEMA_FILE = "WOM_Workorder__e.avsc"

def load_schema(path: str):
    with open(path, "r") as f:
        return avro.schema.parse(f.read())

def decode_payload(b64_payload: str, schema):
    binary = base64.b64decode(b64_payload)
    decoder = avro.io.BinaryDecoder(io.BytesIO(binary))
    reader = avro.io.DatumReader(schema)
    record = reader.read(decoder)
    return record

def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)

    b64_payload = sys.argv[1]
    schema = load_schema(SCHEMA_FILE)
    record = decode_payload(b64_payload, schema)

    # Pretty‑print the Avro record as JSON
    print(json.dumps(record, indent=2))

if __name__ == "__main__":
    main()
