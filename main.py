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

print(f"Errors in validation: {total_errors} errors")
if bus_id > 0: print(f"bus_id: {bus_id}")
if stop_id > 0: print(f"stop_id: {stop_id}")
if stop_name > 0: print(f"stop_name: {stop_name}")
if next_stop > 0: print(f"next_stop: {next_stop}")
if stop_type > 0: print(f"stop_type: {stop_type}")
if a_time > 0: print(f"a_time: {a_time}")
