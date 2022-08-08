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
    cur.execute('''
    SELECT id FROM client WHERE first_name=%s AND surname=%s;
    ''', (name, last_name))
    res = cur.fetchone()[0]
    cur.execute('''
    UPDATE client SET first_name=%s, surname=%s, email=%s WHERE id=%s;
    ''', (new_name, new_surname, new_email, res))


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


def find_client(name, last_name, e_mail, phone_num):
    cur.execute('''
    SELECT first_name, surname, email, pn.phone FROM client c
    LEFT JOIN phone_number pn ON pn.client_id = c.id
    WHERE first_name=%s AND surname=%s AND email=%s AND pn.phone=%s;
    ''', (name, last_name, e_mail, phone_num))
    res = cur.fetchall()
    print(res)



    conn.commit()