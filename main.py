import psycopg2


def create_table():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS client(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(60) NOT NULL,
    surname VARCHAR(60) NOT NULL,
    email VARCHAR(120)
    );
    ''')

    cur.execute('''
    CREATE TABLE IF NOT EXISTS phone_number(
    id SERIAL PRIMARY KEY,
    phone VARCHAR(50),
    client_id INTEGER NOT NULL REFERENCES client(id)
    );
    ''')


def add_client(name_client, surname_client, email, phone):
    cur.execute('''
    INSERT INTO client(first_name, surname, email) VALUES(%s, %s, %s) RETURNING id;
    ''', (name_client, surname_client, email))
    res = cur.fetchone()
    cur.execute('''
    INSERT INTO phone_number(phone, client_id) VALUES (%s, %s);
    ''', (phone, res))


def add_phone(name, phone):
    cur.execute('''
    SELECT id FROM client WHERE surname=%s;
    ''', (name,))
    res = cur.fetchone()[0]
    cur.execute('''
    INSERT INTO phone_number(phone, client_id) VALUES (%s, %s);
    ''', (phone, res))


def update_client(name, last_name, new_name, new_surname, new_email):
    print("Для изменения информации о клиенте, пожалуйста, введите нужную Вам команду.\n "
          "1 - изменить имя; 2 - изменить фамилию; 3 - изменить e-mail; 4 - изменить номер телефона")

    while True:
        command_sym = int(input())
        if command_sym == 1:
            input_id_for_changing_name = input("Введите id клиента имя которого хотите изменить: ")
            input_name_for_changing = input("Введите имя для изменения: ")
            cur.execute("""
                UPDATE client SET first_name=%s WHERE id=%s;
                """, (input_name_for_changing, input_id_for_changing_name))
            break
        elif command_sym == 2:
            input_id_for_changing_surname = input("Введите id клиента фамилию которого хотите изменить: ")
            input_surname_for_changing = input("Введите фамилию для изменения: ")
            cur.execute("""
                UPDATE client SET surname=%s WHERE id=%s;
                """, (input_surname_for_changing, input_id_for_changing_surname))
            break
        elif command_sym == 3:
            input_id_for_changing_email = input("Введите id клиента e-mail которого хотите изменить: ")
            input_email_for_changing = input("Введите e-mail для изменения: ")
            cur.execute("""
                UPDATE client SET email=%s WHERE id=%s;
                """, (input_email_for_changing, input_id_for_changing_email))
            break
        elif command_sym == 4:
            input_phonenumber_you_wanna_change = input("Введите номер телефона который Вы хотите изменить: ")
            input_phonenumber_for_changing = input("Введите новый номер телефона, который заменит собой старый: ")
            cur.execute("""
                UPDATE phone_number SET phone=%s WHERE phone=%s;
                """, (input_phonenumber_for_changing, input_phonenumber_you_wanna_change))
            break
        else:
            print("К сожалению, Вы ввели неправильную команду, пожалуйста, повторите ввод")


def delete_phone(name, last_name):
    cur.execute('''
    SELECT id FROM client WHERE first_name=%s AND surname=%s;
    ''', (name, last_name))
    res = cur.fetchone()[0]
    cur.execute('''
    DELETE FROM phone_number WHERE id=%s;
    ''', (res,))


def delete_client(name, last_name):
    cur.execute('''
    SELECT id FROM client WHERE first_name=%s AND surname=%s;
    ''', (name, last_name))
    res = cur.fetchone()[0]
    print(res)
    cur.execute('''
    DELETE FROM phone_number WHERE client_id=%s;
    ''', (res,))
    cur.execute('''
    DELETE FROM client WHERE first_name=%s AND surname=%s
    ''', (name, last_name))


def find_client():
    '''Поиск клиента по имени'''
    print("Для поиска информации о клиенте, пожалуйста, введите команду, где:\n "
          "1 - найти по имени; 2 - найти по фамилии; 3 - найти по e-mail; 4 - найти по номеру телефона")
    while True:
        input_command_for_finding = int(input("Введите команду для поиска информации о клиенте: "))
        if input_command_for_finding == 1:
            input_name_for_finding = input("Введите имя для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, surname, email, phone
            FROM client AS cl
            LEFT JOIN phone AS p ON p.id_phonenumber = cl.id
            WHERE first_name=%s
            """, (input_name_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 2:
            input_surname_for_finding = input("Введите фамилию для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, surname, email, phone
            FROM client AS cl
            LEFT JOIN phone AS p ON p.id_phonenumber = cl.id
            WHERE surname=%s
            """, (input_surname_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 3:
            input_email_for_finding = input("Введите email для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, surname, email, phone
            FROM client AS cl
            LEFT JOIN phone AS p ON p.id_phonenumber = cl.id
            WHERE email=%s
            """, (input_email_for_finding,))
            print(cur.fetchall())
        elif input_command_for_finding == 4:
            input_phonenumber_for_finding = input("Введите номер телефона для поиска информации о клиенте: ")
            cur.execute("""
            SELECT id, first_name, surname, email, phone
            FROM client AS cl
            LEFT JOIN phone AS p ON p.id_phonenumber = cl.id
            WHERE phone=%s
            """, (input_phonenumber_for_finding,))
            #return cur.fetchone()[0]
            print(cur.fetchall())
        else:
            print("К сожалению, Вы ввели неправильную команду, пожалуйста, повторите ввод")



    conn.commit()

    if __name__ == '__main__':
        with psycopg2.connect(database="TestDB", user="postgres", password="postgres") as conn:
            with conn.cursor() as cur:
                cur.execute('''
                DROP TABLE phone_number;
                DROP TABLE client
                ''')
                create_table()
                add_client('Ad', 'Ellers', 'ad.a@gmail.com', '+324638453174')
                add_client('Matthew', 'Park', 'Mat.P@mail.com', '+324754863174')
                add_phone('Ad', '+420602272666')
                add_phone('Ad', '+420777875355')
                add_phone('Ad', '+420606879456')
                add_phone('Matthew', '+324638453176')
                add_phone('Matthew', '+324638453172')
                add_phone('Matthew', '+324638453187')
                update_client('Melany', 'Matthew', 'Melany', 'Seeto', 'seeto.mel@gmail.com')
                delete_phone('Audrey', 'Smith')
                delete_phone('Alison', 'Moore')
                find_client('Ad', 'Ellers', 'ad.a@gmail.com', '+324638453174')

                conn.commit()