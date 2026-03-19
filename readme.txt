自动清屏：新建/重建 .venv 后在本目录执行一次
  .venv/bin/python scripts/install_sitecustomize_hook.py
之后在本项目路径下用该 venv 运行 python，会先清屏（需真实终端 TTY；python -m pip 等除外）。
