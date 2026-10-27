# ruff: noqa: E402

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from utils.skill_path import resolve_skill_root


def _touch_wrapper(skill_root: Path) -> None:
    scripts = skill_root / "scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "jy_wrapper.py").write_text("# stub\n", encoding="utf-8")


class TestSkillPath(unittest.TestCase):
    def test_repo_examples_dir_resolves_to_repo_root(self):
        root, _attempted = resolve_skill_root(str(ROOT / "examples"))
        self.assertIsNotNone(root)
        self.assertEqual(os.path.realpath(root), os.path.realpath(str(ROOT)))

    def test_project_cursor_skill_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "app"
            skill = project / ".cursor" / "skills" / "jianying-editor"
            _touch_wrapper(skill)
            nested = project / "videos"
            nested.mkdir(parents=True)

            root, _attempted = resolve_skill_root(str(nested))

            self.assertEqual(os.path.realpath(root), os.path.realpath(str(skill)))

    def test_user_cursor_skill_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            skill = home / ".cursor" / "skills" / "jianying-editor"
            _touch_wrapper(skill)
            project = Path(tmp) / "empty-project"
            project.mkdir()
            old_home = os.environ.get("HOME")
            os.environ["HOME"] = str(home)
            try:
                root, _attempted = resolve_skill_root(str(project))
            finally:
                if old_home is None:
                    os.environ.pop("HOME", None)
                else:
                    os.environ["HOME"] = old_home

            self.assertEqual(os.path.realpath(root), os.path.realpath(str(skill)))

    def test_env_override_wins(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "custom-skill"
            _touch_wrapper(skill)
            old = os.environ.get("JY_SKILL_ROOT")
            os.environ["JY_SKILL_ROOT"] = str(skill)
            try:
                root, attempted = resolve_skill_root(str(ROOT / "examples"))
            finally:
                if old is None:
                    os.environ.pop("JY_SKILL_ROOT", None)
                else:
                    os.environ["JY_SKILL_ROOT"] = old

            self.assertEqual(os.path.realpath(root), os.path.realpath(str(skill)))
            self.assertEqual(attempted[0], os.path.abspath(str(skill)))


if __name__ == "__main__":
    unittest.main()
