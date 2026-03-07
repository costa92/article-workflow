#!/usr/bin/env python3
"""
Unified configuration loader for article-workflow plugin.

Priority: Environment variable > plugin local config/config.json > ~/.claude/env.json (backward compat)

Usage:
    from config_loader import get_config
    api_key = get_config("gemini_api_key")
    author = get_config("default_author", "Anonymous")
"""

import os
import json

# Resolve plugin root (parent of shared/)
_PLUGIN_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOCAL_CONFIG = os.path.join(_PLUGIN_ROOT, "config", "config.json")
_CLAUDE_ENV = os.path.expanduser("~/.claude/env.json")

# Mapping: config key -> environment variable name
_ENV_MAP = {
    "gemini_api_key": "GEMINI_API_KEY",
    "wechat_appid": "WECHAT_APPID",
    "wechat_secret": "WECHAT_SECRET",
    "image_api_key": "IMAGE_API_KEY",
    "image_api_base": "IMAGE_API_BASE",
    "default_author": "ARTICLE_AUTHOR",
    "cdn_domain": "CDN_DOMAIN",
    "github_images_repo": "GITHUB_IMAGES_REPO",
    "obsidian_tech_dir": "OBSIDIAN_TECH_DIR",
    "obsidian_publish_dir": "OBSIDIAN_PUBLISH_DIR",
}

_config_cache = None


def _load_json(path):
    """Load a JSON file, return empty dict on failure."""
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _merged_config():
    """Return merged config dict (local config overrides claude env)."""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    base = _load_json(_CLAUDE_ENV)
    local = _load_json(_LOCAL_CONFIG)
    base.update({k: v for k, v in local.items() if v})
    _config_cache = base
    return _config_cache


def get_config(key, default=None):
    """Get a configuration value.

    Priority: environment variable > config files > default
    Placeholder values (starting with 'your-') are treated as unset.
    """
    env_var = _ENV_MAP.get(key, key.upper())
    val = os.environ.get(env_var)
    if val:
        return val

    cfg = _merged_config()
    val = cfg.get(key, "")
    if val and not str(val).startswith("your-"):
        return val

    return default


def require_config(key):
    """Get a configuration value or raise ValueError if missing."""
    val = get_config(key)
    if not val:
        env_var = _ENV_MAP.get(key, key.upper())
        raise ValueError(
            f"Missing required config '{key}'. Set it via:\n"
            f"  1. Environment variable: export {env_var}=value\n"
            f"  2. Plugin config: config/config.json (key: {key})\n"
            f"  3. Claude env: ~/.claude/env.json (key: {key})"
        )
    return val


def export_to_env(*keys):
    """Export config values to os.environ so subprocesses can access them."""
    for key in keys:
        val = get_config(key)
        if val:
            env_var = _ENV_MAP.get(key, key.upper())
            os.environ[env_var] = val


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
