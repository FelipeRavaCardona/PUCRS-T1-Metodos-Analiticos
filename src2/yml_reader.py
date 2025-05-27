import yaml

class IgnoreUnknown(yaml.SafeLoader):
    pass

def ignore_unknown(loader, tag_suffix, node):
    return loader.construct_mapping(node)

IgnoreUnknown.add_multi_constructor('!', ignore_unknown)

def load_yml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.load(file, Loader=IgnoreUnknown)