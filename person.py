import string
from random import *
import sqlite3

class Person:
    school_db = "student_information_system.db"
    count = 1


    def __init__(self, name, surname, father_name, phone, FIN, country, city, password, email):
        self.__name = name
        self.__surname = surname
        self.__father_name = father_name
        self.__phone = phone
        self.__FIN = FIN
        self.__country = country
        self.__city = city
        self.__password = password
        self.__email = email

    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    def get_surname(self):
        return self.__surname
    
    def set_surname(self, surname):
        self.__surname = surname

    def get_father_name(self):
        return self.__father_name
    
    def set_father_name(self, father_name):
        self.__father_name = father_name

    def get_phone(self):
        return self.__phone
    
    def set_phone(self, phone):
        self.__phone = phone

    def get_FIN(self):
        return self.__FIN
    
    def set_FIN(self, FIN):
        self.__FIN = FIN

    def get_country(self):
        return self.__country
    
    def set_country(self, country):
        self.__country = country

    def get_city(self):
        return self.__city
    
    def set_city(self, city):
        self.__city = city

    def get_password(self):
        return self.__password
    
    def set_password(self, password):
        self.__password = password

    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        self.__email = email


    def new_person(self):
        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.name = str(input('Name: '))
        self.surname = str(input('Surname: '))
        self.father_name = str(input('Father name: '))
        self.FIN = input('FIN: ')

        while True:
            if len(self.FIN) != 7 or self.FIN.isdigit() or self.FIN.isalpha():
                print('Yanliş məlumat')
                self.FIN = input('FIN: ')
            else:
                break

        self.phone = input('Phone: ')

        while True:
            if len(self.phone) != 10 or not self.phone.isdigit():
                print('Yanliş məlumat')
                self.phone = (input('Phone: '))
            else:
                break

        self.country = str(input('Country: '))
        self.city = str(input('City: '))

        self.password = "".join(choice(string.ascii_letters + string.digits) for i in range(8))
        self.email = f'{self.name.lower()}{self.surname.lower()}{self.count}@std.kodaze.com'

        # base_email = f'{self.name.lower()}{self.surname.lower()}'
        # self.email = f'{base_email}{self.count}@std.kodaze.com'



    def all_person(self, data):

        apply_filter = input("Filtr etmək istəyirsiniz? (y/n): ")

        if apply_filter.lower() == 'y':
            name_filter = input("İsim filtr etmək (boş buraxmaq üçün Enter'a basın): ")
            surname_filter = input("Soyad filtr etmək (boş buraxmaq üçün Enter'a basın): ")
            country_filter = input("Olke filtr etmək (boş buraxmaq üçün Enter'a basın): ")
            city_filter = input("Şeher filtr etmək (boş buraxmaq üçün Enter'a basın): ")
            
            filtered_data = []
            for entry in data:
                if name_filter and entry['name'] != name_filter:
                    continue
                if surname_filter and entry['surname'] != surname_filter:
                    continue
                if country_filter and entry['country'] != country_filter:
                    continue
                if city_filter and entry['city'] != city_filter:
                    continue

                filtered_data.append(entry)
        else:
            filtered_data = data

        return filtered_data
    

    def update_person(self, key):
        self.name = str(input('Name: '))
        self.surname = str(input('Surname: '))
        self.father_name = str(input('Father name: '))
        self.FIN = input('FIN: ')

        while True:
            if len(self.FIN) != 7 or self.FIN.isdigit() or self.FIN.isalpha():
                print('Yanliş məlumat')
                self.FIN = input('FIN: ')
            else:
                break

        self.phone = input('Phone: ')

        while True:
            if len(self.phone) != 10 or not self.phone.isdigit():
                print('Yanliş məlumat')
                self.phone = int(input('Phone: '))
            else:
                break

        self.country = str(input('Country: '))
        self.city = str(input('City: '))

        # self.password = input('Password: ')

        # while True:
        #     if len(self.password) != 8:
        #         print('Yanliş məlumat')
        #     else:
        #         break


    def delete_person(self, table_name, key):
        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (key,))

        self.conn.commit()
        self.conn.close()

        print('Silindi.')
