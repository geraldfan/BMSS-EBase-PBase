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


def read(file, firstRowId, firstColId, lastRowId, lastColId, equipment, model):
    # read original data from microplate reader
    # file = 'cytation_H1_plate1_OD600.xlsx'
    cellsId = (get_cellId(offset_col(firstColId, 2), firstRowId), get_cellId(lastColId, lastRowId))
    timeCellsId = (get_cellId(firstColId, firstRowId), get_cellId(firstColId, lastRowId))
    temperatureCellsId = (
    get_cellId(offset_col(firstColId, 1), firstRowId), get_cellId(offset_col(firstColId, 1), firstRowId))
    filePathsId = ("B4", "B5")
    settingsId = ('A2', 'F2')
    identifierId = ('A2', 'A2')
    data_sheet = 'Data'
    settings_sheet = 'Metadata'

    settingsCells = get_cells(file, settingsId, settings_sheet)
    filePathsCells = get_cells(file, filePathsId, data_sheet)
    cells = get_cells(file, cellsId, data_sheet)
    timeCells = get_cells(file, timeCellsId, data_sheet)
    temperatureCells = get_temperature(temperatureCellsId, file, data_sheet)
    identifier = get_identifier(identifierId, file, settings_sheet)
    equipment = create_dict(equipment, model)
    filePaths = create_file_paths_dict(filePathsCells)

    settings = []
    settings = generate_nested_list(settings, settingsCells)
    settings = append_to_nested_list(settings, settingsCells)
    settings = append_single_value_to_nested_list(settings, str(equipment))
    settings = append_single_value_to_nested_list(settings, str(filePaths))

    values = []
    values = generate_nested_list(values, cells)
    values = append_to_nested_list(values, cells)

    time = []
    time = generate_nested_list(time, timeCells)
    time = append_time_to_nested_list(time, timeCells)

    formatted_cells = []
    formatted_cells = generate_single_nested_list(formatted_cells)
    formatted_cells = append_single_value_to_nested_list(formatted_cells, identifier)
    formatted_cells = append_cells_to_single_nested_list(formatted_cells, time)
    formatted_cells = append_single_value_to_nested_list(formatted_cells, temperatureCells)
    formatted_cells = append_cells_to_single_nested_list(formatted_cells, values)

    add_to_database(formatted_cells)
    add_to_settings(settings)


def offset_col(char, offset):
    return str(chr(ord(char) + offset))


def get_cellId(char, lastRow):
    return str(char + lastRow)


def get_identifier(identifierId, file, sheet):
    book = openpyxl.load_workbook(file)
    sheet = book[sheet]

    cell = sheet[identifierId[0]:identifierId[1]]
    return cell[0][0].value

def create_file_paths_dict(filePathsCells):
    file_paths_dict = create_dict("Experiment", filePathsCells[0][0].value)
    return add_to_dict(file_paths_dict, "Protocol", filePathsCells[1][0].value)

def get_cells(file, cellsId, sheet):
    book = openpyxl.load_workbook(file)
    sheet = book[sheet]

    cells = sheet[cellsId[0]: cellsId[1]]

    return cells


def get_temperature(temperatureId, file, sheet):
    book = openpyxl.load_workbook(file)
    sheet = book[sheet]

    cell = sheet[temperatureId[0]:temperatureId[1]]
    return cell[0][0].value


def create_dict(key, value):
    output_dict = {key: value}
    return output_dict

def add_to_dict(dict, key, value):
    dict[key] = value
    return dict

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


def append_single_value_to_nested_list(formatted_cells, value):
    formatted_cells[0].append(value)

    return formatted_cells


def append_cells_to_single_nested_list(formatted_cells, cells):
    to_append = ''
    for i in range(len(cells)):
        to_append += str(cells[i])
    formatted_cells[0].append(to_append)
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


def append_temperature_to_nested_list(formatted_cells, cells, temperature):
    for i in range(len(cells)):
        formatted_cells[i].append(temperature)

    return formatted_cells


def add_to_database(cells):
    db = "sqlite:///EBase.db"
    create_table(db)
    connection = create_connection("EBase.db")

    connection.executemany("""

                           INSERT INTO
                           data(experimental_id, time, set_temperature, data_values)
                           VALUES(?,?,?,?)""", cells)

    connection.commit()
    connection.close()


def add_to_settings(cells):
    db = "sqlite:///EBase.db"
    create_table(db)
    connection = create_connection("EBase.db")

    connection.executemany("""

                           INSERT INTO
                           settings(experimental_id, measurement, experiment_type, temperature, media, plasmid_name, equipment, filepath )
                           VALUES(?,?,?,?,?,?,?,?)""", cells)

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
        Column('experimental_id', String, primary_key=True),
        Column('time', String),
        Column('set_temperature', String),
        Column('data_values', String)
    )

    settings = Table(
        'settings', meta,
        Column('experimental_id', String, primary_key=True),
        Column('measurement', String),
        Column('experiment_type', String),
        Column('Temperature', String),
        Column('Media', String),
        Column('plasmid_name', String),
        Column('Equipment', String),
        Column('Filepath', String)

    )
    meta.create_all(engine)


# Enable the script to be run from the command line
if __name__ == "__main__":
    read("cytation_H1_plate1.xlsx", "63", "B", "95", "CU", "Microplate reader", "Cytation 5")
