import json
from api.whatpulse_api import WhatpulseAPI


def main() -> None:
    # 调用api/whatpulse_api.py中的WhatpulseAPI类中的方法
    whatpulse_api = WhatpulseAPI()
    result = whatpulse_api.get_account_totals()
    # 打印result，json格式化
    print(json.dumps(result, indent=4))
    result = whatpulse_api.activate_profile('1234567890')
    # 打印result，json格式化
    print(json.dumps(result, indent=4))
    result = whatpulse_api.get_user_info('wangsongwangsong417')
    # 打印result，json格式化
    print(json.dumps(result, indent=4))
    # 获取用户计算机列表
    result = whatpulse_api.get_user_computers('wangsongwangsong417', 1)
    # 打印result，json格式化
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()