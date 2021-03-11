import EBase
import PBase


def main():
    while True:
        input = ui_select_database()
        if input.lower() == 'ebase':
            read_to_ebase()
        elif input.lower() == 'pbase':
            read_to_pbase()
        else:
            break

def ui_select_database():
    database = input("Enter the desired database (EBase/PBase): ")
    return database

def read_to_pbase():
    file = input("Enter the file name: ")
    lastRow = input("Enter the id of the last row: ")
    PBase.read(file, lastRow)


def read_to_ebase():
    file = input("Enter the file name: ")
    EBase.read(file)


# Enable the script to be run from the command line
if __name__ == "__main__":
    main()
