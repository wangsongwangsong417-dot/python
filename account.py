import json
import logging
import requests
from config.logger_util import setup_logger

# 初始化日志器
logger = setup_logger(log_file="account.log", level=logging.INFO)

try:
    logger.info("开始请求 API")
    response = requests.get('http://localhost:3490/v1/account-totals', timeout=10)
    logger.info("API 请求成功")
    response.raise_for_status()
    data = response.json()
    # 打印格式化的 JSON 响应
    logger.info(f"API 响应数据: {json.dumps(data, ensure_ascii=False)}")

    keys = data['keys']
    clicks = data['clicks']
    rank_uptime = data['ranks']['rank_uptime']

    message = "Current keys: {}, current clicks: {}, rank in uptime: {}".format(
        keys, clicks, rank_uptime
    )
    logger.info(message)
except requests.exceptions.RequestException as e:
    logger.error(f"API 请求失败: {e}")
except KeyError as e:
    logger.error(f"响应数据格式错误，缺少字段: {e}")
except Exception as e:
    logger.error(f"发生未知错误: {e}", exc_info=True)