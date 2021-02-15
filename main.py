import random
import csv


def get_distance(start_point, end_point, city_dictionary):
    current_stop = start_point
    output = 0
    step_counter = 0
    no_go = [""]
    route = [start_point]

    # MOVE FROM START POINT TO END POINT
    while current_stop != end_point:
        possible_options = 0
        possible_destinations = []

        # DETERMINE WHAT POSSIBLE STOPS THERE ARE
        for destination in city_dictionary[current_stop]:
            possible_destinations.append(destination[0])

        # CHECK IF THERE IS A NEW STOP POSSIBLE
        for d in possible_destinations:
            if d not in no_go:
                possible_options += 1

        # RESET WHEN THERE ARE NO OPTIONS
        if possible_options == 0:
            current_stop = start_point
            no_go = [""]
            route = [start_point]

        # WHEN THERE ARE OPTIONS, SELECT ONE
        n = random.randint(0, 4)
        next_stop = city_dictionary[current_stop][n][0]

        # CHECK IF THE STOP HAS NOT PREVIOUSLY BEEN VISITED
        if next_stop not in no_go:
            output += int(city_dictionary[current_stop][n][1])
            no_go.append(start_point)
            current_stop = next_stop
            step_counter += 1
            route.append(next_stop)
    # RETURN THE DATA
    return output, step_counter, route

# OPEN THE FILE AND CREATE DICTIONARY


with open(r"A_ticket_to_ride.csv", "r") as a_ticket_to_ride:
    city_dict = {}
    for row in csv.reader(a_ticket_to_ride, delimiter=";"):
        city_dict[row[0]] = (row[1], row[2]), (row[3], row[4]), (row[5], row[6]), (row[7], row[8]), (row[9], row[10])
# CREATE SOME LIST WHERE WE CAN TRACK THE PROGRESS(route_list) AND THE RESULTS (route_dictionary, min_route)
route_list = []
route_dictionary = {}
min_route = []
# ITERATE THROUGH ALL CITIES TO GO TO ALL CITIES
for start_city in city_dict:
    for end_city in city_dict:
        # FILTER OUT CITIES THAT ARE NEXT TO EACH OTHER, HAVE ALREADY BEEN DONE AND WHERE THE ROUTE WOULD BE A LOOP
        if end_city not in [start_city, city_dict[start_city]] and (end_city, start_city) not in route_list:
            # SET VALUES FOR MINIMUM DISTANCE AND MINIMUM STEPS
            min_distance = 1000
            min_steps = 1000
            # SIMULATE 2000 TIMES
            for iteration in range(2000):
                length, steps, current_route = get_distance(start_city, end_city, city_dict)
                # CHECK IF THE ROUTE IS IMPROVED UPON AND ADJUST THE MINIMA
                if length < min_distance:
                    min_distance = length
                    min_steps = steps
                    min_route = current_route
            # APPEND THE ROUTE TO THE ROUTE_LIST, BOTH WAYS.
            route_list.append((start_city, end_city))
            route_list.append((end_city, start_city))
            # STORE THE DATA IN A DICTIONARY
            route_dictionary[(start_city, end_city)] = (min_distance, min_steps, min_route)
            route_dictionary[(end_city, start_city)] = (min_distance, min_steps, min_route.reverse())
            print("We got this far")
            print("{} to {} completed".format(start_city, end_city))

# SORT THE ROUTE LIST, SO THE DICTIONARY CAN BE READ ALPHABETICALLY
route_list.sort()
# READ THE DICTIONARY
for x in route_list:
    print(x)
    print(route_dictionary[x])
