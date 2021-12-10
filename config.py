import yaml

config_file = '.env.config.yaml'

with open(config_file) as file:
    content = file.read()
    if not content:
        raise FileNotFoundError('.env.config.yaml is missing')

    config = yaml.load(content, Loader=yaml.SafeLoader)
