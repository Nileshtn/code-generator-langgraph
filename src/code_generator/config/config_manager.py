import yaml
import os


def load_config(path:str)->dict:
    with open(path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config

config_folder = r"src/code_generator/config"

prompt  = load_config(os.path.join(config_folder, "prompts.yaml"))
model_config = load_config(os.path.join(config_folder, "config.yaml"))