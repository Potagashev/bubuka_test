# DATABASE CREDENTIALS

HOST = 'ec2-176-34-211-0.eu-west-1.compute.amazonaws.com'
DBNAME = 'd1pq7vqqhcnc0'
USER = 'kgazhzbgqrmkwr'
PORT = '5432'
PASSWORD = 'cfc6a9d1be371749ffb34751f19f9180b4215003ae20661e1ffcb0c0159b00b0'

# -----------------

cookie_name = 'bubuka-test-cookie'

# ----------------- SQL REQUESTS -----------------------------

# TABLES CREATION
CREATE_USER_TABLE = """
    CREATE TABLE users
        (
            id SERIAL PRIMARY KEY,
            login CHARACTER VARYING(30) NOT NULL,
            email CHARACTER VARYING(30) UNIQUE ,
            password CHARACTER VARYING(30) NOT NULL,
            authorization_cookie CHARACTER VARYING(100) UNIQUE
        );
"""

CREATE_COUNTRIES_TABLE = """
    CREATE TABLE countries
        (
            country CHARACTER VARYING(30),
            continent CHARACTER VARYING(30) NOT NULL,
            PRIMARY KEY(country)
        );
"""

CREATE_CITIES_TABLE = """
    CREATE TABLE cities
        (
            city CHARACTER VARYING(30),
            country CHARACTER VARYING(30) REFERENCES countries (country) NOT NULL,
            PRIMARY KEY(city)
        );
"""

CREATE_POPULATION_TABLE = """
    CREATE TABLE population
        (
            city CHARACTER VARYING(100) REFERENCES cities (city) NOT NULL,
            population INTEGER NOT NULL,
            PRIMARY KEY(city)
        );
"""

# SELECTING DATA

GET_LOGIN_BY_COOKIE = """
    SELECT login FROM users
    WHERE authhorization_cookie = 
"""