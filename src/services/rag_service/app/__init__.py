""" Config Loader Script """
import os
import yaml

# Path to the current directory (rag_service/)
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config.yaml")

def load_config(config_file: str = CONFIG_FILE) -> dict:


    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found at {config_file}")

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    return config

# Load config globally so it can be used anywhere
CONFIG = load_config()