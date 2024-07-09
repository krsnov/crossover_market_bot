import psycopg2
from config import db_connection_string
from datetime import datetime


def check_super_adm(tlgm_id):
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('select tlgm_id from users where tlgm_id = 506165762')
        super_id = cur.fetchone()[0]
    con.close()
    if tlgm_id == super_id:
        return True
    else:
        return False


def select_user(number):
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('select name, phone, card, bonus, tlgm_id, gift_bonus, ttl_gb, birthday, roles '
                    'from users where phone = %s or card = %s', (number, number,))
        inf = cur.fetchone()
    con.close()
    return inf


def select_all_users():
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('select tlgm_id from users')
        users = cur.fetchall()
    con.close()
    return users


def super_find_user(number, rool):
    try:
        con = psycopg2.connect(db_connection_string)
        con.set_client_encoding('UTF8')
        with con.cursor() as cur:
            cur.execute('update users set roles = %s where tlgm_id = %s', (rool, number,))
            con.commit()
        con.close()
        return True
    except Exception:
        return False


def update_bonus(bonus, gift_bonus, number):
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('update users set bonus = %s, gift_bonus = %s where card = %s', (bonus, gift_bonus, number,))
        con.commit()
    con.close()


def update_state(adm_id, new_bonus, new_gift_bonus, card, check_ttl, ttl_gb, user_name, user_id):
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('update state '
                    'set adm_id = %s, new_bonus = %s, new_gift_bonus = %s, card = %s, check_ttl = %s, '
                    'ttl_gb = %s, user_name = %s, user_id = %s',
                    (adm_id, new_bonus, new_gift_bonus, card, check_ttl, ttl_gb, user_name, user_id,))
        con.commit()
    con.close()


def select_state():
    con = psycopg2.connect(db_connection_string)
    con.set_client_encoding('UTF8')
    with con.cursor() as cur:
        cur.execute('select adm_id, new_bonus, new_gift_bonus, card, check_ttl, ttl_gb, user_name, user_id from state')
        value = cur.fetchall()[0]
    con.close()
    return value


def check_ttl_gift_bonus(gift_bonus, ttl_gb):
    try:
        assert gift_bonus
        assert (datetime.date(datetime.now()) < ttl_gb)
        return gift_bonus, f'❗️Вы имеете {"%.2f" % gift_bonus} подарочных баллов,\n' \
                           f'❗️успейте потратить их до <b>{datetime.strftime(ttl_gb, "%d.%m.%Y")}</b>!\n'
    except Exception:
        return 0, ''
