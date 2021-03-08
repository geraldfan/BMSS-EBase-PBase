# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:50:47 2021

@author: Gerald
"""

import sqlite3

import openpyxl
from sqlalchemy import create_engine, MetaData, Table, Column, String


def read():
    # read original data from microplate reader
    file = 'E6-04_plasmid_list.xlsx'

    nameCellsId = ('A3', 'A62')
    plasmidOriginId = ('C3', 'C62')
    restOriginId = ('P3', 'R62')
    setInfoId = ('D3', 'O62')

    nameCells = get_cells(file, nameCellsId)
    plasmidOriginCells = get_cells(file, plasmidOriginId)
    restOriginCells = get_cells(file, restOriginId)
    setInfoCells = get_cells(file, setInfoId)

    set_cells = []
    set_cells = generate_nested_list(set_cells, nameCells)
    set_cells = append_to_nested_list(set_cells, setInfoCells)

    formatted_cells = []

    formatted_cells = generate_nested_list(formatted_cells, nameCells)

    formatted_cells = append_to_nested_list(formatted_cells, nameCells)
    formatted_cells = append_to_nested_list(formatted_cells, plasmidOriginCells)
    formatted_cells = append_set_to_nested_list(formatted_cells, set_cells)
    formatted_cells = append_to_nested_list(formatted_cells, restOriginCells)


    print(formatted_cells)
    add_to_database(formatted_cells)


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


def append_set_to_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        formatted_cells[i].append(str(cells[i]))

    return formatted_cells

def add_to_database(cells):
    db = "sqlite:///PBase.db"

    create_table(db)
    connection = create_connection("PBase.db")

    connection.executemany("""
                           
                           INSERT INTO 
                           plasmid(name, plasmid_origin, set_information, dna_sequence,size, benchling)
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

    plasmid = Table(
        'plasmid', meta,
        Column('name', String, primary_key=True),
        Column('plasmid_origin', String),
        Column('set_information', String),
        Column('dna_sequence', String),
        Column('size', String),
        Column('benchling', String)
    )


    meta.create_all(engine)


# Enable the script to be run from the command line
if __name__ == "__main__":
    read()
