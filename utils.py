import http.cookies
import hashlib
from constants import SECRET_KEY_FOR_COOKIE_GENERATOR

from db_connection import PSQLConnection


def get_login_by_cookie(cookie):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = "SELECT login FROM users WHERE authorization_cookie = '" + cookie + "'"
        cursor.execute(query)
        try:
            login = cursor.fetchone()[0]
        except TypeError:
            return None
        return login


def is_cookie_actual(given_cookie):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = "SELECT authorization_cookie FROM users WHERE authorization_cookie = '" + given_cookie + "'"
        cursor.execute(query)
        try:
            real_cookie = cursor.fetchone()[0]
            if real_cookie == given_cookie:
                return True
            else:
                return False
        except TypeError:
            return False


def delete_cookie(given_cookie):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = "UPDATE users SET authorization_cookie = NULL WHERE authorization_cookie = '" + given_cookie + "'"
        cursor.execute(query)


def get_password_by_login(login):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = "SELECT password FROM users WHERE login = '" + login + "'"
        cursor.execute(query)
        try:
            password = cursor.fetchone()[0]
        except TypeError:
            return None
        return password


def update_cookie(login, given_cookie):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = "UPDATE users SET authorization_cookie = '" + given_cookie + "' WHERE login = '" + login + "'"
        cursor.execute(query)


def create_user(
        login,
        email,
        password
):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = f"INSERT INTO users (id, login, email, password, authorization_cookie) "\
                f"VALUES (DEFAULT, '{login}', '{email}', '{password}', NULL);"
        cursor.execute(query)


def check_cookie(headers):
    try:
        all_cookies = http.cookies.SimpleCookie(headers['Cookie'])
        given_cookie = all_cookies['bubuka-test-cookie'].value
        if is_cookie_actual(given_cookie):
            return True
        else:
            return False
    except KeyError:
        return False


def generate_cookie(login, password):
    string = f'{login}.{password}.{SECRET_KEY_FOR_COOKIE_GENERATOR}'
    cookie = hashlib.sha256(string.encode()).hexdigest()
    return str(cookie)


def get_continents():
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = "SELECT continent FROM countries GROUP BY continent ORDER BY continent"
        cursor.execute(query)
        try:
            continents = cursor.fetchall()
        except TypeError:
            return None
        return continents


def get_cities(continent):
    with PSQLConnection() as connection:
        cursor = connection.cursor()
        query = f"""
            SELECT row_number() over (), c.city, c.country, population
            FROM countries
            INNER JOIN cities c on countries.country = c.country
            INNER JOIN population p on c.city = p.city
            WHERE continent = '{continent}'
            ORDER BY population DESC
        """
        cursor.execute(query)
        try:
            cities = cursor.fetchall()
        except TypeError:
            return None
        return cities
