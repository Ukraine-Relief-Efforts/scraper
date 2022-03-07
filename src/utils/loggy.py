"""Functionality related to logging."""
import json
import logging
import logging.config
from pathlib import Path


def init_logging():
    """Initialize logging."""
    base_dir = Path(__file__).parent
    sumo_code_path = base_dir / ".sumo-code"
    log_config_path = base_dir / "logConfig.json"

    try:
        sumo_code = sumo_code_path.read_text().strip()
        raw_config = log_config_path.read_text()
        text_config = raw_config.replace('${sumoCode}', sumo_code)
        log_config = json.loads(text_config)
        logging.config.dictConfig(log_config)
    except Exception:
        logging.exception("Could not initialize sumo logging.")
