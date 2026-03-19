# 写一个main函数，从项目根目录执行
# python main.py
# 或
# python -m main

def main() -> None:
    from api.whatpulse_api import run

    run()


if __name__ == "__main__":
    main()