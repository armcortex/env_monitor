import ujson


def read_json(fpath):
    with open(fpath, 'r') as f:
        config = ujson.loads(f.read())
    return config

CONFIG = read_json('./config.json')

