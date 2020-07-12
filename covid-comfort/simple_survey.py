#!/usr/bin/python

import random
import math

MAX_DIST = 10

def generate_random_positions(num):
    positions = []
    distances = []
    for i in range(num):
        while True:
            x = random.randint(-1*MAX_DIST+1, MAX_DIST-1)
            y = random.randint(-1*MAX_DIST+1, MAX_DIST-1)
            if (x, y) not in positions:
                positions.append((x, y))
                distances.append(math.sqrt(x**2 + y**2))
                break
    return positions, distances

def print_simulation(positions):
    print ("\nSIMULATED ENVIRONMENT:\n")
    for y in range(-1*MAX_DIST, MAX_DIST):
        sim_line = ""
        for x in range(-1*MAX_DIST, MAX_DIST):
            spot = (x, y)
            if spot == (0, 0):
                sim_line += " O"
            else:
                sim_line += " X" if spot in positions else " ."
        print(sim_line)
    print ("\n")

# Math functions

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulates positional situations of strangers walking around you in public.')
    parser.add_argument( '--file', action = 'store', type = str, required = True, \
        help = 'File to record responses.')
    args = parser.parse_args()

    while True:
        # Generate positions
        positions, distances = generate_random_positions(random.randint(1,10))
        # Print positions
        print_simulation(positions)
        
        risk_score = input("Rate perceived risk from 1 (feels very safe) to (feels very unsafe):\n")
        while True:
            try:
                risk_score = int(risk_score)
                assert risk_score > 0 and risk_score <= 5
                break
            except:
                risk_score = input("Enter a valid rating.\n")

        # Build feature list
        # Closest Distance, Mean Square, 