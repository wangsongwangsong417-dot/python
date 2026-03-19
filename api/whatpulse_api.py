import json
import logging
import requests
import http.client
from config.logger_util import setup_logger


class WhatpulseAPI:
    """
    Whatpulse API 接口类
    """

    def __init__(self, log_file: str = "account.log", level: int = logging.INFO):
        """
        初始化 WhatpulseAPI 实例

        Args:
            log_file: 日志文件路径
            level: 日志级别
        """
        self.logger = setup_logger(log_file=log_file, level=level)
        self.base_url = "http://localhost:3490/v1"
        self.whatpulse_org_base_url = "https://whatpulse.org/api/v1"
        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiNWVkMzhhZDBiM2FjMzc3MDA3NzAwNjc5ZjU1ZjY4Njg1NTI1ZWY1YjAwOGQ3MDg4ODZkNGE5ZmRkM2Q2NDUxMzZjMWJjNWMyYWFmZGU3MzkiLCJpYXQiOjE3NzM5MzczOTAuMDU5NDA1LCJuYmYiOjE3NzM5MzczOTAuMDU5NDEsImV4cCI6MTgwNTQ3MzM5MC4wNTA4MDIsInN1YiI6IjE0NjM0OTgiLCJzY29wZXMiOlsidXNlci1wdWJsaWMtYXBpIl19.ubmE5uymjHHk3ROP3AMJKHttrNAmpmnGdVTW6x1NM5HPHrhgkqqNvuTjCFhLjjkRlSdMIp858DwwCAZm1_tVMMO28Wzuua5KqKA2xXPXIfLoZGv6jyPc7frj9lq6q_EBFmUXIv9r7meBgUtYB8oFDh2WSxfaYkEM6wOdDMAFgVrwa5C2koSk_Snru2IJuLowk9tJeOQGxlzSZhpiKVsQbQA8j6tQEDl4kWcOPmuGloyUtI6kKMS4FAuNxcFDQvLjPh3irJIK091-wamEiLuYm0fpApVIBYC_ub5Y0v-P0m9hkslt4zO7IweD3PiOKbjE_kGGksXa1pJepq9k7-annjdbF7VL0s4CvUkJ8J7s_MAvee3oApMT9bhAabD_PXVKqsG3WDQoKqevymUCEcjf-MIbQmEgcIpFuBsiMQlacfrj5dtAWfHUw_U8stwxUqjEc33K-0tO8TTv4ayYYz5Vp7S4T3qRiHuQNIbeb-xH4z3Jg0uE4yRHv--M5iDD9bDgrFjFhc-XD86zKS_nHESPeZZKjiGloX77kLdFT3NRli17U0khktTxsboPkl2XNWZH6o8q3tOVJPfY-QU7joUeppBuMHCsk2FiRh-uzO8Ckt9vozbh3v6U4qB9M-rlxNszM99x15oUeMJmlvTuWarDVIsA2PXfXGpy30A-SFAtdRk'
        }

    def get_account_totals(self, timeout: int = 10) -> dict:
        """
        获取账户总统计信息

        Args:
            timeout: 请求超时时间（秒）

        Returns:
            账户总统计数据
        """
        try:
            self.logger.info("开始请求账户总统计信息")
            url = f"{self.base_url}/account-totals"
            response = requests.get(url, timeout=timeout)
            self.logger.info("账户总统计信息请求成功")
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"API 响应数据: {json.dumps(data, ensure_ascii=False)}")
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"账户总统计信息请求失败: {e}")
            raise
        except Exception as e:
            self.logger.error(f"获取账户总统计信息时发生未知错误: {e}", exc_info=True)
            raise

    def activate_profile(self, profile_id: str) -> dict:
        """
        激活指定的配置文件

        Args:
            profile_id: 配置文件 ID

        Returns:
            激活操作的响应数据
        """
        try:
            self.logger.info(f"开始激活配置文件: {profile_id}")
            url = f"{self.base_url}/profiles/activate"
            data = {'profile_id': profile_id}
            response = requests.post(url, json=data)
            self.logger.info("配置文件激活成功")
            response.raise_for_status()
            result = response.json()
            self.logger.info(f"API 请求成功: {result}")
            return result
        except requests.exceptions.RequestException as e:
            self.logger.error(f"激活配置文件失败: {e}")
            raise
        except Exception as e:
            self.logger.error(f"激活配置文件时发生未知错误: {e}", exc_info=True)
            raise

    def get_user_info(self, username: str) -> dict:
        """
        获取用户信息

        Args:
            username: Whatpulse 用户名

        Returns:
            用户信息数据
        """
        try:
            self.logger.info(f"开始请求用户信息: {username}")
            url = f"{self.whatpulse_org_base_url}/users/{username}"
            response = requests.get(url, headers=self.headers)
            self.logger.info("用户信息请求成功")
            response.raise_for_status()
            data = response.json()
            self.logger.info(f"API 请求成功: {data}")
            return data
        except requests.exceptions.RequestException as e:
            self.logger.error(f"用户信息请求失败: {e}")
            raise
        except Exception as e:
            self.logger.error(f"获取用户信息时发生未知错误: {e}", exc_info=True)
            raise

    def get_user_computers(self, username: str, is_archived: int = 1) -> dict:
        """
        获取用户的计算机列表

        Args:
            username: Whatpulse 用户名
            is_archived: 是否只获取已归档的计算机（0 = 否，1 = 是）

        Returns:
            用户计算机列表数据
        """
        try:
            self.logger.info(f"开始请求用户计算机列表: {username}")
            conn = http.client.HTTPSConnection("whatpulse.org")
            payload = ''
            url = f"/api/v1/users/{username}/computers?is_archived={is_archived}"
            conn.request("GET", url, payload, self.headers)
            res = conn.getresponse()
            data = res.read()
            result = json.loads(data.decode("utf-8"))
            self.logger.info("用户计算机列表请求成功")
            return result
        except Exception as e:
            self.logger.error(f"获取用户计算机列表失败: {e}", exc_info=True)
            raise

    def process_account_totals(self, data: dict) -> str:
        """
        处理账户总统计数据并生成格式化消息

        Args:
            data: 账户总统计数据

        Returns:
            格式化的消息字符串
        """
        try:
            keys = data['keys']
            clicks = data['clicks']
            rank_uptime = data['ranks']['rank_uptime']
            message = "Current keys: {}, current clicks: {}, rank in uptime: {}".format(
                keys, clicks, rank_uptime
            )
            self.logger.info(message)
            return message
        except KeyError as e:
            self.logger.error(f"响应数据格式错误，缺少字段: {e}")
            raise
        except Exception as e:
            self.logger.error(f"处理账户总统计数据时发生未知错误: {e}", exc_info=True)
            raise