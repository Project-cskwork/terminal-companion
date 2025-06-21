#!/usr/bin/env python3
"""
Terminal AI Companion - 감정적이고 지적인 동반자
Cross-platform terminal-based AI girlfriend/boyfriend with memory
Enterprise-grade modular architecture
"""

import sys
import os
import logging

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 전체 로깅 시스템에서 ERROR 레벨 이하 비활성화
logging.disable(logging.ERROR)

# mem0 및 관련 라이브러리 로거 억제 (프로그램 시작 시점에 설정)
# 이 설정은 다른 모듈이 임포트되기 전에 실행되어야 함
mem0_loggers = [
    '',  # 빈 문자열은 루트 로거
    'root',
    'mem0',
    'mem0.memory',
    'mem0.memory.main',
    'mem0.memory.base',
    'mem0.memory.memory',
    'mem0.vector_stores',
    'mem0.embeddings',
    'mem0.llms',
    'mem0.utils',
    'chromadb',
    'chromadb.telemetry',
    'chromadb.api',
    'chromadb.db',
    'chromadb.segment',
    'chromadb.config',
    'httpx',
    'httpcore',
    'openai',
    'openai._base_client',
    'urllib3',
    'urllib3.connectionpool',
    'requests',
    'requests.packages.urllib3',
    '__main__'  # 메인 모듈
]

for logger_name in mem0_loggers:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.CRITICAL)
    logger.handlers = []
    logger.propagate = False

# 루트 로거 설정 (mem0이 루트 로거로 오류를 출력하는 경우 대비)
root_logger = logging.getLogger()
root_logger.setLevel(logging.CRITICAL)

# 루트 로거의 모든 핸들러 제거
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Chromadb 텔레메트리 비활성화
os.environ['ANONYMIZED_TELEMETRY'] = 'False'

from src.Controller import CompanionController
from src.Utils import setup_logging
from src.Config import config

def main():
    """메인 함수"""
    # 로깅 재활성화 (CRITICAL 레벨만)
    logging.disable(logging.NOTSET)
    
    # 로깅 설정 (우리 애플리케이션의 로거만 설정)
    app_logger = setup_logging()
    
    # 우리 애플리케이션 로거는 다시 활성화
    app_logger.setLevel(logging.INFO)
    
    # 터미널 컴패니언 로거만 활성화
    terminal_logger = logging.getLogger('terminal_companion')
    terminal_logger.setLevel(logging.INFO)
    
    # 다른 모든 로거는 CRITICAL로 유지
    logging.getLogger().setLevel(logging.CRITICAL)
    
    # 컨트롤러 생성 및 실행
    controller = CompanionController()
    controller.run()

if __name__ == "__main__":
    main()