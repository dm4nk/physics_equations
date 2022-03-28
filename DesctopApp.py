from PyQt5.QtWidgets import (QApplication, QMessageBox, QMainWindow, QVBoxLayout, QAction, QFileDialog, QDialog)
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUiType
from sys import argv
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


def main():
    app = QApplication(argv)
    # window = Main()
    # window.showFullScreen() # Start at position full screen
    # window.showMaximized()  # Start position max screen
    app.exec_()

