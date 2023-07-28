from person import Person
import string
from random import *
import sqlite3

class Teacher(Person):
    school_db = "student_information_system.db"
    
    def __init__(self, name, surname, father_name, phone, FIN, country, city, subject, password, email, personnel_number):
        super().__init__(name, surname, father_name, phone, FIN, country, city, password, email)
        self.__subject = subject
        self.__personnel_number = personnel_number

    def get_subject(self):
        return self.__subject
    
    def set_subject(self, subject):
        self.__subject = subject

    def get_personnel_number(self):
        return self.__personnel_number
    
    def set_personnel_number(self, personnel_number):
        self.__personnel_number = personnel_number


    def new_teacher(self):
        self.new_person(self)
        self.email = f'{self.name.lower()}{self.surname.lower()}{self.count}@kodaze.com'


        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM teacher WHERE phone=?", (self.phone,))
        existing_phone_record = self.cursor.fetchone()

        if existing_phone_record:
            print("Bu telefon nömrəsi artıq istifadə olunur.")
            self.conn.close()
            return
        
        self.cursor.execute("SELECT * FROM teacher WHERE FIN=?", (self.FIN,))
        existing_fin_record = self.cursor.fetchone()

        if existing_fin_record:
            print("Bu FIN nömrəsi artıq istifadə olunur.")
            self.conn.close()
            return
        
        self.cursor.execute("SELECT * FROM teacher WHERE email=?", (self.email,))
        existing_email_record = self.cursor.fetchone()

        while existing_email_record:
            self.count += 1
            self.email = f'{self.name.lower()}{self.surname.lower()}{self.count}@kodaze.com'
            self.cursor.execute("SELECT * FROM teacher WHERE email=?", (self.email,))
            existing_email_record = self.cursor.fetchone()
        
        self.conn.close()


        self.subject = input('Subject: ')

        self.personnel_number = "".join(choice(string.digits) for i in range(9))

        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS teacher (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                surname TEXT,
                father_name TEXT,
                phone INTEGER,
                FIN TEXT,
                country TEXT,
                city TEXT,
                subject TEXT,
                password TEXT,
                email TEXT,
                personnel_number INTEGER UNIQUE
            )
        """)

        self.cursor.execute("""
            INSERT INTO teacher (name, surname, father_name, phone, FIN, country, city, subject, password, email, personnel_number)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (self.name, self.surname, self.father_name, self.phone, self.FIN, self.country, self.city, self.subject, self.password, self.email, self.personnel_number))

        self.conn.commit()
        self.conn.close()

        print("Data school_db ünvanında saxlanıldı")



    def all_teacher(self):
        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM teacher")
        rows = self.cursor.fetchall()

        data = [{'name': row[1], 'surname': row[2], 'father_name': row[3], 'phone': row[4], 'FIN': row[5], 'country': row[6], 'city': row[7],
                 'subject': row[8], 'password': row[9], 'email': row[10], 'personnel_number': row[11]} for row in rows]

        filtered_data = self.all_person(self, data)

        print("Filtr edilmis datalar:")
        for entry in filtered_data:
            print(entry)

        self.conn.close()


    def update_teacher(self):
        key = int(input('Id daxil edin: '))
        self.conn = sqlite3.connect(self.school_db)
        self.cursor = self.conn.cursor()

        self.update_person(self, key)

        self.cursor.execute("""
            UPDATE teacher
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
            FROM teacher
            WHERE email=? AND password=?
        """, (email, password))

        teacher_data = self.cursor.fetchone()

        if teacher_data:
            teacher_id, name, surname, father_name, phone, password, current_email = teacher_data
            
            self.name = input('Ad: ')
            self.surname = input('Soyad: ')
            self.father_name = input('Ata adı: ')
            self.phone = input('Telefon: ')
            self.password = input('Password: ')

            new_email = f'{self.name.lower()}{self.surname.lower()}@kodaze.com'
            self.email = new_email if new_email != current_email else current_email



            self.cursor.execute("""
                UPDATE teacher
                SET name=?, surname=?, father_name=?, phone=?, password=?, email=?
                WHERE id=?
            """, (self.name, self.surname, self.father_name, self.phone, self.password, self.email, teacher_id))

            self.conn.commit()
            print("Məlumatlarınız yeniləndi.")
        else:
            print("Giriş uğursuz oldu. Lütfən, düzgün e-poçt və parol daxil edin.")

        self.conn.close()












        # email = input('Email daxil edin: ')
        # password = input('Parol daxil edin: ')

        # self.conn = sqlite3.connect(self.school_db)
        # self.cursor = self.conn.cursor()

        # self.cursor.execute("""
        #     SELECT id
        #     FROM teacher
        #     WHERE email=? AND password=?
        # """, (email, password))

        # teacher_id = self.cursor.fetchone()

        # if teacher_id:
        #     self.cursor.execute("""
        #         UPDATE teacher
        #         SET name=?, surname=?, father_name=?, phone=?, FIN=?, country=?, city=?
        #         WHERE id=?
        #     """, (self.name, self.surname, self.father_name, self.phone, self.FIN, self.country, self.city))
        # else:
        #     print("Giriş başarısız. Lütfen doğru email ve parolayı girin.")

        # self.conn.close()



    def delete_teacher(self):
        key = int(input('Id daxil edin: '))
        self.delete_person(self, 'teacher', key)