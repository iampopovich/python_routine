import json

default_data = {'key':'value'}

def write_test_file(file = 'test_file.json', data = default_data):
	with open(file, 'w') as input_file:
		json.dump(data, input_file)

def upload_data_from_file(file = 'test_file.json'):
	try:
		with open(file, 'r') as output_file:
			data = json.load(output_file)
			return data
	except Exception as ex:
		return ex


def main():
	write_test_file()
	print(upload_data_from_file())

if __name__ == '__main__':
	main()

