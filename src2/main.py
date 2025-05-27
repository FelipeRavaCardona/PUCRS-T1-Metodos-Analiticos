from queue_network import QueueNetwork, Networking
from simulated_queue import Queue
from yml_reader import load_yml

def initial_configuration(config):
    if len(config['seeds']) != 1:
        print(f"Only one seed is allowed, but multiple seeds were provided: {config['seeds']}")
        exit()
    seed = config['seeds'][0]
    events = config['rndnumbersPerSeed']
    
    if 'queues' not in config:
        print("No queues defined in the configuration.")
        exit()
    first_arrival = config['arrivals']['Q1']

    queues = []

    for queue_name, queue_config in config['queues'].items():
        queues.append(Queue(
                name= queue_name, 
                servers= queue_config['servers'], 
                capacity= queue_config.get('capacity', float('inf')), 
                min_arrival= queue_config.get('minArrival', 0), 
                max_arrival= queue_config.get('maxArrival', 0),
                min_service= queue_config['minService'], 
                max_service= queue_config['maxService']))

    network = {}

    for relation in config['network']:
        source = relation['source']
        target = relation['target']
        probability = relation['probability']
        if source not in network:
            network[source] = []
        network[source].append(Networking(target, probability))

    return seed, first_arrival, queues, network

if __name__ == "__main__":
    config = load_yml('model.yml')
    seed, first_arrival, queues, network = initial_configuration(config)
    queue_network = QueueNetwork(seed, first_arrival)

    queue_network.queues = queues
    queue_network.network = network

    print(queue_network)