import json

with open("foo.txt", "r") as f:
    s = f.readline()


log_data = json.loads(s)
print(log_data)