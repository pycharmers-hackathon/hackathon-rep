from math import radians, cos, sin, sqrt, atan2
import random

def aco(petrol_stations, dist, gas_type, capacity, initial_petrol, overall_dist,
        consumption, source, target, ants=2, a=1, b=1, iterations=10):
    pheromone = {key: 4 for key in petrol_stations.keys()}
    first_iter = 0
    rest_petrol = initial_petrol
    probability = lambda i, feasible, dist: pheromone[i] ** a * h(i, dist) ** b / \
        summation(feasible)
    summation = lambda feasible: sum(pheromone[i] ** a * h(i, dist) ** b
                                     for i in feasible)
    h = lambda i, dist: petrol_stations[i][gas_type] / dist
    for i in range(iterations):
        for j in range(ants):
            feasible_dist = rest_petrol * consumption
            feasible_stations = get_feasible(source, target, petrol_stations,
                                             feasible_dist, overall_dist)
            number = len(feasible_stations)
            for feasible_station in feasible_stations:
                p = {feasible_station: probability(feasible_station, number, dist)}
                choices = sum([[element] * int(weight * 100)for element, weight in zip(elements, weights)], [])
                random.choice(choices)

def calulate_distance(source, target):
    R = 3673.0
    source_lat = radians(source[0])
    source_lng = radians(source[1])
    target_lat = radians(target[0])
    target_lng = radians(target[1])

    dist_lat = target_lat - source_lat
    dist_lng = target_lng - source_lng

    a = sin(dist_lat / 2) ** 2 + cos(source_lat) * cos(target_lat) * sin(dist_lng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def get_feasible(source, target, petrol_stations, feasible_dist, overall_dist):
    accepted = []
    for petrol_station in petrol_stations:
        dist1 = calulate_distance(source, petrol_station['location'])
        dist2 = calulate_distance(petrol_station['location'], target)
        if dist2 > overall_dist:
            continue
        if dist1 <= feasible_dist:
            accepted.append(petrol_station['id'])
    return accepted