import os, json

class Json:
    def __init__(self, file: str):
        self.file = file

    def update(self, name:str, value):
        if not os.path.isfile(self.file):
            with open(self.file, "w", encoding="utf-8") as json_file:
                data = dict()
                data[name] = value
                json.dump(data, json_file, indent=4, sort_keys=True)
                json_file.close()
        else:
            with open(self.file, "r", encoding="utf-8") as st_json:
                st_python2 = json.loads(st_json.read())
                st_json.close()
            st_python2[name] = value
            with open(self.file, "w", encoding="utf-8") as json_file:
                json.dump(st_python2, json_file, indent=4, sort_keys=True)
                json_file.close()

    def remove(self, name: str):
        if not os.path.isfile(self.file): raise FileNotFoundError(f"File '{self.file}' does not exist.")
        with open(self.file, "r", encoding="utf-8") as st_json:
            st_python2 = json.loads(st_json.read())
            st_json.close()
        try: del st_python2[name]
        except KeyError: raise KeyError(f"{self.file} does not have a value of '{name}'")
        with open(self.file, "w", encoding="utf-8") as json_file:
            json.dump(st_python2, json_file, indent=4, sort_keys=True)
            json_file.close()

    def get(self, name: str):
        if not os.path.isfile(self.file): raise FileNotFoundError(f"File '{self.file}' does not exist.")
        with open(self.file, "r", encoding="utf-8") as st_json:
            st_python2 = json.loads(st_json.read())
            st_json.close()
        try: data = st_python2[name]
        except KeyError: raise KeyError(f"{self.file} does not have a value of '{name}'")
        return data