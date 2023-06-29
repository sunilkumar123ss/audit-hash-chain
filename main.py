"""Canonical JSON audit chains with optional independently trusted head."""
import argparse
import hashlib
import json
ZERO = '0' * 64

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')

def hash_body(index, previous, payload):
    return hashlib.sha256(canonical({'index': index, 'previous': previous, 'payload': payload})).hexdigest()
