# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 11:17:39 2021

@author: Gerald
"""

# -*- coding: utf-8 -*-
import re

"""
Created on Thu Feb 25 14:44:13 2021

@author: Gerald
"""

import sqlite3

import openpyxl
from sqlalchemy import create_engine, MetaData, Table, Column, String


def read(file, odFirstRowId, firstColId, odLastRowId, lastColId, gfpFirstRowId, gfpLastRowId,
         rfpFirstRowId, rfpLastRowId, equipment, model, readODWavelengthId, readGFPExcitationEmissionId, readGFPGainId,
         readRFPExcitationEmissionId, readRFPGainId):
    # read original data from microplate reader
    # file = 'cytation_H1_plate1_OD600.xlsx'
    odCellsId = (get_cellId(offset_col(firstColId, 2), odFirstRowId), get_cellId(lastColId, odLastRowId))
    odTimeCellsId = (get_cellId(firstColId, odFirstRowId), get_cellId(firstColId, odLastRowId))
    odTemperatureCellsId = (
        get_cellId(offset_col(firstColId, 1), odFirstRowId), get_cellId(offset_col(firstColId, 1), odFirstRowId))
    gfpCellsId = (get_cellId(offset_col(firstColId, 2), gfpFirstRowId), get_cellId(lastColId, gfpLastRowId))
    gfpTimeCellsId = (get_cellId(firstColId, gfpFirstRowId), get_cellId(firstColId, gfpLastRowId))
    gfpTemperatureCellsId = (
        get_cellId(offset_col(firstColId, 1), gfpFirstRowId), get_cellId(offset_col(firstColId, 1), gfpFirstRowId))
    rfpCellsId = (get_cellId(offset_col(firstColId, 2), rfpFirstRowId), get_cellId(lastColId, rfpLastRowId))
    rfpTimeCellsId = (get_cellId(firstColId, rfpFirstRowId), get_cellId(firstColId, rfpLastRowId))
    rfpTemperatureCellsId = (
        get_cellId(offset_col(firstColId, 1), rfpFirstRowId), get_cellId(offset_col(firstColId, 1), rfpFirstRowId))
    filePathsId = ("B4", "B5")
    procedureCellsId = ("B14", "B21")
    readODId = (readODWavelengthId, readODWavelengthId)
    readGFPId = (readGFPExcitationEmissionId, readGFPGainId)
    readRFPId = (readRFPExcitationEmissionId, readRFPGainId)
    experimentDateAndTimeId = ("B7", "B8")
    settingsId = ('A2', 'F2')
    identifierId = ('A2', 'A2')
    wellId = ('A1', 'CR1')
    wellInfoId = ('A2', 'CR2')
    data_sheet = 'Data'
    settings_sheet = 'Metadata'
    well_sheet = 'Well Information'

    settingsCells = get_cells(file, settingsId, settings_sheet)
    filePathsCells = get_cells(file, filePathsId, data_sheet)
    experimentDateAndTimeCells = get_cells(file, experimentDateAndTimeId, data_sheet)
    procedureCells = get_cells(file, procedureCellsId, data_sheet)
    readGFPCells = get_cells(file, readGFPId, data_sheet)
    readRFPCells = get_cells(file, readRFPId, data_sheet)
    odCells = get_cells(file, odCellsId, data_sheet)
    odTimeCells = get_cells(file, odTimeCellsId, data_sheet)
    odTemperatureCells = get_single_value(odTemperatureCellsId, file, data_sheet)
    gfpCells = get_cells(file, gfpCellsId, data_sheet)
    gfpTimeCells = get_cells(file, gfpTimeCellsId, data_sheet)
    gfpTemperatureCells = get_single_value(gfpTemperatureCellsId, file, data_sheet)
    rfpCells = get_cells(file, rfpCellsId, data_sheet)
    rfpTimeCells = get_cells(file, rfpTimeCellsId, data_sheet)
    rfpTemperatureCells = get_single_value(rfpTemperatureCellsId, file, data_sheet)
    wellCells = get_cells(file, wellId, well_sheet)
    wellInfoCells = get_cells(file, wellInfoId, well_sheet)
    identifier = get_identifier(identifierId, file, settings_sheet)
    equipment = create_dict(equipment, model)
    filePaths = create_file_paths_dict(filePathsCells)
    readODWavelength = get_single_value(readODId, file, data_sheet)


    experimentDateAndTime = create_experiment_date_and_time_dict(experimentDateAndTimeCells)
    readInfo = create_read_info_dict(readODWavelength, readGFPCells, readRFPCells)
    procedure_details = create_procedure_details_dict(procedureCells, readInfo)
    wellsInfo = create_wells_dict(wellCells, wellInfoCells)

    settings = []
    settings = generate_nested_list(settings, settingsCells)
    settings = append_to_nested_list(settings, settingsCells)
    settings = append_single_value_to_nested_list(settings, str(equipment))
    settings = append_single_value_to_nested_list(settings, str(filePaths))
    settings = append_single_value_to_nested_list(settings, str(experimentDateAndTime))
    settings = append_single_value_to_nested_list(settings, str(procedure_details))
    settings = append_single_value_to_nested_list(settings, str(wellsInfo))

    data_values = create_data_dict(odCells, gfpCells, rfpCells)
    time = create_time_dict(odTimeCells, gfpTimeCells, rfpTimeCells)
    temperature = create_temperature_dict(odTemperatureCells, gfpTemperatureCells, rfpTemperatureCells)

    formatted_cells = []
    formatted_cells = generate_single_nested_list(formatted_cells)
    formatted_cells = append_single_value_to_nested_list(formatted_cells, identifier)
    formatted_cells = append_cells_to_single_nested_list(formatted_cells, str(time))
    formatted_cells = append_single_value_to_nested_list(formatted_cells, odTemperatureCells)
    formatted_cells = append_cells_to_single_nested_list(formatted_cells, str(data_values))

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


def create_experiment_date_and_time_dict(experimentDateAndTimeCells):
    experiment_date_and_time_dict = create_dict("Date", experimentDateAndTimeCells[0][0].value.strftime("%d/%m/%Y"))
    return add_to_dict(experiment_date_and_time_dict, "Time",
                       experimentDateAndTimeCells[1][0].value.strftime("%H:%M:%S"))


def create_temperature_dict(odTemperatureCells, gfpTemperatureCells, rfpTemperatureCells):
    temperature_dict = create_dict("OD", odTemperatureCells)
    temperature_dict = add_to_dict(temperature_dict, "GFP", gfpTemperatureCells)
    return add_to_dict(temperature_dict, "RFP", rfpTemperatureCells)


def create_time_dict(odTimeCells, gfpTimeCells, rfpTimeCells):
    odTime = []
    odTime = append_time_to_list(odTime, odTimeCells)
    gfpTime = []
    gfpTime = append_time_to_list(gfpTime, gfpTimeCells)
    rfpTime = []
    rfpTime = generate_nested_list(rfpTime, rfpTimeCells)
    rfpTime = append_time_to_list(rfpTime, rfpTimeCells)
    time_dict = create_dict("OD", odTime)
    time_dict = add_to_dict(time_dict, "GFP", gfpTime)
    return add_to_dict(time_dict, "RFP", rfpTime)


def create_data_dict(odCells, gfpCells, rfpCells):
    odValues = []
    odValues = generate_nested_list(odValues, odCells)
    odValues = append_to_nested_list(odValues, odCells)
    gfpValues = []
    gfpValues = generate_nested_list(gfpValues, gfpCells)
    gfpValues = append_to_nested_list(gfpValues, gfpCells)
    rfpValues = []
    rfpValues = generate_nested_list(rfpValues, rfpCells)
    rfpValues = append_to_nested_list(rfpValues, rfpCells)
    data_dict = create_dict("OD", odValues)
    data_dict = add_to_dict(data_dict, "GFP", gfpValues)
    return add_to_dict(data_dict, "RFP", rfpValues)


def create_read_info_dict(readODWavelength, readGFPCells, readRFPCells):
    read_info_dict = create_dict("OD", create_dict("Wavelength", extract_int_as_string(readODWavelength)))
    gfp_dict = create_fp_dict(readGFPCells)
    read_info_dict = add_to_dict(read_info_dict, "GFP", str(gfp_dict))
    rfp_dict = create_fp_dict(readRFPCells)
    read_info_dict = add_to_dict(read_info_dict, "RFP", str(rfp_dict))
    return read_info_dict


def create_procedure_details_dict(procedureCells, readInfo):
    procedure_details_dict = create_dict("Plate Type", procedureCells[0][0].value)
    procedure_details_dict = add_to_dict(procedure_details_dict, "Set Temperature", procedureCells[2][0].value)
    procedure_details_dict = add_to_dict(procedure_details_dict, "Start Kinetic", procedureCells[5][0].value)
    shake_dict = create_shake_dict(procedureCells)
    procedure_details_dict = add_to_dict(procedure_details_dict, "Shake", str(shake_dict))

    return add_to_dict(procedure_details_dict, "Read", readInfo)

def create_wells_dict(wellCells, wellInfoCells):
    wells_dict = {}
    for i in range(len(wellCells[0])):
        wells_dict = add_to_dict(wells_dict, wellCells[0][i].value, wellInfoCells[0][i].value)

    return wells_dict
def create_shake_dict(procedureCells):
    shake_dict = create_dict("Orbital", procedureCells[6][0].value.replace("Orbital: ", ""))
    return add_to_dict(shake_dict, "Frequency", procedureCells[7][0].value.replace("Frequency: ", ""))


def create_fp_dict(readFPCells):
    excitation_emissions = readFPCells[0][0].value.split(",")
    gfp_dict = create_dict("Excitation", extract_int_as_string(excitation_emissions[0]))
    gfp_dict = add_to_dict(gfp_dict, "Emission", extract_int_as_string(excitation_emissions[1]))
    return add_to_dict(gfp_dict, "Gain", extract_int_as_string(readFPCells[1][0].value))


def get_cells(file, cellsId, sheet):
    book = openpyxl.load_workbook(file)
    sheet = book[sheet]

    cells = sheet[cellsId[0]: cellsId[1]]

    return cells


def extract_int_as_string(string):
    return str(re.search(r'\d+', string).group())


def get_single_value(temperatureId, file, sheet):
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


def append_time_to_list(formatted_cells, cells):
    for i in range(len(cells)):
        formatted_cells.append(cells[i][0].value.strftime("%H:%M:%S"))

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
                           settings(experimental_id, measurement, experiment_type, temperature, media, plasmid_name, 
                           equipment, filepath, date, procedure_details, wells_info )
                           VALUES(?,?,?,?,?,?,?,?,?,?,?)""", cells)

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
        Column('Filepath', String),
        Column('Date', String),
        Column('procedure_details', String),
        Column('wells_info', String)
    )
    meta.create_all(engine)


# Enable the script to be run from the command line
if __name__ == "__main__":
    read("cytation_H1_plate1.xlsx", "63", "B", "95", "CU", "100", "132", "137", "169", "Microplate reader",
         "Cytation 5", "B25", "B31", "B32",
         "B40", "B41")
