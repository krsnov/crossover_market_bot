import psycopg2
from config import db_connection_string
from datetime import datetime


def check_super_adm(tlgm_id):
    con = psycopg2.connect(db_connection_string)
    with con.cursor() as cur:
        cur.execute(f"select tlgm_id from users where tlgm_id = 910090977")
        super_id = cur.fetchone()[0]
    con.close()
    if tlgm_id == super_id:
        return True
    else:
        return False


def select_user(number):
    if len(number) == 11:
        query = f"select name, phone, card, bonus, tlgm_id, gift_bonus, ttl_gb, birthday, roles from users where phone = '{number}'"
    elif len(number) == 8:
        query = f"select name, phone, card, bonus, tlgm_id, gift_bonus, ttl_gb, birthday, roles from users where card = '{number}'"
    con = psycopg2.connect(db_connection_string)
    with con.cursor() as cur:
        cur.execute(query)
        inf = cur.fetchone()
    con.close()
    return inf


def select_all_users():
    con = psycopg2.connect(db_connection_string)
    with con.cursor() as cur:
        cur.execute('select tlgm_id from users')
        users = cur.fetchall()
    con.close()
    return users


def super_find_user(number, rool):
    try:
        con = psycopg2.connect(db_connection_string)
        with con.cursor() as cur:
            cur.execute(f"update users set roles = {rool} where tlgm_id = '{number}'")
            con.commit()
        con.close()
        return True
    except Exception:
        return False


def update_bonus(bonus, gift_bonus, number):
    con = psycopg2.connect(db_connection_string)
    with con.cursor() as cur:
        cur.execute(f"update users set bonus = {bonus}, gift_bonus = {gift_bonus} where card = '{number}'")
        con.commit()
    con.close()


def check_ttl_gift_bonus(gift_bonus, ttl_gb):
    try:
        assert gift_bonus
        assert (datetime.date(datetime.now()) < ttl_gb)
        return gift_bonus, f'❗️Вы имеете {"%.2f" % gift_bonus} подарочных баллов,\n' \
                           f'❗️успейте потратить их до <b>{datetime.strftime(ttl_gb, "%d.%m.%Y")}</b>!\n'
    except Exception:
        return 0, ''
