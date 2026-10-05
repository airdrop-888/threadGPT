"""ThreadsGPT - The Ultimate AI-Powered Threads Growth Engine"""

__version__ = "1.0.0"
__author__ = "ThreadsGPT Contributors"
__license__ = "MIT"

from .core.analytics import Analyzer
from .core.scheduler import Scheduler
from .core.api_client import ThreadsAPI
from .core.database import Database
from .ai.viral_detector import ViralDetector

__all__ = [
    'Analyzer',
    'Scheduler',
    'ThreadsAPI',
    'Database',
    'ViralDetector',
]
