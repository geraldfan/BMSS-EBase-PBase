# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 11:17:39 2021

@author: Gerald
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 14:44:13 2021

@author: Gerald
"""

import sqlite3

import openpyxl
from sqlalchemy import create_engine, MetaData, Table, Column, String


def read():
    # read original data from microplate reader
    file = 'cytation_H1_plate1_GFP.xlsx'
    cellsId = ('C2', 'CT34')
    timeCellsId = ('A2', 'A34')
    temperatureCellsId = ('B2', 'B34')
    settingsId = ('A2', 'F2')
    identifierId = ('B2', 'B2')
    book = openpyxl.load_workbook(file)
    data_sheet = 'Data'
    settings_sheet = 'Settings'

    settingsCells = get_cells(file, settingsId, settings_sheet)
    cells = get_cells(file, cellsId, data_sheet)
    timeCells = get_cells(file, timeCellsId, data_sheet)
    temperatureCells = get_cells(file, temperatureCellsId, data_sheet)
    identifier = get_identifier(identifierId, file, settings_sheet)

    settings = []
    settings = generate_nested_list(settings, settingsCells)
    settings = append_to_nested_list(settings, settingsCells)

    values = []
    values = generate_nested_list(values, cells)
    values = append_to_nested_list(values, cells)

    formatted_cells = []
    formatted_cells = generate_nested_list(formatted_cells, cells)
    formatted_cells = append_identifier_to_nested_list(formatted_cells, cells, identifier)
    formatted_cells = append_time_to_nested_list(formatted_cells, timeCells)
    formatted_cells = append_to_nested_list(formatted_cells, temperatureCells)
    formatted_cells = append_values_to_nested_list(formatted_cells, values)


    add_to_database(formatted_cells)
    add_to_settings(settings)


def get_identifier(identifierId, file, sheet):
    book = openpyxl.load_workbook(file)
    sheet = book[sheet]

    cell = sheet[identifierId[0]:identifierId[1]]
    return cell[0][0].value


def get_cells(file, cellsId, sheet):
    book = openpyxl.load_workbook(file)
    sheet = book[sheet]

    cells = sheet[cellsId[0]: cellsId[1]]

    return cells


def generate_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        formatted_cells.append([])

    return formatted_cells


def append_to_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        for k in range(len(cells[0])):
            formatted_cells[i].append(cells[i][k].value)

    return formatted_cells


def append_values_to_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        formatted_cells[i].append(str(cells[i]))

    return formatted_cells


def append_time_to_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        for k in range(len(cells[0])):
            formatted_cells[i].append(cells[i][k].value.strftime("%H:%M:%S"))

    return formatted_cells


def append_identifier_to_nested_list(formatted_cells, cells, identifier):
    for i in range(len(cells)):
        formatted_cells[i].append(identifier)

    return formatted_cells


def add_to_database(cells):
    db = "sqlite:///EBase.db"
    create_table(db)
    connection = create_connection("EBase.db")

    connection.executemany("""

                           INSERT INTO
                           data(identifier, time, set_temperature, data_values)
                           VALUES(?,?,?,?)""", cells)

    connection.commit()
    connection.close()


def add_to_settings(cells):
    db = "sqlite:///EBase.db"
    create_table(db)
    connection = create_connection("EBase.db")

    connection.executemany("""

                           INSERT INTO
                           settings(protocol, identifier, experiment_type, temperature, media, equipment)
                           VALUES(?,?,?,?,?,?)""", cells)

    connection.commit()
    connection.close()


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(db):
    engine = create_engine(db)

    meta = MetaData()

    data = Table(
        'data', meta,
        Column('identifier', String),
        Column('time', String),
        Column('set_temperature', String),
        Column('data_values', String, primary_key=True)
    )

    settings = Table(
        'settings', meta,
        Column('protocol', String),
        Column('identifier', String, primary_key=True),
        Column('experiment_type', String),
        Column('Temperature', String),
        Column('Media', String),
        Column('Equipment', String)
    )
    meta.create_all(engine)


# Enable the script to be run from the command line
if __name__ == "__main__":
    read()
