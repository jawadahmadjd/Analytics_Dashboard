"""
National Bonds Corporation - JDAgent Root Shim
Imports directly from backend/jd_engine.py for single source of truth across all apps.
Author: Jawad Ahmad | Product AI Solutions
"""

from backend.jd_engine import JDAgent, resolve_data_path, DEEPSEEK_DEFAULT_KEY, DEEPSEEK_API_URL

__all__ = ['JDAgent', 'resolve_data_path', 'DEEPSEEK_DEFAULT_KEY', 'DEEPSEEK_API_URL']
