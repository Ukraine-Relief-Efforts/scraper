"""Functionality related to logging."""
from asyncore import file_dispatcher
import json
import logging
from pathlib import Path


def init_logging():
    """Initialize logging."""
    base_dir = Path(__file__).parent
    sumo_secrets_path = base_dir / ".sumo-code.json"
    log_config_path = base_dir / "logConfig.json"
    sumo_secrets = ""
    log_config = ""

    print("Sumo Secrets Path: " + sumo_secrets_path)
    print("Log Config Path: " + log_config_path)

    try:
        sumo_secrets = json.loads(sumo_secrets_path.read_text())
        log_config = json.loads(log_config_path.read_text())
        log_config = log_config.replace("${sumoCode}", sumo_secrets["sumoCode"])
        logging.config.dictConfig(log_config)
    except Exception:
        logging.exception("Could not initialize sumo logging.")
