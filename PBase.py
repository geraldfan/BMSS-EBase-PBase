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

    formatted_cells = []

    formatted_cells = generate_nested_list(formatted_cells, nameCells)

    formatted_cells = append_to_nested_list(formatted_cells, nameCells)
    formatted_cells = append_to_nested_list(formatted_cells, plasmidOriginCells)
    formatted_cells = append_to_nested_list(formatted_cells, restOriginCells)

    set_cells = []
    set_cells = generate_nested_list(set_cells, nameCells)
    set_cells = append_to_nested_list(set_cells, nameCells)
    set_cells = append_to_nested_list(set_cells, setInfoCells)

    print(set_cells)
    add_to_database(formatted_cells, set_cells)


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


def add_to_database(cells, set_cells):
    db = "sqlite:///PBase.db"

    create_table(db)
    connection = create_connection("PBase.db")

    connection.executemany("""
                           
                           INSERT INTO 
                           plasmid(name, plasmid_origin, dna_sequence,size, benchling)
                           VALUES(?,?,?,?,?)""", cells)

    connection.executemany("""

                            INSERT INTO
                            plasmid_set(name, promoter_set1, rbs_set1, goi_set1, terminator_set1,
                            promoter_set2, rbs_set2, goi_set2, terminator_set2,
                            promoter_set3, rbs_set3, goi_set3, terminator_set3)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                            """, set_cells)
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
        Column('dna_sequence', String),
        Column('size', String),
        Column('benchling', String)
    )

    plasmid_set = Table(
        'plasmid_set', meta,
        Column('name', String, primary_key=True),
        Column('promoter_set1', String),
        Column('rbs_set1', String),
        Column('goi_set1', String),
        Column('terminator_set1', String),
        Column('promoter_set2', String),
        Column('rbs_set2', String),
        Column('goi_set2', String),
        Column('terminator_set2', String),
        Column('promoter_set3', String),
        Column('rbs_set3', String),
        Column('goi_set3', String),
        Column('terminator_set3', String)
    )
    meta.create_all(engine)


# Enable the script to be run from the command line
if __name__ == "__main__":
    read()
