"""
由项目根目录的 sitecustomize.py 加载；解释器启动时尽早执行。
仅当「当前工作目录在本项目内」且为 TTY 时清屏；可选过滤 urllib3/LibreSSL 警告。
"""

from __future__ import annotations

import os
import sys
import warnings
from pathlib import Path


def _cwd_under_project(project_root: Path) -> bool:
    try:
        cwd = Path.cwd().resolve()
        root = project_root.resolve()
        cwd.relative_to(root)
        return True
    except (OSError, ValueError):
        return False


def _should_skip_for_argv() -> bool:
    """避免清屏干扰 pip / venv 等工具输出。"""
    if len(sys.argv) < 3:
        return False
    if sys.argv[1] != "-m":
        return False
    mod = sys.argv[2].split(".")[0]
    return mod in ("pip", "pip3", "ensurepip", "venv")


def run_at_interpreter_startup(project_root: Path) -> None:
    try:
        if not _cwd_under_project(project_root):
            return
        if not sys.stdout.isatty():
            return
        if _should_skip_for_argv():
            return

        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

        warnings.filterwarnings(
            "ignore",
            message=r".*urllib3 v2 only supports OpenSSL.*",
        )
    except Exception:
        pass
