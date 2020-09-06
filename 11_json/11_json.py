import json

default_data = {
    "president": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian"
    }
}


def write_test_file(file='test_file.json', data=default_data):
    with open(file, 'w') as input_file:
        json.dump(data, input_file)


def upload_data_from_file(file='test_file.json'):
    try:
        with open(file, 'r') as output_file:
            data = json.load(output_file)
            return data
    except Exception as ex:
        return ex


def show_data_prettify(data=default_data, indents=4):
    return json.dumps(data, indent=indents)


def main():
    write_test_file()
    print(upload_data_from_file())
    print(show_data_prettify())
    print(show_data_prettify(indents=1))


if __name__ == '__main__':
    main()
