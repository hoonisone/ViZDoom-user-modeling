import json

with open("log.txt", "r") as f:
    s = f.readline()


log_data = json.loads(s)
print(log_data)