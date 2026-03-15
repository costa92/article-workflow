#!/usr/bin/env python3
"""
Unified configuration loader for article-workflow plugin.

支持多级配置管理：
1. 环境变量 (最高优先级)
2. 本地配置文件 config/config.json
3. 全局配置文件 ~/.claude/env.json (向后兼容)
4. 默认值

支持高级特性：
- 类型转换 (字符串/数字/布尔值)
- 配置验证
- YAML配置文件支持
- .env文件支持
- 配置模板生成

Usage:
    from config_loader import get_config, require_config, get_config_bool, export_to_env
    api_key = get_config("gemini_api_key")
    author = get_config("default_author", "Anonymous")
    debug_mode = get_config_bool("debug_mode", False)
    # 配置验证
    require_config("gemini_api_key")
"""

import os
import json
import yaml
from typing import Any, Optional, Union, Dict, List
from pathlib import Path

# Resolve plugin root (parent of shared/)
_PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOCAL_CONFIG = os.path.join(_PLUGIN_ROOT, "config", "config.json")
_LOCAL_CONFIG_YAML = os.path.join(_PLUGIN_ROOT, "config", "config.yaml")
_LOCAL_DOTENV = os.path.join(_PLUGIN_ROOT, ".env")
_CLAUDE_ENV = os.path.expanduser("~/.claude/env.json")

# Mapping: config key -> environment variable name
_ENV_MAP = {
    # API配置
    "gemini_api_key": "GEMINI_API_KEY",
    "wechat_appid": "WECHAT_APPID", 
    "wechat_secret": "WECHAT_SECRET",
    "image_api_key": "IMAGE_API_KEY",
    "image_api_base": "IMAGE_API_BASE",
    
    # 内容配置
    "default_author": "ARTICLE_AUTHOR",
    "default_category": "ARTICLE_CATEGORY",
    "default_tags": "ARTICLE_TAGS",
    
    # 发布配置
    "cdn_domain": "CDN_DOMAIN",
    "github_images_repo": "GITHUB_IMAGES_REPO",
    
    # 路径配置
    "obsidian_tech_dir": "OBSIDIAN_TECH_DIR",
    "obsidian_publish_dir": "OBSIDIAN_PUBLISH_DIR",
    "output_dir": "ARTICLE_OUTPUT_DIR",
    "temp_dir": "ARTICLE_TEMP_DIR",
    
    # 流水线配置
    "max_retry_count": "ARTICLE_MAX_RETRY",
    "review_score_threshold": "REVIEW_SCORE_THRESHOLD",
    "enable_debug": "ARTICLE_WORKFLOW_DEBUG",
    "log_level": "ARTICLE_LOG_LEVEL",
    
    # 高级配置
    "timeout_seconds": "ARTICLE_TIMEOUT_SECONDS",
    "max_concurrent_tasks": "MAX_CONCURRENT_TASKS",
    "cache_enabled": "ARTICLE_CACHE_ENABLED",
    "cache_ttl_hours": "ARTICLE_CACHE_TTL_HOURS",
}

# 配置验证规则
_VALIDATION_RULES = {
    "gemini_api_key": lambda v: v and len(v) > 20,
    "wechat_appid": lambda v: v and len(v) == 18,
    "wechat_secret": lambda v: v and len(v) == 32,
    "review_score_threshold": lambda v: 0 <= int(v) <= 100,
    "max_retry_count": lambda v: 0 <= int(v) <= 10,
    "timeout_seconds": lambda v: int(v) > 0,
    "max_concurrent_tasks": lambda v: 1 <= int(v) <= 20,
}

# 默认值
_DEFAULT_VALUES = {
    "default_author": "Anonymous",
    "default_category": "技术",
    "default_tags": "技术,AI,编程",
    "max_retry_count": 3,
    "review_score_threshold": 55,
    "timeout_seconds": 300,
    "max_concurrent_tasks": 5,
    "enable_debug": False,
    "log_level": "INFO",
    "cache_enabled": True,
    "cache_ttl_hours": 24,
}

_config_cache = None
_dotenv_cache = None


def _load_json(path: str) -> Dict[str, Any]:
    """Load a JSON file, return empty dict on failure."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Failed to load JSON config {path}: {e}")
        return {}


def _load_yaml(path: str) -> Dict[str, Any]:
    """Load a YAML file, return empty dict on failure."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"Warning: Failed to load YAML config {path}: {e}")
        return {}


def _load_dotenv(path: str) -> Dict[str, str]:
    """Load .env file, return dict of key-value pairs."""
    global _dotenv_cache
    if _dotenv_cache is not None:
        return _dotenv_cache
    
    if not os.path.exists(path):
        _dotenv_cache = {}
        return _dotenv_cache
    
    try:
        result = {}
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    result[key.strip()] = value.strip().strip('"\'')
        _dotenv_cache = result
        return result
    except Exception as e:
        print(f"Warning: Failed to load .env file {path}: {e}")
        return {}


def _merged_config() -> Dict[str, Any]:
    """Return merged config dict with priority order."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    # 1. 默认值
    config = _DEFAULT_VALUES.copy()
    
    # 2. 全局配置文件 (~/.claude/env.json)
    claude_config = _load_json(_CLAUDE_ENV)
    config.update({k: v for k, v in claude_config.items() if v is not None})
    
    # 3. 本地YAML配置文件
    yaml_config = _load_yaml(_LOCAL_CONFIG_YAML)
    config.update({k: v for k, v in yaml_config.items() if v is not None})
    
    # 4. 本地JSON配置文件
    json_config = _load_json(_LOCAL_CONFIG)
    config.update({k: v for k, v in json_config.items() if v is not None})
    
    # 5. .env文件
    dotenv_config = _load_dotenv(_LOCAL_DOTENV)
    # 将.env中的键转换为小写（标准做法）
    for key, value in dotenv_config.items():
        config_key = key.lower()
        if config_key in config or value:
            config[config_key] = value
    
    _config_cache = config
    return config


def _validate_config(key: str, value: Any) -> bool:
    """Validate a configuration value."""
    if key in _VALIDATION_RULES:
        try:
            return _VALIDATION_RULES[key](value)
        except Exception:
            return False
    return True


def _convert_value(value: Any, expected_type: Optional[str] = None) -> Any:
    """Convert value to appropriate type."""
    if value is None:
        return None
    
    if isinstance(value, str):
        # 处理布尔值
        if value.lower() in ("true", "yes", "1", "on"):
            return True
        elif value.lower() in ("false", "no", "0", "off"):
            return False
        
        # 处理数字
        try:
            if "." in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # 处理列表（逗号分隔）
        if "," in value:
            return [item.strip() for item in value.split(",")]
    
    return value


def get_config(key: str, default: Any = None, validate: bool = True) -> Any:
    """Get a configuration value.

    Args:
        key: Configuration key
        default: Default value if not found
        validate: Whether to validate the value
    
    Returns:
        Configuration value, converted to appropriate type
    
    Priority:
        1. Environment variable
        2. .env file
        3. Local config files (YAML > JSON)
        4. Global config file (~/.claude/env.json)
        5. Default value
    """
    # 检查环境变量
    env_var = _ENV_MAP.get(key, key.upper())
    env_val = os.environ.get(env_var)
    if env_val is not None:
        val = _convert_value(env_val)
        if validate and not _validate_config(key, val):
            print(f"Warning: Invalid value for {key} from environment variable: {env_val}")
            return default if default is not None else env_val
        return val
    
    # 检查. env文件
    dotenv_config = _load_dotenv(_LOCAL_DOTENV)
    dotenv_val = dotenv_config.get(env_var) or dotenv_config.get(key.upper()) or dotenv_config.get(key.lower())
    if dotenv_val is not None:
        val = _convert_value(dotenv_val)
        if validate and not _validate_config(key, val):
            print(f"Warning: Invalid value for {key} from .env file: {dotenv_val}")
            return default if default is not None else dotenv_val
        return val
    
    # 检查配置文件
    cfg = _merged_config()
    cfg_val = cfg.get(key)
    if cfg_val is not None and cfg_val != "":
        val = _convert_value(cfg_val)
        if validate and not _validate_config(key, val):
            print(f"Warning: Invalid value for {key} from config file: {cfg_val}")
            return default if default is not None else cfg_val
        return val
    
    return default


def get_config_bool(key: str, default: bool = False) -> bool:
    """Get a boolean configuration value."""
    val = get_config(key, default, validate=False)
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return bool(val)
    if isinstance(val, str):
        return val.lower() in ("true", "yes", "1", "on", "enabled")
    return bool(val)


def get_config_int(key: str, default: int = 0) -> int:
    """Get an integer configuration value."""
    val = get_config(key, default, validate=False)
    if isinstance(val, (int, float)):
        return int(val)
    if isinstance(val, str):
        try:
            return int(val)
        except ValueError:
            return default
    return default


def get_config_list(key: str, default: Optional[List[str]] = None) -> List[str]:
    """Get a list configuration value."""
    default = default or []
    val = get_config(key, default, validate=False)
    if isinstance(val, list):
        return val
    if isinstance(val, str):
        if "," in val:
            return [item.strip() for item in val.split(",")]
        return [val]
    return default


def require_config(key: str, validate: bool = True) -> Any:
    """Get a configuration value or raise ValueError if missing."""
    val = get_config(key, validate=validate)
    if not val:
        env_var = _ENV_MAP.get(key, key.upper())
        sources = [
            f"1. Environment variable: export {env_var}=value",
            f"2. .env file: {_LOCAL_DOTENV}",
            f"3. YAML config: {_LOCAL_CONFIG_YAML}",
            f"4. JSON config: {_LOCAL_CONFIG}",
            f"5. Global config: {_CLAUDE_ENV}"
        ]
        raise ValueError(
            f"Missing required configuration: '{key}'\n"
            f"Set it via one of these methods:\n" + "\n".join(sources)
        )
    return val


def export_to_env(*keys: str) -> None:
    """Export config values to os.environ so subprocesses can access them."""
    for key in keys:
        val = get_config(key, validate=False)
        if val is not None:
            env_var = _ENV_MAP.get(key, key.upper())
            os.environ[env_var] = str(val)


def reload_config() -> None:
    """Reload configuration from all sources."""
    global _config_cache, _dotenv_cache
    _config_cache = None
    _dotenv_cache = None
    _merged_config()


def get_all_config() -> Dict[str, Any]:
    """Get all configuration values."""
    return _merged_config().copy()


def generate_config_template(output_path: Optional[str] = None) -> str:
    """Generate a configuration template with all available options."""
    template = {
        "api": {
            "gemini_api_key": "your-gemini-api-key-here",
            "wechat_appid": "your-wechat-appid",
            "wechat_secret": "your-wechat-secret",
            "image_api_key": "your-image-api-key",
            "image_api_base": "https://api.example.com",
        },
        "content": {
            "default_author": "Anonymous",
            "default_category": "技术",
            "default_tags": ["技术", "AI", "编程"],
        },
        "paths": {
            "obsidian_tech_dir": "path/to/obsidian/tech",
            "obsidian_publish_dir": "path/to/obsidian/publish",
            "output_dir": "output",
            "temp_dir": "temp",
        },
        "pipeline": {
            "max_retry_count": 3,
            "review_score_threshold": 55,
            "timeout_seconds": 300,
            "max_concurrent_tasks": 5,
        },
        "debug": {
            "enable_debug": False,
            "log_level": "INFO",
        },
        "cache": {
            "cache_enabled": True,
            "cache_ttl_hours": 24,
        }
    }
    
    if output_path:
        if output_path.endswith(".yaml") or output_path.endswith(".yml"):
            with open(output_path, "w", encoding="utf-8") as f:
                yaml.dump(template, f, default_flow_style=False, allow_unicode=True, indent=2)
        else:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(template, f, ensure_ascii=False, indent=2)
    
    return json.dumps(template, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print("article-workflow config loader")
    print(f"  Plugin root: {_PLUGIN_ROOT}")
    print(f"  Local config: {_LOCAL_CONFIG} ({'exists' if os.path.exists(_LOCAL_CONFIG) else 'not found'})")
    print(f"  Claude env: {_CLAUDE_ENV} ({'exists' if os.path.exists(_CLAUDE_ENV) else 'not found'})")
    print()
    for key in _ENV_MAP:
        val = get_config(key)
        if val:
            display = val[:8] + "..." if len(val) > 12 else val
            print(f"  {key}: {display}")
        else:
            print(f"  {key}: (not set)")
