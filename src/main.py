from yml_reader import load_yml
from random_generator import RandomGenerator
from enum import Enum

class RandomType(Enum):
    DEFINED = 0
    SEED = 1

A = 1140671485
C = 12820163
M = 2124325123

type = RandomType.DEFINED
amount_random_numbers_seed = 0
generate_number = 0

def main(config):
    print(config)

def initial_configuration(config):
    if 'rndnumbers' in config:
        global random_numbers
        random_numbers = config['rndnumbers']
        print(f"Simulating with provided random numbers")
    elif 'rndnumbersPerSeed' in config:
        if len(config['seeds']) != 1:
            print(f"Only one seed is allowed, but multiple seeds were provided: {config['seeds']}")
            exit()
        global amount_random_numbers_seed, type, generate_number
        type = RandomType.SEED
        amount_random_numbers_seed = config['rndnumbersPerSeed']
        seed = config['seeds'][0]
        generator = RandomGenerator(seed, A, C, M)
        generate_number = generator.generate()

if __name__ == "__main__":
    config = load_yml('example.yml')
    initial_configuration(config)
    main(config)