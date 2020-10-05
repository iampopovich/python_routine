import json #для записи в файл 

persons = []

def add_person():
    name = input("Type name: ")
    surname = input("Type surname: ")
    middle_name = input("Type middle name: ")
    fullname = name + ' ' + middle_name + ' ' + surname
    birth_date = input("Type birthdate: ")
    phone_number = input("Type contact phone number: ")
    person = {'name':fullname, 'DOB':birth_date, 'phone':phone_number}
    global persons
    persons.append(person)

def list_all_persons():
    #сделай сама
    pass

def search_by_name():
    #сделай сама
    pass

def search_by_number():
    #сделай сама
    pass

def remove_person():
    #сделай сама
    pass

def main():
    print("Address book v1.0")
    d = int(input("Type command"
        "0 - добавить контакт"
        "1 - просмотр контактов"
        "2 - поиск по имени"
        "3 - поиск по номеру"
        "4 - удалить контакт"))
    if d == 0:
        add_person()
    if d == 1:
        list_all_persons()
    if d == 2:
        search_by_name()
    if d == 3:
        search_by_number()
    if d == 4:
        remove_person()

if __name__ == '__main__':
    main()
