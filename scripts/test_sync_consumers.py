import tempfile
import unittest
from pathlib import Path

from sync_consumers import START, END, candidates, routing, updated


class SyncTests(unittest.TestCase):
    def test_preserves_surrounding_text_and_idempotent(self):
        original = 'ユーザーの既存変更\n\n' + START + '\nold\n' + END + '\n末尾\n'
        result = updated(original, START + '\nnew\n' + END)
        self.assertTrue(result.startswith('ユーザーの既存変更\n\n'))
        self.assertTrue(result.endswith('\n末尾\n'))
        self.assertEqual(updated(result, START + '\nnew\n' + END), result)

    def test_bad_markers_are_rejected(self):
        for value in (START, END, START + START + END, END + START):
            with self.subTest(value=value), self.assertRaises(ValueError):
                updated(value, 'replacement')

    def test_append_preserves_existing_rules(self):
        self.assertEqual(updated('既存規約\n', 'block'), '既存規約\n\nblock\n')

    def test_only_enrolled_projects_without_symlinks(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            source = parent / 'source'
            source.mkdir()
            for name, text in [('yes', str(source)), ('no', 'unrelated')]:
                project = parent / name
                project.mkdir()
                (project / 'AGENTS.md').write_text(text)
            (parent / 'linked').symlink_to(parent / 'yes', target_is_directory=True)
            self.assertEqual([p.parent.name for p, _ in candidates(source, [parent])], ['yes'])

    def test_rule_change_changes_routing(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / 'rules').mkdir()
            rule = source / 'rules' / 'interaction.md'
            rule.write_text('before')
            before = routing(source)
            rule.write_text('after')
            self.assertNotEqual(before, routing(source))


if __name__ == '__main__':
    unittest.main()
