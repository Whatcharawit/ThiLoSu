message = {}
print(message)

battery = {
    "Batt1": {
        "raw_data": 123,
        "status": 1
    }
}

message["values"] = {"key": 11}

print(message)

message["values"].update(battery)
print(message)