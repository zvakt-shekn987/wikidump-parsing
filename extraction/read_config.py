import yaml

def main():

    with open("config.yaml") as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print("Could not read YAML!")
            print(exc)
            exit()

    return conf

conf = main()
    