"""
Shared modules for article-workflow plugin.

This package provides core functionality for the article creation workflow:
- Pipeline state management
- Retry logic and error handling
- User confirmation management
- Configuration loading

Usage:
    from shared import PipelineManager, RetryManager, UserConfirm, get_config
    pipeline = PipelineManager()
    retry = RetryManager()
    user_confirm = UserConfirm(pipeline.pipeline_id)
    api_key = get_config("gemini_api_key")
"""

from .pipeline_manager import PipelineManager
from .retry_manager import RetryManager, RetryableErrorType, NonRetryableErrorType
from .user_confirm import UserConfirm, ConfirmationType
from .config_loader import (
    get_config,
    get_config_bool,
    get_config_int,
    get_config_list,
    require_config,
    export_to_env,
    reload_config,
    get_all_config,
    generate_config_template,
)

__all__ = [
    "PipelineManager",
    "RetryManager",
    "RetryableErrorType",
    "NonRetryableErrorType",
    "UserConfirm",
    "ConfirmationType",
    "get_config",
    "get_config_bool",
    "get_config_int",
    "get_config_list",
    "require_config",
    "export_to_env",
    "reload_config",
    "get_all_config",
    "generate_config_template",
]

__version__ = "2.0.0"
__author__ = "article-workflow team"