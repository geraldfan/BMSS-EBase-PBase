# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:50:47 2021

@author: Gerald
"""

import sqlite3

import openpyxl
from sqlalchemy import create_engine, MetaData, Table, Column, String


def read(file, lastRow, sheet, contributor):
    # read original data from microplate reader
    # file = 'E6-04_plasmid_list.xlsx'

    nameCellsId = ('A3', get_lastRowId('A', lastRow))
    plasmidOriginId = ('B3', get_lastRowId('C', lastRow))
    restOriginId = ('P3', get_lastRowId('V', lastRow))
    setInfoId = ('D3', get_lastRowId('O', lastRow))

    nameCells = get_cells(file, nameCellsId, sheet)
    plasmidOriginCells = get_cells(file, plasmidOriginId, sheet)
    restOriginCells = get_cells(file, restOriginId, sheet)
    setInfoCells = get_cells(file, setInfoId, sheet)

    set_cells = []
    set_cells = generate_nested_list(set_cells, nameCells)
    set_cells = append_set_cells_to_nested_list(set_cells, setInfoCells)

    formatted_cells = []

    formatted_cells = generate_nested_list(formatted_cells, nameCells)

    formatted_cells = append_to_nested_list(formatted_cells, nameCells)
    formatted_cells = append_to_nested_list(formatted_cells, plasmidOriginCells)
    formatted_cells = append_value_to_nested_list(formatted_cells, contributor)
    formatted_cells = append_set_to_nested_list(formatted_cells, set_cells)
    formatted_cells = append_to_nested_list(formatted_cells, restOriginCells)

    add_to_database(formatted_cells)


def read_entry(name, location, plasmid_origin_antibiotics, contributor, plasmid_details, dna_sequence, size, benchling,
               reference, quantity, remarks, description):
    formatted_cells = []
    formatted_cells = generate_single_nested_list(formatted_cells)
    formatted_cells = append_entries_to_nested_list(formatted_cells, name, location, plasmid_origin_antibiotics,
                                                    contributor, plasmid_details, dna_sequence, size, benchling,
                                                    reference, quantity, remarks, description)

    add_to_database(formatted_cells)


def get_lastRowId(char, lastRow):
    return str(char + lastRow)


def get_cells(file, cellsId, sheet):
    book = openpyxl.load_workbook(file)
    sheet = book[sheet]

    cells = sheet[cellsId[0]: cellsId[1]]

    return cells


def create_set_dict(cells, row):
    row_set_dict = {}
    set1 = []
    set2 = []
    set3 = []
    set1_nested = {}
    set2_nested = {}
    set3_nested = {}

    for i in range(len(cells[row])):
        if i <= 3:
            set1_nested = parse_set(i, set1_nested, cells, row)
            if i == 3:
                set1.append(set1_nested)
        elif i <= 7:
            set2_nested = parse_set(i, set2_nested, cells, row)
            if i == 7:
                set2.append(set2_nested)
        elif i <= 11:
            set3_nested = parse_set(i, set3_nested, cells, row)
            if i == 11:
                set3.append(set3_nested)
    for variable in ["set1", "set2", "set3"]:
        row_set_dict[variable] = eval(variable)
    return row_set_dict


def parse_set(i, set_nested, cells, row):
    if i % 4 == 0:
        set_nested['Promoter'] = cells[row][i].value
    elif i % 4 == 1:
        set_nested['RBS'] = cells[row][i].value
    elif i % 4 == 2:
        set_nested['GOI'] = cells[row][i].value
    elif i % 4 == 3:
        set_nested['Terminator'] = cells[row][i].value

    return set_nested


def generate_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        formatted_cells.append([])

    return formatted_cells


def generate_single_nested_list(formatted_cells):
    formatted_cells.append([])
    return formatted_cells


def append_to_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        for k in range(len(cells[0])):
            formatted_cells[i].append(cells[i][k].value)

    return formatted_cells


def append_entries_to_nested_list(formatted_cells, name, location, plasmid_origin_antibiotics, contributor,
                                  plasmid_details, dna_sequence,
                                  size, benchling, reference, quantity, remarks, description):
    formatted_cells[0].append(name)
    formatted_cells[0].append(location)
    formatted_cells[0].append(plasmid_origin_antibiotics)
    formatted_cells[0].append(contributor)
    formatted_cells[0].append(plasmid_details)
    formatted_cells[0].append(dna_sequence)
    formatted_cells[0].append(size)
    formatted_cells[0].append(benchling)
    formatted_cells[0].append(reference)
    formatted_cells[0].append(quantity)
    formatted_cells[0].append(remarks)
    formatted_cells[0].append(description)

    return formatted_cells


def append_value_to_nested_list(formatted_cells, value):
    for i in range(len(formatted_cells)):
        formatted_cells[i].append(value)

    return formatted_cells


def append_set_cells_to_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        row_dict = create_set_dict(cells, i)
        formatted_cells[i].append(row_dict)

    return formatted_cells


def append_set_to_nested_list(formatted_cells, cells):
    for i in range(len(cells)):
        formatted_cells[i].append(str(cells[i]))

    return formatted_cells


# TODO change method to use sqlalchemy
def add_to_database(cells):
    db = "sqlite:///PBase.db"

    create_table(db)
    connection = create_connection("PBase.db")

    connection.executemany("""
                           
                           INSERT INTO 
                           plasmid(name, location, plasmid_origin_antibiotics, contributor, plasmid_details, dna_sequence,
                           'size(bp)', benchling, 'reference/publication', 'quantity', 'remarks', 'description/purpose')
                           VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", cells)

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
        Column('location', String),
        Column('plasmid_origin_antibiotics', String),
        Column('contributor', String),
        Column('plasmid_details', String),
        Column('dna_sequence', String),
        Column('size(bp)', String),
        Column('benchling', String),
        Column('reference/publication', String),
        Column('quantity', String),
        Column('remarks', String),
        Column('description/purpose', String)
    )

    meta.create_all(engine)


# Enable the script to be run from the command line
if __name__ == "__main__":
    read("E6-04_plasmid_list.xlsx", "62", "AiYing", "Ai Ying")
    read_entry('name', 'location', 'plasmid_origin', '', 'plasmid_details', 'dna', 'size', 'benchling',
               'reference', 'quantity', 'remarks', 'description')
