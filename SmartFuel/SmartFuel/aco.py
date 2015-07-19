from math import radians, cos, sin, sqrt, atan2
import random

def aco(petrol_stations, dist, gas_type, capacity, initial_petrol, overall_dist,
        consumption, source, target, ants=2, a=1, b=1, iterations=10):
    pheromone = {key: 4 for key in petrol_stations.keys()}
    probability = lambda i, feasible, dist: pheromone[i] ** a * h(i, dist) ** b / \
        summation(feasible)
    summation = lambda feasible: sum(pheromone[i] ** a * h(i, dist) ** b
                                     for i in feasible)
    h = lambda i, dist: petrol_stations[i][gas_type] / dist
    solutions = []
    overall_best_sol = None
    overall_cost = float('inf')
    for i in range(iterations):
        best_sol = None
        best_cost = float('inf')
        for j in range(ants):
            sol, cost = construct_solution(source, target, petrol_stations, initial_petrol,
                                    consumption, overall_dist, probability,
                                    capacity, gas_type)
            solutions.append((sol, cost))
            if cost < best_cost:
                best_cost = cost
                best_sol = sol
        if best_cost < overall_cost:
            overall_cost = best_cost
            overall_best_sol = best_sol
        update_pheromone(pheromone, best_sol, best_cost)
    return overall_best_sol, overall_cost


def construct_solution(source, target, petrol_stations, initial_petrol,
                       consumption, overall_dist, probability, capacity,
                       gas_type):
    feasible_dist = initial_petrol * consumption
    dist = calulate_distance(source, target)
    sol = []
    cost = 0.0
    while feasible_dist < dist:
        feasible_stations = get_feasible(source, target, petrol_stations,
                                         feasible_dist, overall_dist)
        p = [probability(feasible_station, len(feasible_stations), dist)
             for feasible_station in feasible_stations]
        choices = sum([[element] * int(weight * 100)for element, weight in zip(feasible_stations, p)], [])
        next_patrol = random.choice(choices)
        quantity = calulate_distance(source, next_patrol) * consumption
        feasible_dist = (capacity - quantity) * consumption
        sol.append({next_patrol: quantity})
        source = next_patrol
        cost += quantity * next_patrol[gas_type]
    return sol, cost


def update_pheromone(pheromone, sol, cost):
    for item in sol.keys():
        pheromone[item] += 1 / cost



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