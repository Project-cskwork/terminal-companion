"""
파일 관리 유틸리티
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class FileManager:
    """파일 관리 유틸리티 클래스"""
    
    @staticmethod
    def ensure_directory(directory_path: str) -> bool:
        """디렉토리가 존재하는지 확인하고 없으면 생성"""
        try:
            Path(directory_path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"디렉토리 생성 실패: {directory_path} - {e}")
            return False
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str, backup: bool = True) -> bool:
        """JSON 데이터를 파일에 저장"""
        try:
            # 디렉토리 확인
            directory = os.path.dirname(file_path)
            if directory and not FileManager.ensure_directory(directory):
                return False
            
            # 백업 생성
            if backup and os.path.exists(file_path):
                # 마이크로초를 포함한 타임스탬프로 충돌 방지
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                backup_path = f"{file_path}.backup_{timestamp}"
                
                # 백업 파일이 이미 존재하는 경우 처리
                counter = 1
                while os.path.exists(backup_path):
                    backup_path = f"{file_path}.backup_{timestamp}_{counter}"
                    counter += 1
                
                try:
                    # Windows 호환성을 위해 shutil.move 사용
                    import shutil
                    shutil.copy2(file_path, backup_path)
                    logger.debug(f"백업 파일 생성: {backup_path}")
                except Exception as e:
                    logger.warning(f"백업 생성 실패: {e}")
            
            # 데이터 저장
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.debug(f"JSON 파일 저장 완료: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"JSON 파일 저장 실패: {file_path} - {e}")
            return False
    
    @staticmethod
    def load_json(file_path: str, default: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """JSON 파일에서 데이터 로드"""
        try:
            if not os.path.exists(file_path):
                logger.debug(f"파일이 존재하지 않음: {file_path}")
                return default or {}
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.debug(f"JSON 파일 로드 완료: {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"JSON 파일 로드 실패: {file_path} - {e}")
            return default or {}
    
    @staticmethod
    def get_file_info(file_path: str) -> Optional[Dict[str, Any]]:
        """파일 정보 반환"""
        try:
            if not os.path.exists(file_path):
                return None
            
            stat = os.stat(file_path)
            return {
                "size": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_ctime),
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "accessed": datetime.fromtimestamp(stat.st_atime)
            }
            
        except Exception as e:
            logger.error(f"파일 정보 조회 실패: {file_path} - {e}")
            return None
    
    @staticmethod
    def clean_old_files(directory: str, days: int = 30, pattern: str = "*.log") -> int:
        """오래된 파일 정리"""
        try:
            if not os.path.exists(directory):
                return 0
            
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            deleted_count = 0
            
            for file_path in Path(directory).glob(pattern):
                if file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                        deleted_count += 1
                        logger.debug(f"오래된 파일 삭제: {file_path}")
                    except Exception as e:
                        logger.warning(f"파일 삭제 실패: {file_path} - {e}")
            
            if deleted_count > 0:
                logger.info(f"{deleted_count}개의 오래된 파일이 삭제되었습니다.")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"파일 정리 실패: {directory} - {e}")
            return 0
    
    @staticmethod
    def backup_file(source_path: str, backup_dir: str = "backups") -> Optional[str]:
        """파일 백업"""
        try:
            if not os.path.exists(source_path):
                logger.warning(f"백업할 파일이 존재하지 않음: {source_path}")
                return None
            
            # 백업 디렉토리 생성
            if not FileManager.ensure_directory(backup_dir):
                return None
            
            # 백업 파일명 생성
            source_file = os.path.basename(source_path)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{timestamp}_{source_file}"
            backup_path = os.path.join(backup_dir, backup_filename)
            
            # 파일 복사
            import shutil
            shutil.copy2(source_path, backup_path)
            
            logger.info(f"파일 백업 완료: {source_path} -> {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"파일 백업 실패: {source_path} - {e}")
            return None
    
    @staticmethod
    def safe_write(file_path: str, content: str, encoding: str = 'utf-8') -> bool:
        """안전한 파일 쓰기 (임시 파일 사용)"""
        try:
            temp_path = f"{file_path}.tmp"
            
            # 임시 파일에 쓰기
            with open(temp_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            # 원본 파일 교체
            if os.path.exists(file_path):
                backup_path = f"{file_path}.old"
                os.rename(file_path, backup_path)
            
            os.rename(temp_path, file_path)
            
            # 백업 파일 제거
            if os.path.exists(f"{file_path}.old"):
                os.remove(f"{file_path}.old")
            
            logger.debug(f"안전한 파일 쓰기 완료: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"안전한 파일 쓰기 실패: {file_path} - {e}")
            
            # 정리 작업
            temp_path = f"{file_path}.tmp"
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            
            return False