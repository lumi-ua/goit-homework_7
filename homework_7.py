from classes_hw7 import AddressBook, Name, Phone, Birthday, Record

address_book = AddressBook()
address_book_iterator = None


def input_error(func):
    def wrapper(*args):
        result = None
        try:
            result = func(*args) 
        except KeyError:
            print("Enter user name")
        except ValueError:
            print("Give me name and phone please")
        except IndexError:
            print("You entered incorrect data")
        except TypeError:
            print("Wrong input type")
        return result
    return wrapper     


@input_error
def hello(*args):
    return f"How can I help you?"

@input_error
def add(*args):
    global address_book_iterator
    name = args[0]
    number = args[1]
    address_book_iterator = None # грохаем итератор, т.к. после добавления новой записи он станет не валидный.
    if len(args) == 3:
        birthday = args[2]
        address_book.add_record(Record(Name(name), Phone(number), Birthday(birthday)))
        return f"Add success {name} {number} {birthday}"
    else:
        address_book.add_record(Record(Name(name), Phone(number)))
        return f"Add success {name} {number}"
    
@input_error
def change(*args):
    global address_book_iterator
    name = args[0]
    number_from = int(args[1])  #check if number, else generate exception
    number_to = int(args[2])    #check if number, else generate exception
    phone_from = args[1]
    phone_to = args[2]

    record = address_book.search_user(name)
    if record:
        address_book_iterator = None
        record.change_phone(Phone(phone_from), Phone(phone_to))
        return f"Change success {name} {number_from}->{number_to}"
    return f"Change error {name} {number_from}->{number_to}"

@input_error
def phone(*args):
    name = args[0]
    record = address_book.search_user(name)
    if record:
        return str(record)
    return "ERROR empty"

@input_error
def show_all():
    return address_book

@input_error
def good_bye(*args):
    print("Good bye!")
    exit(0)
    return None

@input_error
def no_command(*args):
    return "Unknown command"

@input_error
def show_next(*args):
    global address_book_iterator

    #если итератор валидный - значит можно делать инкремент.
    if address_book_iterator:
        # после инкремента перезаписываем итератор, как результат работы.
        # может стать и не валидным, если вышли за границы. 
        address_book_iterator = next(address_book_iterator)
    else:
        # если не валидный - пересоздаём заново, чтобы итерироваться с начала. 
        address_book_iterator = address_book.iterator()

    # если итератор после инкремента всё ещё валидный, значит можно вернуть строкой.
    if address_book_iterator:
        return str(address_book_iterator)
    return None

@input_error
def rename(*args):
    global address_book_iterator
    if len(args) == 2:
        if address_book.rename_record(args[0], args[1]):
            address_book_iterator = None
            return f'renamed from:{args[0]} to:{args[1]}'
        else: return 'wrong username:{args[0]}'
    return None


COMMANDS = {
    hello: ("hello", "hi"),
    add: ("add", "+"),
    change: ("change", "edit"),
    phone: ("phone", "user"),
    show_all: ("show all", "all"),
    good_bye: ("exit", "close", "end"),
    show_next: ("next",),
    rename: ("rename",)
}

def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data 
    return no_command, None

def main():
    while True:
        user_input = input(">>>")
        command, args = parser(user_input)
        if args != None:
            result = command(*args)
        else:
            result = command()
        
        if result: print(result)

###############################################
if __name__ == "__main__":
    main()
   