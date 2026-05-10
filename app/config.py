import json
import os
from pathlib import Path

CONFIG_FILE = Path(os.environ.get("CLINIC_CONFIG_PATH", "db_config.json"))


def get_config() -> dict | None:
    """Load database configuration from file."""
    if not CONFIG_FILE.exists():
        return None
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(server: str, username: str, password: str) -> None:
    """Save database configuration to file."""
    config = {
        "server": server,
        "database": "hospimag",
        "username": username,
        "password": password,
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def is_configured() -> bool:
    """Check if database connection is configured."""
    return CONFIG_FILE.exists()
