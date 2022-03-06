"""Functionality related to logging."""
import json
import logging
from pathlib import Path


def init_logging():
    """Initialize logging."""
    base_dir = Path(__file__).parent
    sumo_secrets_path = base_dir / ".sumo-code"
    log_config_path = base_dir / "logConfig.json"

    try:
        with open(sumo_secrets_path, 'r') as sumo_file:
            sumo_secrets = sumo_file.read().strip()
        with open(log_config_path, 'r') as log_file:
            log_config = log_file.read().strip()

        log_config = log_config.replace("${sumoCode}", sumo_secrets["sumoCode"])
        logging.config.dictConfig(log_config)
    except Exception:
        logging.exception("Could not initialize sumo logging.")
