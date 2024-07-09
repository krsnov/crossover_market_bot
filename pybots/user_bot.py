import psycopg2
from config import db_connection_string
import random
import string


def insert_user(id, name):
    try:
        con = psycopg2.connect(db_connection_string)
        con.set_client_encoding('UTF8')
        with con.cursor() as cur:
            cur.execute('insert into users (tlgm_id, roles, name) values %s on conflict (tlgm_id) do NOTHING',
                        [(id, False, name,)])
            con.commit()
        con.close()
        return True
    except Exception as e:
        print(e)
        return False


def insert_phone_numbers(phone_number, tlgm_id):
    try:
        con = psycopg2.connect(db_connection_string)
        con.set_client_encoding('UTF8')
        with con.cursor() as cur:
            cur.execute(f'update users set phone = %s where tlgm_id = %s', (phone_number, tlgm_id,))
            con.commit()
        con.close()
        return True
    except Exception as e:
        print(e)
        return False


def insert_birthday(birthday, tlgm_id):
    try:
        con = psycopg2.connect(db_connection_string)
        con.set_client_encoding('UTF8')
        with con.cursor() as cur:
            cur.execute(f'update users set birthday = %s where tlgm_id = %s', (birthday, tlgm_id,))
            con.commit()
        con.close()
        return True
    except Exception as e:
        print(e)
        return False


def create_card(tlgm_id):
    card = str(random.randint(1, 9)) + ''.join(random.choices(string.digits, k=7))
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    try:
        with con.cursor() as cur:
            cur.execute(f'update users set card = %s, bonus = 300, gift_bonus = 0 where tlgm_id = %s', (card, tlgm_id,))
            con.commit()
        con.close()
    except Exception:
        create_card(tlgm_id)


def select_card_information(tlgm_id):
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute(f'select card, bonus, gift_bonus, ttl_gb from users where tlgm_id = %s', (tlgm_id,))
        inf = cur.fetchone()
    con.close()
    return inf


def select_tokens():
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('select token from tokens')
        tokens = cur.fetchall()
    con.close()
    return tokens


def check_users(id):
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    try:
        with con.cursor() as cur:
            cur.execute('select id, roles from users where tlgm_id = %s', (id,))
            user_inf = cur.fetchall()[0]
        con.close()
        return True, user_inf[1]
    except Exception:
        return False, None


def add_gift_bonus(gb, ttl_gb, tlgm_id):
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute(f'update users set gift_bonus = %s, ttl_gb = %s where tlgm_id = %s', (gb, ttl_gb, tlgm_id,))
        con.commit()
    con.close()


def select_birthday():
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('select tlgm_id, name, birthday from users WHERE birthday is not null')
        bds = cur.fetchall()
    con.close()
    return bds
