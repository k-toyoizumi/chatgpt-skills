import json
from pathlib import Path
import tempfile
import unittest
from codex_status import Tracker, recommend


def usage(n, **extra):
    return dict(input_tokens=n, output_tokens=10, total_tokens=n+10, **extra)


def event(kind, **kwargs):
    return json.dumps({'type':'event_msg', 'timestamp':'2026-10-24T00:00:00Z', 'payload':dict(type=kind, **kwargs)})+'\n'


def tokens(n, last=20, **extra):
    return event('token_count',info={'total_token_usage':usage(n, **extra), 'last_token_usage':usage(last, **extra), 'model_context_window':100})


class Tests(unittest.TestCase):
    def test_thresholds(self):
        for percent, expected in [(15,'引き継ぎ'),(30,'整理'),(31,'追加の提案なし')]:
            self.assertIn(expected, recommend(percent,{}, {})[0])

    def test_incremental_and_partial(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.jsonl'; p.write_text(tokens(100))
            t=Tracker(p); t.poll()
            with p.open('a') as f: f.write(tokens(150)[:-1])
            t.poll(); self.assertEqual(t.info['total_token_usage']['input_tokens'],100)
            with p.open('a') as f: f.write('\n')
            t.poll(); self.assertEqual(t.info['total_token_usage']['input_tokens'],150)
            before=t.render(); t.poll(); self.assertEqual(before,t.render())

    def test_turn_delta(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.jsonl'
            p.write_text(tokens(100)+event('task_started')+tokens(200)+tokens(250)+event('task_complete'))
            t=Tracker(p); t.poll()
            self.assertEqual(t.turn['input_tokens'],150)
            self.assertFalse(t.in_turn)

    def test_missing_fields_hidden(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.jsonl';p.write_text(tokens(10))
            t=Tracker(p);t.poll();self.assertNotIn('| cache write', t.render())

    def test_truncate_resets(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'test.jsonl';p.write_text(tokens(100)*3)
            t=Tracker(p);t.poll();p.write_text(tokens(10));t.poll()
            self.assertEqual(t.info['total_token_usage']['input_tokens'],10)

    def test_input_growth(self):
        self.assertIn('入力が増加',recommend(None,usage(40000),usage(10000))[0])


if __name__=='__main__': unittest.main()
