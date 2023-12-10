import json
import os


class AttrMap:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.__dict__, f, indent=4)

a = {
    "a_w": "John",
    "a_s": 30,
    "a_e": "New York"
}

fp = open("out.json", "w")
am = AttrMap(**a)
am.save("out2.json")
# run os to run the executable with the json file as an argument
a = os.system("telemetry.exe out2.json")
print(a)


