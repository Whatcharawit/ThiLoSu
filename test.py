import json

with open("json_payload.json", 'r') as file:
    message = json.load(file)
    file.close()

print(message["values"]["SMU01_Controller"])

dict_ = {
    "a": 1,
    "b": 2
}
print(dict_)

dict_["c"] = {}
print(dict_)