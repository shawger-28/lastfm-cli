import os
import configparser
from pathlib import Path


CONFIG_PATH = Path.home() / ".config" / "lastfm" / "config"
DEFAULT_LIMIT = 5


class ConfigError(Exception):
    """Raised when config is invalid or missing."""
    pass


def load_config():
    config = {}

    # 1. Load from environment variables first
    env_username = os.getenv("LASTFM_USERNAME")
    env_api_key = os.getenv("LASTFM_API_KEY")
    env_limit = os.getenv("LASTFM_LIMIT")

    if env_username:
        config["username"] = env_username.strip()

    if env_api_key:
        config["api_key"] = env_api_key.strip()

    if env_limit:
        try:
            config["default_limit"] = int(env_limit)
        except ValueError:
            raise ConfigError("LASTFM_LIMIT must be an integer")

    # 2. Load from config file if needed
    if CONFIG_PATH.exists():
        parser = configparser.ConfigParser()

        try:
            parser.read(CONFIG_PATH)
        except Exception as e:
            raise ConfigError(f"Failed to read config file: {e}")

        if "lastfm" not in parser:
            raise ConfigError("Config file is missing [lastfm] section")

        section = parser["lastfm"]

        if "username" not in config and "username" in section:
            config["username"] = section.get("username", "").strip()

        if "api_key" not in config and "api_key" in section:
            config["api_key"] = section.get("api_key", "").strip()

        if "default_limit" not in config and "default_limit" in section:
            try:
                config["default_limit"] = section.getint("default_limit")
            except ValueError:
                raise ConfigError("default_limit must be an integer")

    # 3. Apply defaults
    if "default_limit" not in config:
        config["default_limit"] = DEFAULT_LIMIT

    # 4. Validate required fields
    if not config.get("username"):
        raise ConfigError(
            "Missing username.\n"
            "Set LASTFM_USERNAME or create ~/.config/lastfm/config"
        )

    if not config.get("api_key"):
        raise ConfigError(
            "Missing API key.\n"
            "Set LASTFM_API_KEY or create ~/.config/lastfm/config"
        )

    return config
