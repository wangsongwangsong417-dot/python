"""
Python 启动时会自动 import sitecustomize（若位于当前环境的 site-packages）。

通过 scripts/install_sitecustomize_hook.py 将本文件以符号链接安装到 .venv/.../site-packages/
后，在本项目目录下使用该 venv 运行任意 python 会先清屏。
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

_ROOT = Path(__file__).resolve().parent

_spec = spec_from_file_location(
    "_project_site_startup",
    _ROOT / "config" / "project_site_startup.py",
)
_mod = module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_mod)
_mod.run_at_interpreter_startup(_ROOT)
