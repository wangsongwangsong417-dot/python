import logging
import sys
from pathlib import Path


class ColoredFormatter(logging.Formatter):
    """
    带颜色的日志格式化器
    """
    # ANSI 颜色代码
    COLORS = {
        'DEBUG': '\033[36m',      # 青色
        'INFO': '\033[32m',       # 绿色
        'WARNING': '\033[33m',    # 黄色
        'ERROR': '\033[31m',      # 红色
        'CRITICAL': '\033[35m',   # 紫色
        'TIME': '\033[90m',       # 灰色（时间）
        'FILENAME': '\033[94m',   # 蓝色（文件名）
        'LINENO': '\033[35m',     # 紫色（行号）
        'RESET': '\033[0m'        # 重置颜色
    }

    def format(self, record: logging.LogRecord) -> str:
        # 保存原始属性
        original_levelname = record.levelname
        original_filename = record.filename
        original_lineno = record.lineno

        # 为各个字段添加颜色
        # 时间颜色在 formatTime 方法中处理
        # 文件名和行号
        record.filename = f"{self.COLORS['FILENAME']}{record.filename}{self.COLORS['RESET']}"
        record.lineno = f"{self.COLORS['LINENO']}{record.lineno}{self.COLORS['RESET']}"
        # 日志级别
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        record.levelname = f"{level_color}{record.levelname}{self.COLORS['RESET']}"

        result = super().format(record)

        # 恢复原始属性
        record.levelname = original_levelname
        record.filename = original_filename
        record.lineno = original_lineno
        return result

    def formatTime(self, record, datefmt=None):
        """格式化时间并添加颜色"""
        time_str = super().formatTime(record, datefmt)
        return f"{self.COLORS['TIME']}{time_str}{self.COLORS['RESET']}"


def setup_logger(name: str = None, log_file: str = "app.log", level: int = logging.DEBUG) -> logging.Logger:
    """
    配置并返回一个日志记录器

    Args:
        name: 日志记录器名称，默认为调用模块的名称
        log_file: 日志文件路径
        level: 日志级别

    Returns:
        配置好的 Logger 实例
    """
    # 如果没有提供名称，使用调用者的模块名
    if name is None:
        # 获取调用者的文件名（不含扩展名）
        caller_frame = sys._getframe(1)
        caller_path = Path(caller_frame.f_code.co_filename)
        name = caller_path.stem

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 确保 logs 目录存在
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # 将日志文件路径放到 logs 目录中
    log_file_path = logs_dir / Path(log_file).name

    # 日志格式：包含文件名、行号、时间、级别、消息
    formatter = logging.Formatter(
        '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 文件 handler
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 控制台 handler（可选，用于同时输出到控制台）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    # 控制台使用彩色格式化器
    # 彩色格式化器会把 lineno 改成带 ANSI 的字符串，不能用 %(lineno)d，否则报 TypeError
    colored_formatter = ColoredFormatter(
        '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(colored_formatter)
    logger.addHandler(console_handler)

    return logger
