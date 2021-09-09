import json
import re


def check_stop_name(x):
    stop_name_split = x.split()
    for name in stop_name_split:
        if not name[0].isupper():
            return 1
    return 1 if x == "" or isinstance(x, str) is False or x[-1:x.rfind(" "):-1][::-1] not in [
        "Road",
        "Avenue",
        "Boulevard",
        "Street"] else 0


buses = json.load(open("bus.json", "r"))
bus_id = stop_id = stop_name = next_stop = stop_type = a_time = 0
for data in buses:
    bus_id += 1 if isinstance(data["bus_id"], int) is False else 0
    stop_id += 1 if isinstance(data["stop_id"], int) is False else 0
    stop_name += check_stop_name(data["stop_name"])
    next_stop += 1 if isinstance(data["next_stop"], int) is False else 0
    stop_type += 1 if data["stop_type"] not in ['S', 'F', 'O', ''] else 0
    a_time += 1 if isinstance(data["a_time"], str) is False or re.match(r"^[0-2][0-9]:[0-5][0-9]$",
                                                                        data["a_time"]) is None else 0

total_errors = bus_id + stop_id + stop_name + next_stop + stop_type + a_time

# Prints if there are any errors
if total_errors > 0:
    print(f"Errors in validation: {total_errors} errors")
    if bus_id > 0: print(f"bus_id: {bus_id}")
    if stop_id > 0: print(f"stop_id: {stop_id}")
    if stop_name > 0: print(f"stop_name: {stop_name}")
    if next_stop > 0: print(f"next_stop: {next_stop}")
    if stop_type > 0: print(f"stop_type: {stop_type}")
    if a_time > 0: print(f"a_time: {a_time}")
    print("\nPlease correct the error(s) and restart the program")
    exit(-1)
else:
    print("All bus data is correctly formatted!")

#  Check number of stops
stop_dict = dict()
street_dict = dict()
time_dict = dict()
on_demand_dict = dict()
starts = set()
finishes = set()
transfers = set()

for data in buses:
    stop_dict.setdefault(data["bus_id"], []).append(data["stop_type"])
    street_dict.setdefault(data["bus_id"], []).append(data["stop_name"])
    time_dict.setdefault(data["bus_id"], []).append([data["a_time"], data["stop_name"]])

    if data["stop_type"] == "O":
        on_demand_dict.setdefault(data["bus_id"], []).append([data["stop_type"], data["stop_name"]])
    if data["stop_type"] == "S":
        starts.add(data["stop_name"])
    elif data["stop_type"] == "F":
        finishes.add(data["stop_name"])

# Check that there is exactly one stop or finish for each line
for data in stop_dict:
    if stop_dict[data].count("S") != 1 or stop_dict[data].count("F") != 1:
        print("ERROR: There is no start or end stop for the line: {}.".format(data))
        break

# List each unique start, transfer, and stop
else:
    for i in range(0, len(street_dict.values()) - 1):
        for j in range(i + 1, len(street_dict.values())):
            transfers.update(set.intersection(set(list(street_dict.values())[i]), set(list(street_dict.values())[j])))

    print("\nStart stops: {} {}".format(len(starts), sorted(starts)))
    print("Transfer stops: {} {}".format(len(transfers), sorted(transfers)))
    print("Finish stops: {} {}\n".format(len(finishes), sorted(finishes)))

    # Check for 'O' stops not being start, transfer, or finish stops
    incorrect = False
    bad_stops = []
    for data in on_demand_dict:
        for i in range(0, len(on_demand_dict[data])):
            if on_demand_dict[data][i][1] in [*starts, *transfers, *finishes]:
                bad_stops.append(on_demand_dict[data][i][1])
                incorrect = True
    if not incorrect:
        print("All 'O' stops are not start, transferring, or finishing stops!")
    else:
        print("WARNING: Wrong 'O' stop type: {}".format(sorted(bad_stops)))

    # Check for increasing times on each bus line
    incorrect = False
    for data in time_dict:
        for i in range(0, len(time_dict[data]) - 1):
            if time_dict[data][i + 1][0] <= time_dict[data][i][0]:
                print("WARNING: This time is not correct at {}: {}".format(data, time_dict[data][i + 1][1]))
                incorrect = True
                break
    if not incorrect:
        print("All times are increasing for each bus line!")
