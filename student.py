from person import Person
import string
from random import *
import sqlite3


class Student(Person):
    school_db = "student_information_system.db"

    def __init__(self, name, surname, father_name, phone, FIN, country, city, acceptance_score, password, email, student_number):
        super().__init__(name, surname, father_name, phone, FIN, country, city, password, email)
        self.__acceptance_score = acceptance_score
        self.__student_number = student_number

    def get_acceptance_score(self):
        return self.__acceptance_score
    
    def set_acceptance_score(self, acceptance_score):
        self.__acceptance_score = acceptance_score

    def get_student_number(self):
        return self.__student_number
    
    def set_student_number(self, student_number):
        self.__student_number = student_number



    def new_student(self):
        self.new_person(self)

        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM student WHERE phone=?", (self.phone,))
        existing_phone_record = self.cursor.fetchone()

        if existing_phone_record:
            print("Bu telefon nömrəsi artıq istifadə olunur.")
            self.conn.close()
            return
        
        self.cursor.execute("SELECT * FROM student WHERE FIN=?", (self.FIN,))
        existing_fin_record = self.cursor.fetchone()

        if existing_fin_record:
            print("Bu FIN nömrəsi artıq istifadə olunur.")
            self.conn.close()
            return
        
        self.cursor.execute("SELECT * FROM student WHERE email=?", (self.email,))
        existing_email_record = self.cursor.fetchone()

        while existing_email_record:
            self.count += 1
            self.email = f'{self.name.lower()}{self.surname.lower()}{self.count}@std.kodaze.com'
            self.cursor.execute("SELECT * FROM student WHERE email=?", (self.email,))
            existing_email_record = self.cursor.fetchone()
            # self.count += 1
        
        self.conn.close()


        self.acceptance_score = int(input('Acceptance Score: '))

        while True:
            if self.acceptance_score < 0 or self.acceptance_score > 700:
                print('Yanliş məlumat')
                self.acceptance_score = int(input('Acceptance Score: '))
            else:
                break
        


        self.student_number = "".join(choice(string.digits) for i in range(9))

        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS student (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                father_name TEXT,
                phone INTEGER,
                FIN TEXT,
                country TEXT,
                city TEXT,
                acceptance_score INTEGER,
                password TEXT,
                email TEXT,
                student_number INTEGER UNIQUE
            )
        """)

        self.cursor.execute("""
            INSERT INTO student (name, surname, father_name, phone, FIN, country, city, acceptance_score, password, email, student_number)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.name, self.surname, self.father_name, self.phone, self.FIN, self.country, self.city, self.acceptance_score, self.password, self.email, self.student_number))

        self.conn.commit()
        self.conn.close()

        print("Data school_db ünvanında saxlanıldı")
        # self.count = self.count =+1


    def all_student(self):
        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM student")
        rows = self.cursor.fetchall()

        data = [{'name': row[1], 'surname': row[2], 'father_name': row[3], 'phone': row[4], 'FIN': row[5], 'country': row[6], 'city': row[7],
                 'acceptance_score': row[8], 'password': row[9], 'email': row[10], 'student_number': row[11]} for row in rows]

        filtered_data = self.all_person(self, data)

        print("Filtr edilmis datalar:")
        for entry in filtered_data:
            print(entry)

        self.conn.close()


    def update_student(self):
        key = int(input('Id daxil edin: '))
        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.update_person(self, key)

        self.cursor.execute("""
            UPDATE student
            SET name=?, surname=?, father_name=?, phone=?, FIN=?, country=?, city=?
            WHERE id=?
        """, (self.name, self.surname, self.father_name, self.phone, self.FIN, self.country, self.city, key))

        self.conn.commit()
        self.conn.close()

        print('Güncellendi.')


    def teacher_login(self):
        email = input('Email daxil edin: ')
        password = input('Parol daxil edin: ')

        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            SELECT id, name, surname, father_name, phone, password, email
            FROM student
            WHERE email=? AND password=?
        """, (email, password))

        student_data = self.cursor.fetchone()

        if student_data:
            student_id, name, surname, father_name, phone, password, current_email  = student_data
            

            self.name = input('Ad: ')
            self.surname = input('Soyad: ')
            self.father_name = input('Ata adı: ')
            self.phone = input('Telefon: ')
            self.password = input('Password: ')

            new_email = f'{self.name.lower()}{self.surname.lower()}@kodaze.com'
            self.email = new_email if new_email != current_email else current_email



            self.cursor.execute("""
                UPDATE student
                SET name=?, surname=?, father_name=?, phone=?, password=?, email=?
                WHERE id=?
            """, (self.name, self.surname, self.father_name, self.phone, self.password, self.email, student_id))
            
            self.conn.commit()
            print("Məlumatlarınız yeniləndi.")
        else:
            print("Giriş uğursuz oldu. Lütfən, düzgün e-poçt və parol daxil edin.")

        self.conn.close()


    

    def delete_student(self):
        key = int(input('Id daxil edin: '))
        self.delete_person(self, 'student', key)
