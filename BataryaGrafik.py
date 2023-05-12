from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QTableWidget, QTableWidgetItem,QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
import json
import plotly as py
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
import numpy as np
import pandas as pd
from plotly.offline import  iplot, plot
from collections import Counter
from matplotlib.figure import Figure


logData = pd.read_csv("log.csv")

logDf = pd.DataFrame(logData) # DataFrame haline getirip logDf ye atadım 
logDf = logDf.dropna() # Boş değerleri sildim
logDf = logDf.applymap(lambda x: None if x == 0 else x) # DataFrame içerisindeki tüm 0 değerlerini siler


string_columns = logDf.select_dtypes(include=['object']).columns
logDf = logDf.drop(string_columns, axis=1)

string_columns = logDf.select_dtypes(include=['bool']).columns
logDf = logDf.drop(string_columns, axis=1)

logDf = logDf.drop(['UUID', 'batteries__uuid'], axis=1)

logDf = logDf.astype(float)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

logDf = pd.DataFrame(logData) # DataFrame haline getirip logDf ye atadım
logDf = logDf.dropna() # Boş değerleri sildim
logDf = logDf.applymap(lambda x: None if x == 0 else x) # DataFrame içerisindeki tüm 0 değerlerini siler

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

string_columns = logDf.select_dtypes(include=['object']).columns
logDf = logDf.drop(string_columns, axis=1)

string_columns = logDf.select_dtypes(include=['bool']).columns
logDf = logDf.drop(string_columns, axis=1)

logDf = logDf.drop(['UUID', 'batteries__uuid'], axis=1)

logDf = logDf.astype(float)


def detect_outliers(logDf,features):
    outlier_indices = []
    
    for c in features:
        # 1st quartile
        Q1 = np.percentile(logDf[c],25)
        # 3rd quartile
        Q3 = np.percentile(logDf[c],75)
        
        # IQR
        IQR = Q3 - Q1
        # Outlier step
        outlier_step = IQR * 1.5
        # detect outlier and their indeces
        outlier_list_col = logDf[(logDf[c] < Q1 - outlier_step) | (logDf[c] > Q3 + outlier_step)].index
        # store indeces
        outlier_indices.extend(outlier_list_col)
    
    outlier_indices = Counter(outlier_indices)
    multiple_outliers = list(i for i, v in outlier_indices.items() if v > 2)
    
    return multiple_outliers


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


max_voltage = logDf["batteries__Voltage"].max()
ort_voltage = logDf["batteries__Voltage"] / max_voltage

max_temp = logDf["batteries__temp"].max()
ort_temp = logDf["batteries__temp"]/max_temp

max_current = logDf["batteries__current"].max()
ort_current = logDf["batteries__current"]/max_current

columnA = dict(zip(logDf.columns, range(len(logDf.columns))))


#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

grafikler1 = {              
    'Correlation': 1,
    'Line Chart': 2,
    'Histogram Plot': 3
}
grafikler2 = {              
    'Line Chart': 1,    
    'Scatter Plot': 2,
    'Bar Chart': 3,
    'Strip Plot': 4,
    'Joint Plot': 5,
    'Count Plot': 6,
    'KDE Plot': 7
}
grafikler3 = {
    '3D Scatter': 1,
    'Line Plot': 2
}

logs=[]

#------------------------------------------------------------------------------------------------ PyQt TASARIMININ YAPILMASI ------------------------------------------------------------------------------------------------

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        self.boyut= 3
        self.grafikDeger=3
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1404, 752)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);\n")     
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_left_bar = QtWidgets.QFrame(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_left_bar.sizePolicy().hasHeightForWidth())
        self.frame_left_bar.setSizePolicy(sizePolicy)
        self.frame_left_bar.setMinimumSize(QtCore.QSize(320, 734))
        self.frame_left_bar.setMaximumSize(QtCore.QSize(247, 734))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 255, 223))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 255, 175))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 170, 84))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 191))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 255, 223))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 255, 175))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 170, 84))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 191))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(213, 255, 223))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(149, 255, 175))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(56, 170, 84))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(42, 127, 63))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 255, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipText, brush)
        self.frame_left_bar.setPalette(palette)
        self.frame_left_bar.setAutoFillBackground(False)
        self.frame_left_bar.setStyleSheet("background-color: rgb(217, 217, 217);\n"
"\n"
"border-radius: 30px;\n"
"\n"
"  -webkit-box-shadow: 0px 1px 3px #000000;\n"
"  -moz-box-shadow: 0px 1px 3px #000000;\n"
"  box-shadow: 0px 1px 3px #000000;")
        self.frame_left_bar.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_left_bar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_left_bar.setObjectName("frame_left_bar")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_left_bar)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_icon = QtWidgets.QLabel(parent=self.frame_left_bar)
        self.label_icon.setMinimumSize(QtCore.QSize(100, 100))
        self.label_icon.setMaximumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setKerning(True)
        self.label_icon.setFont(font)
        self.label_icon.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.label_icon.setStyleSheet("border-radius:10px;\n"
"")
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap("anayurt-icon.png"))
        self.label_icon.setScaledContents(True)
        self.label_icon.setWordWrap(False)
        self.label_icon.setIndent(-1)
        self.label_icon.setOpenExternalLinks(False)
        self.label_icon.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard)
        self.label_icon.setObjectName("label_icon")
        self.verticalLayout.addWidget(self.label_icon, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout.addLayout(self.verticalLayout_11)
        self.frame_9 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_9.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_9.setObjectName("frame_9")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_extent_column_number = QtWidgets.QLabel(parent=self.frame_9)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_extent_column_number.setFont(font)
        self.label_extent_column_number.setObjectName("label_extent_column_number")
        self.verticalLayout_10.addWidget(self.label_extent_column_number)
        self.lineEdit_column_number = QtWidgets.QLineEdit(parent=self.frame_9)
        self.lineEdit_column_number.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"\n"
"padding: 2,5px 20px 2,5px 20px;\n"
"\n"
"font-size: 12px;\n"
"")
        self.lineEdit_column_number.setObjectName("lineEdit_column_number")
        self.verticalLayout_10.addWidget(self.lineEdit_column_number)
        self.verticalLayout.addWidget(self.frame_9)
        self.frame_8 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_8.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.pushButton_boyut_ekle = QtWidgets.QPushButton(parent=self.frame_8)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.pushButton_boyut_ekle.setFont(font)
        self.pushButton_boyut_ekle.setStyleSheet("QPushButton {\n"
"  border-radius: 25px;\n"
"  color: #000000;\n"
"background-color: rgb(229, 239, 234);\n"
"\n"
"border-radius: 10px;\n"
"\n"
"padding: 10px 6px 6px 10px;\n"
"\n"
"font: 80 10pt \"Segoe UI Semibold\";\n"
"\n"
"text-align: center;\n"
"\n"
"box-shadow: blue 5px 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #bfc7c3;\n"
"\n"
"}")
        self.pushButton_boyut_ekle.setObjectName("boyut_ekle")
        self.horizontalLayout_4.addWidget(self.pushButton_boyut_ekle)
        self.verticalLayout.addWidget(self.frame_8)
        self.frame_4 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_4.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_column_number_1 = QtWidgets.QLabel(parent=self.frame_4)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_column_number_1.setFont(font)
        self.label_column_number_1.setObjectName("label_column_number_1")
        self.verticalLayout_4.addWidget(self.label_column_number_1)
        self.comboBox_column_number_1 = QtWidgets.QComboBox(parent=self.frame_4)
        self.comboBox_column_number_1.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"\n"
"padding: 2,5px 20px 2,5px 20px;\n"
"\n"
"font-size: 12px;\n"
"")
        self.comboBox_column_number_1.setObjectName("comboBox_column_number_1")
        self.verticalLayout_4.addWidget(self.comboBox_column_number_1)
        self.verticalLayout.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_column_number_2 = QtWidgets.QLabel(parent=self.frame_5)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_column_number_2.setFont(font)
        self.label_column_number_2.setObjectName("label_column_number_2")
        self.verticalLayout_5.addWidget(self.label_column_number_2)
        self.comboBox_column_number_2 = QtWidgets.QComboBox(parent=self.frame_5)
        self.comboBox_column_number_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"\n"
"padding: 2,5px 20px 2,5px 20px;\n"
"\n"
"font-size: 12px;\n"
"")
        self.comboBox_column_number_2.setObjectName("comboBox_column_number_2")
        self.verticalLayout_5.addWidget(self.comboBox_column_number_2)
        self.verticalLayout.addWidget(self.frame_5)
        self.frame_10 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_10.setObjectName("frame_10")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_column_number_3 = QtWidgets.QLabel(parent=self.frame_10)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_column_number_3.setFont(font)
        self.label_column_number_3.setObjectName("label_column_number_3")
        self.verticalLayout_6.addWidget(self.label_column_number_3)
        self.comboBox_column_number_3 = QtWidgets.QComboBox(parent=self.frame_10)
        self.comboBox_column_number_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"\n"
"padding: 2,5px 20px 2,5px 20px;\n"
"\n"
"font-size: 12px;\n"
"")
        self.comboBox_column_number_3.setObjectName("comboBox_column_number_3")
        self.verticalLayout_6.addWidget(self.comboBox_column_number_3)
        self.verticalLayout.addWidget(self.frame_10)
        self.frame_6 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_6.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_plot_name = QtWidgets.QLabel(parent=self.frame_6)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_plot_name.setFont(font)
        self.label_plot_name.setAutoFillBackground(False)
        self.label_plot_name.setObjectName("label_plot_name")
        self.verticalLayout_7.addWidget(self.label_plot_name)
        self.comboBox_plot_name = QtWidgets.QComboBox(parent=self.frame_6)
        self.comboBox_plot_name.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"\n"
"padding: 2,5px 20px 2,5px 20px;\n"
"\n"
"font-size: 12px;\n"
"")
        self.comboBox_plot_name.setObjectName("comboBox_plot_name")
        self.verticalLayout_7.addWidget(self.comboBox_plot_name)
        self.verticalLayout.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_7.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        
        self.pushButton_draw_plot = QtWidgets.QPushButton(parent=self.frame_7)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.pushButton_draw_plot.setFont(font)
        self.pushButton_draw_plot.setStyleSheet("QPushButton {\n"
"  border-radius: 29px;\n"
"  color: #000000;\n"
"  font-size:  55 13pt \"Inter\";\n"
"  background: #E5EFEA;\n"
"  padding: 24px 24px 24px 24px;\n"
"  border-shadow: 0px 1px 3px #000000;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"  text-decoration: none;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #bfc7c3;\n"
"\n"
"}")
        self.pushButton_draw_plot.setObjectName("pushButton_draw_plot")
        self.horizontalLayout_10.addWidget(self.pushButton_draw_plot)
        self.verticalLayout.addWidget(self.frame_7)

        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout.addLayout(self.verticalLayout_9)
        self.horizontalLayout.addWidget(self.frame_left_bar)
        self.frame_right_bar = QtWidgets.QFrame(parent=self.centralwidget)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(212, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(85, 127, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(217, 217, 217))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipText, brush)
        self.frame_right_bar.setPalette(palette)
        self.frame_right_bar.setAutoFillBackground(False)  
        self.frame_right_bar.setStyleSheet("background-color:rgb(217, 217, 217);\n"
"\n"
"border-radius: 30px;")
        self.frame_right_bar.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_right_bar.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_right_bar.setObjectName("frame_right_bar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_right_bar)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_right_bar_top = QtWidgets.QFrame(parent=self.frame_right_bar)
        self.frame_right_bar_top.setStyleSheet("background-color: rgb(121, 140, 164);\n"
"\n"
"border-radius: 20px;")
        self.frame_right_bar_top.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_right_bar_top.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_right_bar_top.setObjectName("frame_right_bar_top")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_right_bar_top)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.frame_right_bar_top)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"background-color: rgb(255, 255, 255);\n"
"\n"
"border-radius: 10px;\n"
"\n"
"padding: 10px 6px 6px 10px;\n"
"\n"
"font: 80 10pt \"Segoe UI Semibold\";\n"
"\n"
"text-align: center;\n"
"\n"
"box-shadow: blue 5px 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #bfc7c3;\n"
"\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.frame_right_bar_top)
        self.pushButton_5.setStyleSheet("QPushButton{\n"
"background-color: rgb(255, 255, 255);\n"
"\n"
"border-radius: 10px;\n"
"\n"
"padding: 10px 6px 6px 10px;\n"
"\n"
"font: 80 10pt \"Segoe UI Semibold\";\n"
"\n"
"text-align: center;\n"
"\n"
"box-shadow: blue 5px 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #bfc7c3;\n"
"\n"
"}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_3.addWidget(self.pushButton_5)
        self.label_title = QtWidgets.QLabel(parent=self.frame_right_bar_top)
        self.label_title.setMinimumSize(QtCore.QSize(173, 0))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.label_title.setFont(font)
        self.label_title.setFocusPolicy(QtCore.Qt.FocusPolicy.TabFocus)
        self.label_title.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.label_title.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 75 16pt \"MS Shell Dlg 2\";\n"
"align: center;\n"
"padding: 10px 6px 6px 10px;\n"
"")
        self.label_title.setObjectName("label_title")
        self.horizontalLayout_3.addWidget(self.label_title, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.frame_right_bar_top)
        self.pushButton_6.setStyleSheet("QPushButton{\n"
"background-color: rgb(255, 255, 255);\n"
"\n"
"border-radius: 10px;\n"
"\n"
"padding: 10px 6px 6px 10px;\n"
"\n"
"font: 80 10pt \"Segoe UI Semibold\";\n"
"\n"
"text-align: center;\n"
"\n"
"box-shadow: blue 5px 5px;\n"
"\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"background-color: #bfc7c3;\n"
"\n"
"}")
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_3.addWidget(self.pushButton_6)

        self.pushButton_7 = QtWidgets.QPushButton(parent=self.frame_right_bar_top)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)        
        sizePolicy.setHeightForWidth(self.pushButton_7.sizePolicy().hasHeightForWidth())
        self.pushButton_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI Semibold")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"\n"
"background-color: rgb(255, 0, 1);\n"
"\n"
"font: 80 10pt \"Segoe UI Semibold\";\n"
"\n"
"border-radius: 10px;\n"
"\n"
"padding: 10px 6px 6px 10px;\n"
"\n"
"text-align: center;\n"
"}\n"
"\n"
"QPushButton:pressed{\n""background-color: #bfc7c3;\n""\n"
"}\n"
"")

        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_3.addWidget(self.pushButton_7)
        self.verticalLayout_2.addWidget(self.frame_right_bar_top, 0, QtCore.Qt.AlignmentFlag.AlignTop)
        self.frame_right_bar_center = QtWidgets.QFrame(parent=self.frame_right_bar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_right_bar_center.sizePolicy().hasHeightForWidth())
        self.frame_right_bar_center.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))  
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(108, 108, 108))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 106, 106))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        self.frame_right_bar_center.setPalette(palette)
        self.frame_right_bar_center.setAutoFillBackground(False)
        self.frame_right_bar_center.setStyleSheet("background-color:rgb(240, 240, 240)")
        self.frame_right_bar_center.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_right_bar_center.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_right_bar_center.setObjectName("frame_right_bar_center")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_right_bar_center)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2.addWidget(self.frame_right_bar_center)
        self.horizontalLayout.addWidget(self.frame_right_bar)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.grafik_gorsel = QtWidgets.QLabel(parent=self.frame_right_bar_center)
        self.table_widget = QtWidgets.QTableWidget(parent= self.frame_right_bar_center)
        self.grafik_widget = QtWidgets.QLabel(parent= self.frame_right_bar_center)
        self.column_info_goster = QtWidgets.QLabel(parent= self.frame_right_bar_center)

        self.grafik_gorsel.setHidden(True) # grafik değerini gizle
        self.table_widget.setHidden(True) # ana tabloyu gizle
        self.grafik_widget.setHidden(True) # grafikleri gizle
        self.column_info_goster.setHidden(True) #column info gizle


    def column_info(self):

        self.grafik_gorsel.setHidden(False) #grafik değerini göster
        self.table_widget.setHidden(True) # tabloyu gizle
        self.grafik_widget.setHidden(True) # grafikleri gizle

        # Öğenin minimum boyutu 1050x600 olarak ayarlanıyor
        self.grafik_gorsel.setMinimumSize(QtCore.QSize(1050,655))
        # Öğenin maksimum boyutu ayarlanıyor
        self.grafik_gorsel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        # Öğenin içeriği "anayurt-icon.png" dosyasından yükleniyor
        self.grafik_gorsel.setPixmap(QtGui.QPixmap("column_info.png"))
        # Öğenin içeriği boyutuna göre ölçeklendiriliyor
        self.grafik_gorsel.setScaledContents(True)
        # Öğenin dış bağlantıları açılmıyor     
        self.grafik_gorsel.setOpenExternalLinks(False)
        # Öğeye "grafik_gorsel" ismi atanıyor
        self.grafik_gorsel.setObjectName("column_info")




    
    def tablo_tikla(self):
        self.table_widget.setHidden(False) # tablo değerini göster
        self.grafik_gorsel.setHidden(True) # grafik değerini gizle
        self.grafik_widget.setHidden(True) # grafikleri gizle
        
        self.table_widget.setGeometry(QtCore.QRect(10, 10, 1050, 655))

        # Tablo boyutunu ayarla
        self.table_widget.setRowCount(len(logDf))
        self.table_widget.setColumnCount(len(logDf.columns))

        # Sütun başlıklarını ayarla
        self.table_widget.setHorizontalHeaderLabels(logDf.columns)

        # Tabloyu doldur
        for i, row in logDf.iterrows():
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.table_widget.setItem(i, j, item)


         # QLabel öğesi oluşturuluyor, bu öğe frame_right_bar_center öğesinin alt öğesi olarak atanıyor
        self.grafik_gorsel = QtWidgets.QLabel(parent=self.frame_right_bar_center)
    def grafik_goster(self):

        self.grafik_gorsel.setHidden(False) #grafik değerini göster
        self.table_widget.setHidden(True) # tabloyu gizle
        self.grafik_widget.setHidden(True) # grafikleri gizle

        # Öğenin minimum boyutu 1050x600 olarak ayarlanıyor
        self.grafik_gorsel.setMinimumSize(QtCore.QSize(1050,655))
        # Öğenin maksimum boyutu ayarlanıyor
        self.grafik_gorsel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        # Öğenin içeriği "anayurt-icon.png" dosyasından yükleniyor
        self.grafik_gorsel.setPixmap(QtGui.QPixmap("grafik-tablosu.png"))
        # Öğenin içeriği boyutuna göre ölçeklendiriliyor
        self.grafik_gorsel.setScaledContents(True)
        # Öğenin dış bağlantıları açılmıyor     
        self.grafik_gorsel.setOpenExternalLinks(False)
        # Öğeye "grafik_gorsel" ismi atanıyor
        self.grafik_gorsel.setObjectName("grafik_gorsel")

#-------------------------------------------------------------------------------------Buradan İtibaren Değişim ve İndirgemeler Yapıldı------------------------------------------------------------------------------#
  
#Kullanıcının girdiği toplam boyut sayısını bu kısımda alıyoruuz
    def boyut_al(self):
        self.boyut = int(self.lineEdit_column_number.text()) #kullanıcının boyut olarak girdiği değer
        print('Boyut= ', self.boyut)
        self.combobox_ayarla()

    def combobox_ayarla(self):
        _translate = QtCore.QCoreApplication.translate

        self.comboBox_column_number_1.clear()
        self.comboBox_column_number_2.clear()
        self.comboBox_column_number_3.clear()
        self.comboBox_plot_name.clear()
        
        if self.boyut == 1:
            self.comboBox_column_number_1.addItems(columnA.keys())
            
            self.comboBox_plot_name.addItems(grafikler1.keys())
            
        elif self.boyut == 2:
            self.comboBox_column_number_1.addItems(columnA.keys())
            self.comboBox_column_number_2.addItems(columnA.keys())

            self.comboBox_plot_name.addItems(grafikler2.keys())

        elif self.boyut == 3:
            self.comboBox_column_number_1.addItems(columnA.keys())
            self.comboBox_column_number_2.addItems(columnA.keys())
            self.comboBox_column_number_3.addItems(columnA.keys())

            self.comboBox_plot_name.addItems(grafikler3.keys())

        else:
            self.comboBox_column_number_1.setItemText(0, _translate("MainWindow", "   "))
            self.comboBox_column_number_2.setItemText(0, _translate("MainWindow", "   "))
            self.comboBox_column_number_3.setItemText(0, _translate("MainWindow", "   "))

            self.comboBox_plot_name.setItemText(0, _translate("MainWindow", " "))

    def grafik_ciz(self):
        self.grafik_widget.setHidden(False) # grafikleri gizle
        self.grafik_gorsel.setHidden(True) # grafik değerini gizle
        self.table_widget.setHidden(True) # tablo değerini göster

        self.deger1_column = self.comboBox_column_number_1.currentText()
        self.deger2_column = self.comboBox_column_number_2.currentText()
        self.deger3_column = self.comboBox_column_number_3.currentText()
        self.grafikDeger = self.comboBox_plot_name.currentText()
        self.grafik_widget.setObjectName("grafik_widget")
  
        if self.boyut==1:
                grDgr1 = grafikler1[self.grafikDeger]
                dgr1 = columnA[self.deger1_column]
                firstColumn = list(columnA.keys())[dgr1]
                sirali = logDf.sort_values(by=[firstColumn], ascending=False, ignore_index=True)
                columnName1 = logDf[firstColumn].name

        # ---Grafikleri Ekrana Yazdırma---

                # Correlation
                if grDgr1 == 1:
                    fig, ax = plt.subplots(figsize=(20, 12))  #Tablonun boyutunu belirliyor
                    sns.heatmap(logDf.corr(), #correlation değerlerini alır
                          annot=True, #Saydamlık saplayarak yazıların gözükmesini sağlar
                         linewidths=.5, #her bir değer arasındaki çizgilerin kalınlığını veriyor
                          fmt= '.2f', #kaç sıfır olacağını belirler
                          ax=ax)
                    plt.title('Correlation')

                    self.grafik_widget.setFixedSize(1400, 700)
                    plt.savefig("graphic-outputs/" + 'Ceorelation Plot.png', dpi=70)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + 'Ceorelation Plot.png'))
                   
                # Line Chart
                elif grDgr1 == 2:
                    fig, ax = plt.subplots(figsize=(20, 12))

                    logDf.iloc[:, dgr1].plot(kind = 'line', #Türü line olacak
                               color = 'green', # çizgi rengi
                               label = columnName1, #çizginin adı
                               linewidth=1, #çizginin kalınlığı
                              alpha = 0.5, #saydamlık
                               grid = False, #arkaplan çizgileri
                              linestyle = ':')
                    plt.legend(loc='upper right' ) # legend ın konumu
                    plt.xlabel('x axis') # x eksenindeki label adı
                    plt.ylabel('y axis') #y eksenindeki label adı
                    plt.title(columnName1 + ' Verisinin Line Grafiği', fontsize=14) #plotun başlığı

                    self.grafik_widget.setFixedSize(1400, 700)
                    plt.savefig("graphic-outputs/" + columnName1 + ' Line Plot.png', dpi=70)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + ' Line Plot.png'))


                # Histogram Plot
                elif grDgr1 == 3:
                    fig, ax = plt.subplots(figsize=(20, 12) )
                    sns.histplot(x=logDf.columns[dgr1], data=logDf, ax=ax)
                    plt.xticks(rotation= 90)
                    plt.title(columnName1 + ' Verisinin Histogram Grafiği', fontsize=14) #plotun başlığı

                    self.grafik_widget.setFixedSize(1400, 700)
                    plt.savefig("graphic-outputs/" + columnName1 + ' Histogram Plot.png', dpi=70)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + ' Histogram Plot.png'))

                else:
                    print('hatalı veri')
                
        # 2 Adet Column
        elif self.boyut == 2:
                grDgr2 = grafikler2[self.grafikDeger]
                dgr1 = columnA[self.deger1_column]
                dgr2 = columnA[self.deger2_column]
                firstColumn = list(columnA.keys())[dgr1]
                sirali = logDf.sort_values(by=[firstColumn], ascending=False, ignore_index=True)
                secondColumn = list(columnA.keys())[dgr2]
                columnName1 = logDf[firstColumn].name
                columnName2 = logDf[secondColumn].name

                # Line Chart
                if grDgr2 == 1:
                    fig, ax = plt.subplots(figsize=(20, 10) )

                    logDf.iloc[:, dgr1].plot(kind = 'line', #Türü line olacak
                                color = 'green', # çizgi rengi
                                label = columnName1, #çizginin adı
                                linewidth=1, #çizginin kalınlığı
                                alpha = 0.5, #saydamlık
                                grid = False, #arkaplan çizgileri
                                linestyle = ':',ax=ax)
                    logDf.iloc[:, dgr2].plot(kind='line',
                                color = 'red',
                                label = columnName2,
                                linewidth=1, 
                                alpha = 0.5,
                                grid = True, #Grid değeri en son girilen değeri alıyor. 
                                linestyle = '-.',ax=ax)

                    plt.legend(loc='upper right' ) # legend ın konumu
                    plt.xlabel('x axis') # x eksenindeki label adı
                    plt.ylabel('y axis') #y eksenindeki label adı
                    plt.title(columnName1 + '  -  ' + columnName2 + ' Line Grafiği', fontsize=14) #plotun başlığı
                    
                    plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Line Plot.png', dpi=60)                
                    self.grafik_widget.setFixedSize(1200, 500)
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Line Plot.png'))

                # Scatter Plot
                elif grDgr2 == 2:
                    fig, ax = plt.subplots(figsize=(20, 10))

                    logDf.plot(kind='scatter', x=dgr1, y=dgr2, alpha=0.5, color='red', figsize=(20,10), ax=ax)
                    plt.xlabel(logDf.columns[dgr1])
                    plt.ylabel(logDf.columns[dgr2])
                    plt.title(columnName1 + '  -  ' + columnName2 + ' Scatter Plot', fontsize=14)

                    plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Scatter Plot.png', dpi=60)                
                    self.grafik_widget.setFixedSize(1200, 500)
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Scatter Plot.png'))

                # Bar Chart
                elif grDgr2 == 3:
                    fig, ax = plt.subplots(figsize=(20, 12) )
                    sns.barplot(x=sirali.index , y=sirali.columns[dgr1], data=sirali, ax=ax)
                    plt.xticks(rotation= 90)
                    plt.title(columnName1 + '  -  ' + columnName2 + ' Bar Grafiği', fontsize=14)

                    plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Bar Plot.png', dpi=60)                
                    self.grafik_widget.setFixedSize(1400, 700)
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Bar Plot.png'))

                # Strip Plot
                elif grDgr2 == 4:
                    fig, ax = plt.subplots(figsize=(22, 13) ) # Grafik Boyutu

                    ax.set_title('{} - {} Scatter Plot'.format(firstColumn, secondColumn), fontsize=20) # Grafiğin başlığı
                    sns.stripplot(data=logDf, x=firstColumn, y=secondColumn, ax=ax)
                    ax.set_xlabel(firstColumn, fontsize=12)
                    ax.set_ylabel(secondColumn, fontsize=12)
                    plt.xticks(rotation= 90)

                    self.grafik_widget.setFixedSize(1400, 700)
                    plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Strip Plot.png', dpi=50)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Strip Plot.png'))

                #Joint Plot
                elif grDgr2 == 5:
                    fig, ax = plt.subplots(figsize=(20, 12))
                    
                    grafik = sns.jointplot(x=firstColumn, y=secondColumn, data=logDf)
                    grafik.plot(sns.scatterplot, sns.histplot)

                    self.grafik_widget.setFixedSize(1400, 700)
                    plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Joint Plot.png', dpi=100)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Joint Plot.png'))
            
                # Count Plot
                elif grDgr2 == 6:
                    fig, ax = plt.subplots(figsize=(20, 12) )
                    sns.set(font_scale=0.5)
                    sns.countplot( y = logDf.columns[dgr1], data=logDf,ax=ax)
                    plt.title(columnName1 + '  -  ' + columnName2 + ' Count Plot', fontsize=14)

                    plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Count Plot.png', dpi=70)
                    self.grafik_widget.setFixedSize(1400, 750)
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Count Plot.png'))
            

                # KDE Plot
                elif grDgr2 == 7: 
                    fig, ax = plt.subplots(figsize=(20, 12))

                    sns.kdeplot(data=logDf, x= firstColumn, y=secondColumn, maker="kind", fill=True, fontsize=15, ax=ax)
                    plt.title(columnName1 + '  -  ' + columnName2 + ' KDE Plot', fontsize=15)

                    self.grafik_widget.setFixedSize(1200, 600)
                    plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' KDE Plot.png', dpi=60)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' KDE Plot.png'))
                   

        # 3 Adet Column
        elif self.boyut==3:
            grDgr3 = grafikler3[self.grafikDeger]
            dgr1 = columnA[self.deger1_column]
            dgr2 = columnA[self.deger2_column]
            dgr3 = columnA[self.deger3_column]
            firstColumn = list(columnA.keys())[dgr1]
            sirali = logDf.sort_values(by=[firstColumn], ascending=False, ignore_index=True)
            secondColumn = list(columnA.keys())[dgr2]
            thirdColumn = list(columnA.keys())[dgr3]
            columnName1 = logDf[firstColumn].name
            columnName2 = logDf[secondColumn].name
            columnName3 = logDf[thirdColumn].name

            if grDgr3==1:
                trace1 = go.Scatter3d(
                    x = logDf[logDf.columns[dgr1]],
                    y = logDf[logDf.columns[dgr2]],
                    z = logDf[logDf.columns[dgr3]],
                    mode = 'markers',
                    marker = dict(
                        size=10,
                        color='rgb(255,0,0)'
                        )    
                )

                logDff = [trace1]
                layout = go.Layout(
                margin = dict(l = 0, r = 0, b = 0, t = 0)
                )
                fig = go.Figure(data = logDff, layout = layout)
                iplot(fig)

                fig, ax = plt.subplots(figsize=(20, 12))
                self.grafik_widget.setFixedSize(1000, 700)
                plt.savefig("graphic-outputs/" + firstColumn + '  -  ' + secondColumn +'  -  ' + thirdColumn + ' 3D Scatter Plot.png', dpi=70)                
                self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + firstColumn + '  -  ' + secondColumn +'  -  ' + thirdColumn + ' 3D Scatter Plot.png'))
                   
                

            elif grDgr3 == 2:
                fig, ax = plt.subplots(figsize=(20, 12))
                
                logDf.iloc[:, dgr1].plot(kind = 'line', #Türü line olacak
                            color = 'green', # çizgi rengi
                            label = columnName1, #çizginin adı
                            linewidth=1, #çizginin kalınlığı
                            alpha = 0.5, #saydamlık
                            grid = False, #arkaplan çizgileri
                            linestyle = ':')
                logDf.iloc[:, dgr2].plot(kind='line',
                              color = 'red',
                              label = columnName2,
                              linewidth=1, 
                             alpha = 0.5,
                            grid = True, #Grid değeri en son girilen değeri alıyor. 
                            linestyle = '-.')
                logDf.iloc[:, dgr3].plot(kind='line',
                              color = 'blue',
                              label = columnName3,
                              linewidth=1, 
                             alpha = 0.5,
                            grid = True, #Grid değeri en son girilen değeri alıyor. 
                            linestyle = '-.')
                plt.legend(loc='upper right' ) # legend ın konumu
                plt.xlabel('x axis') # x eksenindeki label adı
                plt.ylabel('y axis') #y eksenindeki label adı
                title=dict(text='{} - {} - {}  Line Plot'.format(firstColumn, secondColumn, thirdColumn), font=dict(size=15))
                
                self.grafik_widget.setFixedSize(1400, 700)
                plt.savefig("graphic-outputs/" + firstColumn + '  -  ' + secondColumn + '  -  ' + thirdColumn + ' 3 Adet Line Plot.png', dpi=70)                
                self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" +  firstColumn + '  -  ' + secondColumn + '  -  ' + thirdColumn +' 3 Adet Line Plot.png'))  
                plt.show()

        else:
            self.grafik_widget(print('Girdiginiz boyut degerinde grafik tanimlanmamistir!!!'))


 # Column Değerleri bu kısımda ekrana yansıtılıyor
 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_extent_column_number.setText(_translate("MainWindow", "Karsilastirilacak toplam sutun sayisini giriniz: "))

        self.label_column_number_1.setText(_translate("MainWindow", "1. Sutun değerini giriniz: "))
        self.label_column_number_2.setText(_translate("MainWindow", "2. Sutun değerini giriniz: "))
        self.label_column_number_3.setText(_translate("MainWindow", "3. Sutun değerini giriniz: "))

# Çizdirilecek olan grafik
        self.label_plot_name.setText(_translate("MainWindow", "Çizdirmek istediğiniz grafiği seçiniz: "))

        self.pushButton_draw_plot.setText(_translate("MainWindow", "Grafiği Çizdir"))
        self.pushButton_draw_plot.clicked.connect(self.grafik_ciz)
        self.pushButton_boyut_ekle.setText(_translate("MainWindow", "Boyut Ekle"))
        self.pushButton_boyut_ekle.clicked.connect(self.boyut_al)        
        self.pushButton_4.setText(_translate("MainWindow", "Veri Tablosu"))
        self.pushButton_4.clicked.connect(self.tablo_tikla)        
        self.pushButton_5.setText(_translate("MainWindow", "Veri Seti Bilgileri"))
        self.pushButton_5.clicked.connect(self.column_info)
        self.label_title.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.label_title.setText(_translate("MainWindow", "Grafik Çizdirme Araci"))
        self.pushButton_6.setText(_translate("MainWindow", "Grafikler"))
        self.pushButton_6.clicked.connect(self.grafik_goster)
        self.pushButton_7.setText(_translate("MainWindow", "Kapat"))
        self.pushButton_7.clicked.connect(MainWindow.close)
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show() 
    sys.exit(app.exec())