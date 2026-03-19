import json
import logging
import requests
import http.client
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
    url = 'http://localhost:3490/v1/profiles/activate'
    data = {'profile_id': '1234567890'}
    response = requests.post(url, json=data)
    logger.info(f"API 请求成功: {response.json()}")
    url = "https://whatpulse.org/api/v1/users/wangsongwangsong417"
    payload = {}
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiNWVkMzhhZDBiM2FjMzc3MDA3NzAwNjc5ZjU1ZjY4Njg1NTI1ZWY1YjAwOGQ3MDg4ODZkNGE5ZmRkM2Q2NDUxMzZjMWJjNWMyYWFmZGU3MzkiLCJpYXQiOjE3NzM5MzczOTAuMDU5NDA1LCJuYmYiOjE3NzM5MzczOTAuMDU5NDEsImV4cCI6MTgwNTQ3MzM5MC4wNTA4MDIsInN1YiI6IjE0NjM0OTgiLCJzY29wZXMiOlsidXNlci1wdWJsaWMtYXBpIl19.ubmE5uymjHHk3ROP3AMJKHttrNAmpmnGdVTW6x1NM5HPHrhgkqqNvuTjCFhLjjkRlSdMIp858DwwCAZm1_tVMMO28Wzuua5KqKA2xXPXIfLoZGv6jyPc7frj9lq6q_EBFmUXIv9r7meBgUtYB8oFDh2WSxfaYkEM6wOdDMAFgVrwa5C2koSk_Snru2IJuLowk9tJeOQGxlzSZhpiKVsQbQA8j6tQEDl4kWcOPmuGloyUtI6kKMS4FAuNxcFDQvLjPh3irJIK091-wamEiLuYm0fpApVIBYC_ub5Y0v-P0m9hkslt4zO7IweD3PiOKbjE_kGGksXa1pJepq9k7-annjdbF7VL0s4CvUkJ8J7s_MAvee3oApMT9bhAabD_PXVKqsG3WDQoKqevymUCEcjf-MIbQmEgcIpFuBsiMQlacfrj5dtAWfHUw_U8stwxUqjEc33K-0tO8TTv4ayYYz5Vp7S4T3qRiHuQNIbeb-xH4z3Jg0uE4yRHv--M5iDD9bDgrFjFhc-XD86zKS_nHESPeZZKjiGloX77kLdFT3NRli17U0khktTxsboPkl2XNWZH6o8q3tOVJPfY-QU7joUeppBuMHCsk2FiRh-uzO8Ckt9vozbh3v6U4qB9M-rlxNszM99x15oUeMJmlvTuWarDVIsA2PXfXGpy30A-SFAtdRk'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    logger.info(f"API 请求用户信息成功: {response.json()}")
    conn = http.client.HTTPSConnection("whatpulse.org")
    payload = ''
    # API 对 is_archived 做 boolean 校验：URL 里用字符串 "false" 常会被拒绝，需用 0/1。
    conn.request("GET", "/api/v1/users/wangsongwangsong417/computers?is_archived=1", payload, headers)
    res = conn.getresponse()
    data = res.read()
    logger.info("xxx")
    print(data.decode("utf-8"))
except requests.exceptions.RequestException as e:
    logger.error(f"API 请求失败: {e}")
except KeyError as e:
    logger.error(f"响应数据格式错误，缺少字段: {e}")
except Exception as e:
    logger.error(f"发生未知错误: {e}", exc_info=True)