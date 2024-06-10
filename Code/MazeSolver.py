import sys
from PyQt5 import QtWidgets
from Point import *
from BFSPathFinder import *
from ThreadClass import *
from UiMainWindow import *


def main():  # Main function
    app = QtWidgets.QApplication(sys.argv)  # Creating a QApplication instance
    main_window = QtWidgets.QMainWindow()  # Creating a QMainWindow instance
    ui = UiMainWindow()  # Creating an instance of UiMainWindow class
    ui.setupUi(main_window)  # Setting up the user interface
    main_window.show()  # Displaying the main window

    sys.exit(app.exec_())  # Executing the application and exiting the program when done


if __name__ == '__main__':  # Check if the script is being run as the main program
    main()  # Call the main function
