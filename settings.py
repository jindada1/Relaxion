import yaml

def load_configuration(file):
    # load config.yml
    f = open(file)
    return yaml.safe_load(f)

def url(prefix, route):
    
    return prefix + route