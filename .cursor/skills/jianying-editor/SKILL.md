---
name: jianying-editor
description: >
  剪映专业版自动化剪辑技能。用户要做视频、生成剪映草稿、加字幕、配音、配乐、特效、转场、录屏变焦、
  网页动效或导出成片时使用。实现代码在仓库根目录，本文件是 Cursor 的发现入口。
---

# JianYing Editor Skill

用这个技能自动搭建剪映专业版时间轴。最终渲染仍由桌面版剪映完成。

## 技能根目录

Cursor 从本文件发现技能，可执行代码在仓库根目录，不在本文件所在目录。

把同时满足下面条件的目录当作 `SKILL_ROOT`：

- 目录里有 `scripts/jy_wrapper.py`
- 优先使用环境变量 `JY_SKILL_ROOT`
- 否则使用本文件向上三级的仓库根目录（`.cursor/skills/jianying-editor` → 仓库根）
- 若本仓库被克隆到 `.cursor/skills/jianying-editor`、`.agents/skills/jianying-editor` 或 `~/.cursor/skills/jianying-editor`，该克隆目录本身就是 `SKILL_ROOT`

动手前先读：

1. `<SKILL_ROOT>/SKILL.md`
2. `<SKILL_ROOT>/docs/agent-playbook.md`
3. `<SKILL_ROOT>/docs/minimal-command-sop.md`
4. `<SKILL_ROOT>/rules/setup.md`

普通剪辑请求按 playbook 里的 Quick Edit Runtime Template 和 Acceptance Checklist 执行。

## 必须遵守

1. 业务剪辑脚本放在用户项目根目录，不要写进技能安装目录。
2. 每个脚本按 `rules/setup.md` 初始化，并在结束时调用 `project.save()`。
3. 配乐放在 audio 轨道。有旁白时，字幕要和语音时间对齐。
4. 简单演示可以用默认音乐。正式项目先检索 `data/cloud_music_library.csv`，再向用户推荐曲目。
5. 草稿生成支持 Windows 与 macOS。自动导出只支持 Windows UI 自动化；macOS 生成草稿后在剪映里手动导出。
6. 不支持 CapCut 国际版和手机端剪映。

## 任务入口

- 云端视频 + 音乐：`rules/media.md`、`rules/audio-voice.md`，参考 `examples/cloud_video_music_tts_demo.py`
- 文案配音字幕：`rules/text.md`、`rules/audio-voice.md`，API `add_narrated_subtitles`
- 录屏变焦：`rules/recording.md`，执行 `tools/recording/recorder.py`
- 特效转场：`rules/effects.md`、`rules/keyframes.md`，检索 `scripts/asset_search.py`
- 影视解说：`rules/generative.md`，执行 `scripts/movie_commentary_builder.py`
- 导出与校验：`rules/core.md`、`rules/cli.md`，执行 `scripts/auto_exporter.py` 与 `scripts/api_validator.py --json`

## 初始化

```python
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
env_root = os.getenv("JY_SKILL_ROOT", "").strip()
skill_root = next((p for p in [
    env_root,
    os.path.join(current_dir, ".cursor", "skills", "jianying-editor"),
    os.path.join(current_dir, ".agents", "skills", "jianying-editor"),
    os.path.join(current_dir, ".agent", "skills", "jianying-editor"),
    os.path.join(current_dir, ".trae", "skills", "jianying-editor"),
    os.path.join(current_dir, ".claude", "skills", "jianying-editor"),
    os.path.join(current_dir, ".codex", "skills", "jianying-editor"),
    os.path.join(current_dir, "skills", "jianying-editor"),
    os.path.join(current_dir, "..", ".cursor", "skills", "jianying-editor"),
    os.path.join(current_dir, "..", ".agents", "skills", "jianying-editor"),
    os.path.abspath(".cursor/skills/jianying-editor"),
    os.path.abspath(".agents/skills/jianying-editor"),
    os.path.abspath(".agent/skills/jianying-editor"),
    os.path.abspath("skills/jianying-editor"),
    os.path.expanduser("~/.cursor/skills/jianying-editor"),
    os.path.expanduser("~/.agents/skills/jianying-editor"),
    os.path.expanduser("~/.claude/skills/jianying-editor"),
    os.path.dirname(current_dir),
] if p and os.path.exists(os.path.join(p, "scripts", "jy_wrapper.py"))), None)

if not skill_root:
    raise ImportError("Could not find jianying-editor skill root. Set JY_SKILL_ROOT.")
sys.path.insert(0, os.path.join(skill_root, "scripts"))
from jy_wrapper import JyProject
```
