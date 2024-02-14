import json
from prettytable import PrettyTable


class PhoneBook:
    """

    Программа имитирует работу телефонного справочника. Контакты хранятся в отдельном файле в формате .json.
    Необходимо создать экземпляр класса PhoneBook и передать в него при создании путь до json-файла с контактами.

    Справочник выдает в консоль контакты, оформленные в таблицу по 10 штук на странице.

    Для корректной работы требуется установить библиотеку  prettytable

    """

    def __init__(self, repo_file_path: str):
        self.repo_file_name = repo_file_path
        self._limit = 0
        self._offset = 11
        self.page = 1

    # Создание таблицы для вывода контактов
    @staticmethod
    def to_display():
        to_display = PrettyTable()
        to_display.field_names = ["Имя", "Фамилия", "Отчество",
                                  "Наименование организации", "Рабочий номер", "Личный номер"]
        return to_display

    # Логика чтения и переписывания справочника
    def open_phonebook(self):
        with open(self.repo_file_name, 'r') as phone_book:
            json_book = phone_book.read()
            contacts = json.loads(json_book)
            return contacts

    def change_phonebook(self, new_data):
        with open(self.repo_file_name, 'w') as phone_book_v:
            phone_book_v.write(new_data)

    def page_forward(self):
        """Перелистнуть на страницу вперед"""
        self.page += 1
        self._limit += 10
        self._offset += 10
        self.read()

    def page_backward(self):
        """Перелистнуть на страницу назад"""
        if self._limit <= 1 or self._limit <= 11:
            self._limit = 0
            self._offset = 11
            self.page = 1
        else:
            self.page -= 1
            self._limit -= 10
            self._offset -= 10
            self.read()

    def read(self):
        """Вывести в консоль текущую страницу"""
        contacts = self.open_phonebook()
        if self._offset > len(contacts):
            self._offset = len(contacts)
        if self._limit > len(contacts):
            return print(f"There is no contacts at page №{self.page}")
        to_display = self.to_display()
        for row in contacts[self._limit:self._offset]:
            to_display.add_row(list(row.values()))
        print(f"Page {self.page}")
        print(to_display)

    def create(self, contact: dict):
        """
        create(contact: dict) -
        Создать контакт. В качестве аргумента принимает словарь,
        в котором передаются соответствующие значения по ключам.

        Словарь вида:
        {
        "name": str, "lastname": str, "surname": str, "organization": str,
        "work_phone_number": str|int, "personal_number": str|int
        }
        """
        contacts = self.open_phonebook()
        contacts.append(contact)
        new_json = json.dumps(contacts, indent=4)
        self.change_phonebook(new_json)

    def find_contact(self, params: list):
        """
        Найти контакт по различным параметрам. На вход подается словарь.
        Если поиск планируется по номеру телефона, необходимо передавать его в словарь в формате str.
        Возвращает в консоль таблицу всех подходящих по параметрам контактов.
        """
        contacts = self.open_phonebook()
        result = []
        for value in params:
            for row in contacts:
                if value in row.values():
                    result.append(row)
        if result:
            to_display = self.to_display()
            for row in result:
                to_display.add_row(list(row.values()))
            print("Результаты по вашему запросу:")
            print(to_display)
        else:
            print("По вашему запросу ничего не найдено")

    def update_contact(self, name: str, lastname: str, params: dict):
        """
        Ищет контакт по имени и фамилии. Обновляет данные контакта, переданные в словарь params вида:

         {
            "name": str, "lastname": str, "surname": str, "organization": str,
            "work_phone_number": str|int, "personal_number": str|int
         }

         Можно передать любое количество указанных параметров.
         """
        contacts = self.open_phonebook()
        for contact in contacts:
            if name == contact["name"] and lastname == contact["lastname"]:
                contact.update(params)
            new_json = json.dumps(contacts, indent=4)
            self.change_phonebook(new_json)
            return print(f"Contact {contact['name']} {contact['lastname']} successfully updated")

    def delete_contact(self, name: str, lastname: str):
        """ Ищет по имени и фамилии и удаляет ПЕРВЫЙ подходящий контакт. """
        contacts = self.open_phonebook()
        for contact in contacts:
            if name == contact["name"] and lastname == contact["lastname"]:
                contacts.remove(contact)
                new_json = json.dumps(contacts, indent=4)
                self.change_phonebook(new_json)
                return print(f"Contact {contact['name']} {contact['lastname']} has been deleted")

# Пример работы всех функций


customer = {"name": "Iliya", "lastname": "Ovechkin", "surname": "Iliich", "organization": "NHL",
            "work_phone_number": "77-77", "personal_number": "777-11133"}

params = ["John", "777-11133"]

updated_params = {"organization": "Westwood", "surname": "Gideonovich"}

phone_book = PhoneBook('phonebook.json')

phone_book.read()
phone_book.create(customer)
phone_book.read()
phone_book.find_contact(params)
phone_book.page_forward()
phone_book.page_backward()
phone_book.update_contact("John", "Doe", updated_params)
phone_book.read()
phone_book.delete_contact("Iliya", "Ovechkin")
help(phone_book)
