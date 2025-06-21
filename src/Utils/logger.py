"""
로깅 유틸리티
"""

import os
import logging
import logging.handlers
from datetime import datetime
from typing import Optional

from ..Config import config

def setup_logging(
    log_level: Optional[str] = None,
    log_dir: Optional[str] = None,
    log_format: Optional[str] = None
) -> logging.Logger:
    """로깅 시스템 설정"""
    
    # 설정값 사용 또는 기본값
    level = log_level or config.logging.level
    directory = log_dir or config.logging.log_dir
    format_str = log_format or config.logging.format
    
    # 로그 디렉토리 생성
    os.makedirs(directory, exist_ok=True)
    
    # 로그 레벨 설정
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # 로거 생성
    logger = logging.getLogger('terminal_companion')
    logger.setLevel(numeric_level)
    
    # 기존 핸들러 제거 (중복 방지)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # 포매터 생성
    formatter = logging.Formatter(format_str)
    
    # 파일 핸들러 (회전 로그)
    log_file = os.path.join(directory, f"companion_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=config.logging.max_file_size,
        backupCount=config.logging.backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # 콘솔 핸들러 (ERROR 레벨 이상만)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info(f"로깅 시스템이 초기화되었습니다. 레벨: {level}, 디렉토리: {directory}")
    return logger

def get_logger(name: str) -> logging.Logger:
    """모듈별 로거 반환"""
    return logging.getLogger(f'terminal_companion.{name}')

class LoggerMixin:
    """로거 믹스인 클래스"""
    
    @property
    def logger(self) -> logging.Logger:
        """클래스별 로거 반환"""
        return get_logger(self.__class__.__name__)