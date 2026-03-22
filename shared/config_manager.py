#!/usr/bin/env python3
"""
ConfigManager class for article-workflow plugin.

This class provides an object-oriented interface to the configuration system,
compatible with the existing functional API.
"""

import os
import json
import yaml
from typing import Any, Dict, Optional, Union
from pathlib import Path

from config_loader import (
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


class ConfigManager:
    """Configuration manager with object-oriented interface."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self._config_cache = None
        self._config_paths = []
        
    def load_config(self) -> bool:
        """
        Load configuration from all sources.
        
        Returns:
            bool: True if configuration loaded successfully
        """
        # This is a no-op in the functional API, but we keep it for compatibility
        self._config_cache = get_all_config()
        return True
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return get_config(key, default)
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        Get configuration value as boolean.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value as boolean
        """
        return get_config_bool(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        Get configuration value as integer.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value as integer
        """
        return get_config_int(key, default)
    
    def get_list(self, key: str, default: list = None) -> list:
        """
        Get configuration value as list.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value as list
        """
        if default is None:
            default = []
        return get_config_list(key, default)
    
    def require(self, key: str) -> Any:
        """
        Get required configuration value.
        
        Args:
            key: Configuration key
            
        Returns:
            Configuration value
            
        Raises:
            ValueError: If configuration key is not found
        """
        return require_config(key)
    
    def export_to_env(self, *keys: str) -> None:
        """
        Export configuration values to environment variables.
        
        Args:
            *keys: Configuration keys to export
        """
        export_to_env(*keys)
    
    def reload(self) -> None:
        """Reload configuration from all sources."""
        reload_config()
        self._config_cache = get_all_config()
    
    def get_all(self) -> Dict[str, Any]:
        """
        Get all configuration values.
        
        Returns:
            Dictionary of all configuration values
        """
        return get_all_config()
    
    def generate_template(self) -> Dict[str, Any]:
        """
        Generate configuration template.
        
        Returns:
            Configuration template
        """
        return generate_config_template()
    
    def save_to_file(self, path: Union[str, Path], format: str = "json") -> bool:
        """
        Save current configuration to file.
        
        Args:
            path: File path
            format: File format ("json" or "yaml")
            
        Returns:
            bool: True if saved successfully
        """
        try:
            config_data = self.get_all()
            with open(path, 'w', encoding='utf-8') as f:
                if format.lower() == "yaml":
                    yaml.dump(config_data, f, allow_unicode=True, default_flow_style=False)
                else:
                    json.dump(config_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存配置文件失败: {e}")
            return False
    
    def __getitem__(self, key: str) -> Any:
        """Get configuration value using dictionary syntax."""
        return self.get(key)
    
    def __contains__(self, key: str) -> bool:
        """Check if configuration key exists."""
        try:
            value = self.get(key)
            return value is not None
        except ValueError:
            return False


# Alias for backward compatibility
ConfigLoader = ConfigManager