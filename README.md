# Audit hash chain

Detect changes and reordering in canonical JSON records, with optional trusted head anchoring.

Educational implementation with synthetic examples.

## Run

Python 3.9 or newer; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

The default example uses synthetic data and needs no credentials, installation, or network connection. The script also works by absolute path from another working directory.

## Behavior

Each record includes its index, previous record hash, JSON object payload, and SHA-256 of those fields. Verification checks shape, sequence, links, and hashes. Supplying an independently retained expected head detects truncation as well as edits.

## Use in Python

```python
from main import AuditChain, verify

chain = AuditChain()
head = chain.append({'event': 'example-job-created'})
# Retain head independently before trusting this verification later.
assert verify(chain.records, expected_head=head) == head
```

## Design limits

This is tamper-evident only relative to a trusted anchor. An attacker able to replace both the entire chain and its trusted head can rewrite history. It is not a signature, timestamp authority, access control, durable logger, or proof that payload statements are true. Payloads are copied through JSON serialization.

## Verification

The unit tests cover successful operations, failure paths, and invariants. These are local correctness checks, not production performance or security certification.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
