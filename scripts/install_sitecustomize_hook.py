#!/usr/bin/env python3
"""
将项目根目录的 sitecustomize.py 符号链接到当前 Python 环境的 site-packages。

用法（创建或重建 .venv 后执行一次）：
  .venv/bin/python scripts/install_sitecustomize_hook.py
"""

from __future__ import annotations

import os
import sys
import sysconfig
from pathlib import Path


def main() -> int:
    in_venv = sys.prefix != sys.base_prefix or hasattr(sys, "real_prefix")
    if not in_venv:
        print("请在项目虚拟环境中运行，例如：", file=sys.stderr)
        print("  .venv/bin/python scripts/install_sitecustomize_hook.py", file=sys.stderr)
        return 1

    purelib = Path(sysconfig.get_path("purelib"))
    dst = purelib / "sitecustomize.py"
    project_root = Path(__file__).resolve().parent.parent
    src = project_root / "sitecustomize.py"

    if not src.is_file():
        print(f"找不到 {src}", file=sys.stderr)
        return 1

    try:
        if dst.is_symlink() or dst.is_file():
            dst.unlink()
    except OSError as e:
        print(f"无法移除旧文件 {dst}: {e}", file=sys.stderr)
        return 1

    try:
        rel = os.path.relpath(src, dst.parent)
        dst.symlink_to(rel)
    except OSError as e:
        print(f"符号链接失败: {e}", file=sys.stderr)
        return 1

    print(f"已安装: {dst} -> {src}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
