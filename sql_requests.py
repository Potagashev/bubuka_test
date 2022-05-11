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
GET_LOGIN_BY_COOKIE = """
    SELECT login FROM users
    WHERE authhorization_cookie = 
"""
