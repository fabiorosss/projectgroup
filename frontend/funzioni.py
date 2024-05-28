import mysql.connector
from mysql.connector import Error
import csv
from unidecode import unidecode
import pandas as pd
import numpy as np
from datetime import timedelta, datetime


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")


def drop_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def caricamento_dataframe(connection, query, df):
    # print("DataFrame Column Data Types:")
    # print(df.dtypes)
    records = df.to_records(index=False)
    data = [tuple(record) for record in records]
    try:
        cursor = connection.cursor()
        cursor.executemany(query, data)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def caricamento_lista(connection, query, l):
    data = [tuple(record) for record in l]
    try:
        cursor = connection.cursor()
        cursor.executemany(query, data)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")


def caricamento_dataframe2(connection, query, df):
    # print("DataFrame Column Data Types:")
    # print(df.dtypes)
    records = df.to_records(index=False)
    data = [tuple(record) for record in records]
    for elem in data:
        try:
            cursor = connection.cursor()
            cursor.execute(query, elem)
            print("Query successful")
            connection.commit()
        except Error as err:
            print(f"Error: '{err}'")
            print(elem)


