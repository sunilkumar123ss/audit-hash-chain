"""Canonical JSON audit chains with optional independently trusted head."""
import argparse
import hashlib
import json
ZERO = '0' * 64

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).encode('utf-8')

def hash_body(index, previous, payload):
    return hashlib.sha256(canonical({'index': index, 'previous': previous, 'payload': payload})).hexdigest()

def verify(records, expected_head=None):
    if not isinstance(records, list):
        raise ValueError('Records must be a list')
    previous = ZERO
    for (index, record) in enumerate(records):
        if not isinstance(record, dict) or set(record) != {'index', 'previous', 'payload', 'hash'} or type(record['index']) is not int or (record['index'] != index) or (not isinstance(record['payload'], dict)):
            raise ValueError('Invalid record shape or sequence')
        if record['previous'] != previous or record['hash'] != hash_body(index, previous, record['payload']):
            raise ValueError('Broken audit chain')
        previous = record['hash']
    if expected_head is not None and previous != expected_head:
        raise ValueError('Trusted head mismatch')
    return previous

class AuditChain:

    def __init__(self):
        self.records = []

    def append(self, payload):
        if not isinstance(payload, dict):
            raise ValueError('Payload must be a JSON object')
        copied = json.loads(canonical(payload))
        previous = verify(self.records)
        index = len(self.records)
        row = {'index': index, 'previous': previous, 'payload': copied, 'hash': hash_body(index, previous, copied)}
        self.records.append(row)
        return row['hash']

def demo():
    chain = AuditChain()
    chain.append({'event': 'synthetic-job-created', 'id': 'a'})
    head = chain.append({'event': 'synthetic-job-completed', 'id': 'a'})
    return {'records': chain.records, 'trusted_head_example': head, 'verified': verify(chain.records, head) == head}
if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    print(json.dumps(demo(), indent=2))
