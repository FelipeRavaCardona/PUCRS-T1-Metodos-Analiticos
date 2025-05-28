import heapq
from yml_loader import load_config, Config
from classes.random_generator import RandomGenerator
from classes.event import Event, EventType
from classes.simulated_queue import Queue
from tabulate import tabulate

random_numbers_per_seed = 0
generate = None
global_time = 0.0

scheduler: list[Event] = []

# def generate_random_numbers(seed, amount):
#     global random_numbers
#     generator = RandomGenerator(seed)
#     gen = generator.generate()
#     for _ in range(amount):
#         random_numbers.append(next(gen))

def next_random():
    return next(generate)

def next_uniform(min_value, max_value):
    return min_value + (max_value - min_value) * next_random()

def simulate(config: Config):
    global scheduler
    scheduler = config['arrivals']
    heapq.heapify(scheduler)
    for _ in range(random_numbers_per_seed):
        event: Event = heapq.heappop(scheduler)
        if event.type == EventType.ARRIVAL:
            arrival_event(event)
        elif event.type == EventType.EXIT:
            exit_event(event)
        else:
            pass_event(event)
    
    for queue_name, queue_data in config['queues'].items():
        generate_report(queue_data)

def accumulate_time(event: Event, queues: dict[str, Queue]):
    global global_time, config
    for queue_name, queue_data in queues.items():
        queue_data.times[queue_data.status] += event.time - global_time
    global_time = event.time 

def arrival_event(event: Event):
    queue = config['queues'][event.queue_name]
    accumulate_time(event, config['queues'])
    if queue.status < queue.capacity:
        queue.customer_in()
        if queue.status <= queue.servers:
            target_name = exit_or_pass(queue)

            if target_name == 'OUT':
                schedule_event(queue, EventType.EXIT)
            else:
                schedule_event(queue, EventType.PASS, target_name)
    else:
        queue.customer_lost()
    schedule_event(queue, EventType.ARRIVAL)


def exit_event(event: Event):
    queue = config['queues'][event.queue_name]
    accumulate_time(event, config['queues'])
    queue.customer_out()
    if queue.status >= queue.servers:
        target_name = exit_or_pass(queue)

        if target_name == 'OUT':
            schedule_event(queue, EventType.EXIT)
        else:
            schedule_event(queue, EventType.PASS, target_name)

def pass_event(event: Event):
    queue = config['queues'][event.queue_name]
    target_queue = config['queues'][event.target_name]
    accumulate_time(event, config['queues'])
    queue.customer_out()
    # Iniciar Servico de um cliente na fila
    if queue.status >= queue.servers:
        target_name = exit_or_pass(queue)

        if target_name == 'OUT':
            schedule_event(queue, EventType.EXIT)
        else:
            schedule_event(queue, EventType.PASS, target_name)
    # Adiciona cliente na fila target ou perde o cliente
    if target_queue.status < target_queue.capacity:
        target_queue.customer_in()
        # Iniciar servico de um cliente na fila
        if target_queue.status <= target_queue.servers:
            target_name = exit_or_pass(target_queue)

            if target_name == 'OUT':
                schedule_event(target_queue, EventType.EXIT)
            else:
                schedule_event(target_queue, EventType.PASS, target_name)
    else:
        target_queue.customer_lost()

def exit_or_pass(queue: Queue):
    summed_probability = 0.0
    random_number = next_random()
    for route in queue.routes:
        summed_probability += route.probability
        if random_number < summed_probability:
            return route.target

def schedule_event(queue: Queue, type: EventType, target: str = None):
    global scheduler, global_time
    time_needed = None
    if type == EventType.ARRIVAL:
        time_needed = next_uniform(queue.min_arrival, queue.max_arrival)
    else:
        time_needed = next_uniform(queue.min_service, queue.max_service)
    event = Event(time_needed + global_time, type, queue.name, target)
    heapq.heappush(scheduler, event)

def generate_report(queue):
    print(f"Queue: {queue.name} - Configuration: (G/G/{queue.servers}/{queue.capacity})")
    if queue.min_arrival != 0 and queue.max_arrival != 0:
        print(f"Arrival: {queue.min_arrival} ... {queue.max_arrival}")
    print(f"Service: {queue.min_service} ... {queue.max_service}")
    print('*' * 50)

    total_time = sum(queue.times)
    rows = []
    for state, time_in_state in enumerate(queue.times):
        if time_in_state > 0:
            prob = (time_in_state / total_time) * 100 if total_time > 0 else 0
            rows.append([state, f"{time_in_state:.4f}", f"{prob:.2f}%"])

    print(tabulate(rows, headers=['State', 'Time', 'Probability'], tablefmt='orgtbl'))
    print(f"\nNumber of losses: {queue.losses}")
    print('=' * 50 + '\n')

if __name__ == "__main__":
    config = load_config('model.yml')
    if 'seeds' in config:
        random_numbers_per_seed = config['random_numbers_per_seed']
        generator = RandomGenerator(config['seeds'][0])
        generate = generator.generate()
        # generate_random_numbers(config['seeds'][0], config['random_numbers_per_seed'])
    # else:
    #     random_numbers = config['random_numbers']
    for queue_name, queue_data in config['queues'].items():
        for route in config['network']:
            if queue_name == route.source:
                queue_data.routes.append(route)
        queue_data.routes = sorted(queue_data.routes, key=lambda obj: obj.probability) 
    print(f"Simulating with random numbers generated with seed {config['seeds'][0]}")
    simulate(config)
    