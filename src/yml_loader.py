import yaml
from typing import TypedDict
from classes.route import Route
from classes.event import Event, EventType
from classes.simulated_queue import Queue

class Config(TypedDict):
    # random_numbers: list[float]
    random_numbers_per_seed: int
    seeds: list[int]
    queues: dict[str, Queue]
    network: list[Route]
    arrivals: list[Event]

class IgnoreUnknown(yaml.SafeLoader):
    pass

def ignore_unknown(loader, tag_suffix, node):
    return loader.construct_mapping(node)

IgnoreUnknown.add_multi_constructor('!', ignore_unknown)

def load_yml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.load(file, Loader=IgnoreUnknown)
    

def load_config(file_path):
    data = load_yml(file_path)
    config: Config = {}

    # Setup seeds and amount of random numbers or random numbers
    if data.get('seeds', None):
        if len(data['seeds']) != 1:
            print(f"Only one seed is allowed, but multiple seeds were provided: {data['seeds']}")
            exit()
        config['seeds'] = data['seeds']
        config['random_numbers_per_seed'] = data['rndnumbersPerSeed']
    # else:
    #     config['random_numbers'] = data['rndnumbers']

    # Setup arrivals
    if 'arrivals' not in data:
        print("No arrivals defined in the configuration.")
        exit()
    config['arrivals'] = []
    for event_name, event_time in data['arrivals'].items():
        config['arrivals'].append(Event(time=event_time, event_type=EventType.ARRIVAL, queue_name=event_name))

    # Setup queues
    if 'queues' not in data:
        print("No queues defined in the configuration.")
        exit()
    config['queues'] = {}
    for queue_name, queue_config in data['queues'].items():
        config['queues'][queue_name] = Queue(
            name=queue_name, 
            servers=queue_config['servers'], 
            capacity=queue_config.get('capacity', float('inf')), 
            min_arrival=queue_config.get('minArrival', -1), 
            max_arrival=queue_config.get('maxArrival', -1),
            min_service=queue_config['minService'], 
            max_service=queue_config['maxService']
        )

    # Setup network
    if 'network' not in data:
        print("No network defined in the configuration.")
        exit()
    config['network'] = []
    for route in data['network']:
        source = route['source']
        target = route['target']
        probability = route['probability']
        config['network'].append(Route(source=source, target=target, probability=probability))

    routes_by_source = {}
    for route in config['network']:
        if route.source not in routes_by_source:
            routes_by_source[route.source] = []
        routes_by_source[route.source].append(route)

    for source, routes in routes_by_source.items():
        total_probability = sum(route.probability for route in routes)
        if total_probability != 1.0:
            routes.append(Route(source=source, target='OUT', probability=round(1.0 - total_probability, 1)))

    config['network'] = [route for routes in routes_by_source.values() for route in routes]

    return config
    

    