import importlib.util
from pathlib import Path
import sys
import unittest
_spec = importlib.util.spec_from_file_location('lab_' + Path(__file__).parent.name.replace('-', '_'), Path(__file__).with_name('main.py'))
m = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = m
_spec.loader.exec_module(m)
import copy

class AuditTests(unittest.TestCase):

    def chain(self):
        c = m.AuditChain()
        c.append({'event': 'a'})
        c.append({'event': 'b'})
        return c

    def test_valid_chain(self):
        c = self.chain()
        self.assertEqual(m.verify(c.records), c.records[-1]['hash'])

    def test_payload_edit_detected(self):
        c = self.chain()
        c.records[0]['payload']['event'] = 'changed'
        with self.assertRaises(ValueError):
            m.verify(c.records)

    def test_reordering_detected(self):
        c = self.chain()
        with self.assertRaises(ValueError):
            m.verify(c.records[::-1])

    def test_anchor_detects_truncation(self):
        c = self.chain()
        head = c.records[-1]['hash']
        with self.assertRaises(ValueError):
            m.verify(c.records[:-1], head)
        self.assertEqual(m.verify(c.records[:-1]), c.records[0]['hash'])


if __name__ == '__main__':
    unittest.main()
