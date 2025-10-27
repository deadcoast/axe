"""
Configuration management for AXE CLI
Handles persistent settings using JSON
"""

import json
from pathlib import Path
from typing import Any, Optional


class Config:
    """Manages configuration settings for AXE CLI"""
    
    def __init__(self):
        """Initialize configuration manager"""
        self.config_dir = Path.home() / '.axe_cli'
        self.config_file = self.config_dir / 'config.json'
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._config = self._load()
    
    def _load(self) -> dict:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._default_config()
        return self._default_config()
    
    def _default_config(self) -> dict:
        """Return default configuration"""
        return {
            'input_path': str(Path.cwd()),
            'output_path': str(Path.cwd() / 'axe_output'),
            'default_format': 'markdown',
            'version': '1.0.0'
        }
    
    def _save(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self._config, f, indent=2)
        except IOError as e:
            raise RuntimeError(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        self._config[key] = value
        self._save()
    
    def get_all(self) -> dict:
        """Get all configuration values
        
        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()
    
    def reset(self):
        """Reset configuration to defaults"""
        self._config = self._default_config()
        self._save()