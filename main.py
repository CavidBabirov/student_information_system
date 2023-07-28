from student import Student
from teacher import Teacher
import sqlite3



def check_the_admin():
    login = 'admin@kodaze.com'
    password = 'admin123'

    rlogin = str(input('Login: '))
    if rlogin == login:
        rpassword = str(input('Password: '))
        if rpassword == password:
            while True:
                print('1 --> Yeni telebe')
                print('2 --> Butun telebeler')
                print('3 --> Telebe melumatlarini yenile')
                print('4 --> Telebe sil\n')

                print('5 ---> Yeni Muellim')
                print('6 ---> Butun Muellimler')
                print('7 ---> Muellim melumatlarini yenile')
                print('8 ---> Muellim sil\n')

                print('0 ---> Exit\n')


                secim = int(input('Secim: '))
                if secim == 1:
                    Student.new_student(Student)
                                        
                elif secim == 2:
                    Student.all_student(Student)

                elif secim == 3:
                    Student.update_student(Student)

                elif secim == 4:
                    Student.delete_student(Student)

                elif secim == 5:
                    Teacher.new_teacher(Teacher)

                elif secim == 6:
                    Teacher.all_teacher(Teacher)

                elif secim == 7:
                    Teacher.update_teacher(Teacher)

                elif secim == 8:
                    Teacher.delete_teacher(Teacher)

                elif secim == 0:
                    exit()

                else:
                    print('Yanliş məlumat')

        else:
            print('Yanliş məlumat')
    else:
        print('Yanliş məlumat')






while True:
    print('1 ---> Admin\n2 ---> Teacher\n 3 ---> Student')
    check_login = input('Select user type: ')

    if check_login == '1':
        check_the_admin()
    elif check_login == '2':
        Teacher.teacher_login(Teacher)
    elif check_login == '3':
        Student.teacher_login(Student)

    else:
        print('Yanliş məlumat')


