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
    file = 'cytation_H1_plate1.xlsx'
    cellsId = ('D63', 'CU95')
    timeCellsId = ('B63', 'B95')
    protocolId = ('A60', 'A60')
    temperatureCellsId = ('C63', 'C95')
    book = openpyxl.load_workbook(file)
    sheet = book.active

    protocol = get_protocol(protocolId, file)
    cells = get_cells(file, cellsId)
    timeCells = get_cells(file, timeCellsId)
    temperatureCells = get_cells(file, temperatureCellsId)

    values = []
    values = generate_nested_list(values, cells)
    values = append_to_nested_list(values, cells)

    formatted_cells = []
    formatted_cells = generate_nested_list(formatted_cells, cells)
    formatted_cells = append_protocol_to_nested_list(formatted_cells, cells, protocol)
    formatted_cells = append_time_to_nested_list(formatted_cells, timeCells)
    formatted_cells = append_to_nested_list(formatted_cells, temperatureCells)
    formatted_cells = append_values_to_nested_list(formatted_cells, values)


    print(formatted_cells)
    add_to_database(formatted_cells)


def get_protocol(protocolId, file):
    book = openpyxl.load_workbook(file)
    sheet = book.active

    cell = sheet[protocolId[0]:protocolId[1]]
    return cell[0][0].value


def get_cells(file, cellsId):
    book = openpyxl.load_workbook(file)
    sheet = book.active

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


def append_protocol_to_nested_list(formatted_cells, cells, protocol):
    for i in range(len(cells)):
        formatted_cells[i].append(protocol)

    return formatted_cells



def add_to_database(cells):
    db = "sqlite:///EBase.db"
    create_table(db)
    connection = create_connection("EBase.db")


    connection.executemany("""

                           INSERT INTO
                           data(protocol, time, set_temperature, data_values)
                           VALUES(?,?,?,?)""", cells)

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
        Column('protocol', String),
        Column('time', String),
        Column('set_temperature', String, ),
        Column('data_values', String, primary_key = True)
    )

    meta.create_all(engine)


# Enable the script to be run from the command line
if __name__ == "__main__":
    read()
