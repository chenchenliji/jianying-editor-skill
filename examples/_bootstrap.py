import os
import sys
from typing import List, Optional, Tuple

_EDITOR_REL_PATHS = (
    os.path.join(".cursor", "skills", "jianying-editor"),
    os.path.join(".agents", "skills", "jianying-editor"),
    os.path.join(".agent", "skills", "jianying-editor"),
    os.path.join(".trae", "skills", "jianying-editor"),
    os.path.join(".claude", "skills", "jianying-editor"),
    os.path.join(".codex", "skills", "jianying-editor"),
    os.path.join("skills", "jianying-editor"),
)


def _build_candidates(start_dir: str) -> List[str]:
    cwd = os.getcwd()
    home = os.path.expanduser("~")
    local_bases = [
        os.path.abspath(start_dir),
        os.path.abspath(os.path.join(start_dir, "..")),
        os.path.abspath(os.path.join(start_dir, "..", "..")),
        os.path.abspath(os.path.join(start_dir, "..", "..", "..")),
    ]
    candidates = list(local_bases)
    for base in local_bases + [os.path.abspath(cwd)]:
        for rel in _EDITOR_REL_PATHS:
            candidates.append(os.path.abspath(os.path.join(base, rel)))
    for rel in _EDITOR_REL_PATHS:
        candidates.append(os.path.abspath(os.path.join(home, rel)))
    return candidates


def resolve_skill_root(start_dir: str) -> Optional[str]:
    env_root = os.getenv("JY_SKILL_ROOT", "").strip()
    if env_root:
        env_root = os.path.abspath(env_root)
        if os.path.exists(os.path.join(env_root, "scripts", "jy_wrapper.py")):
            return env_root

    for candidate in _build_candidates(start_dir):
        if os.path.exists(os.path.join(candidate, "scripts", "jy_wrapper.py")):
            return candidate
    return None


def resolve_skill_root_or_raise(start_dir: str) -> str:
    root = resolve_skill_root(start_dir)
    if root:
        return root
    raise ImportError("Could not locate jianying-editor skill root. Set JY_SKILL_ROOT.")


def ensure_skill_scripts_on_path(start_dir: str) -> Tuple[str, str]:
    skill_root = resolve_skill_root_or_raise(start_dir)
    scripts_dir = os.path.join(skill_root, "scripts")
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    return skill_root, scripts_dir
