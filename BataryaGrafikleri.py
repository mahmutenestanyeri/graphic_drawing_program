from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QTableWidget,QTableWidgetItem,QVBoxLayout,QLabel,QMessageBox,QFileDialog
import plotly as py,matplotlib.pyplot as plt,plotly.graph_objs as go
from numpy import percentile as np
from seaborn import heatmap,histplot,barplot,jointplot,scatterplot,set,countplot,kdeplot,stripplot
import pandas as pd
from plotly.offline import iplot,plot
from collections import Counter
from matplotlib.figure import Figure
import json, csv, os, glob
from sklearn.preprocessing import MinMaxScaler


grafikler1 = {              
                'HeatMap': 1,
                'Line Chart': 2,
                'Histogram Plot': 3,
                'Count Plot': 4
            }
grafikler2 = {              
                'Line Chart': 1,    
                'Scatter Plot': 2,
                'Bar Chart': 3,
                'Strip Plot': 4,
                'Joint Plot': 5,
                'KDE Plot': 6
            }
grafikler3 = {
                '3D Scatter': 1,
                'Line Plot': 2
            }

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        lodData=None
        logDf=None
        logDf_normalized=None
        describe_table=None
        columnA=None
        self.sayac=0
        self.boyut= 3
        self.grafikDeger=3
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 963)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);\n")     
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        plain_text_edit = QtWidgets.QPlainTextEdit()

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
        

#-----------------------
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
        self.label_icon.setMinimumSize(QtCore.QSize(150, 150))
        self.label_icon.setMaximumSize(QtCore.QSize(150, 150))
        font = QtGui.QFont()
        font.setKerning(True)
        self.label_icon.setFont(font)
        self.label_icon.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.label_icon.setStyleSheet("border-radius:10px;\n"
"")
        self.label_icon.setText("")
        self.label_icon.setPixmap(QtGui.QPixmap("anayurt-icon.png"))
        self.label_icon.setStyleSheet("border-radius: 50%;")
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


        self.frame_11 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_11.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")       
        self.pushButton_dosya_ekle = QtWidgets.QPushButton(parent=self.frame_11)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.pushButton_dosya_ekle.setFont(font)
        self.pushButton_dosya_ekle.setStyleSheet("QPushButton {\n"
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
        self.pushButton_dosya_ekle.setObjectName("dosya_ekle")
        self.horizontalLayout_2.addWidget(self.pushButton_dosya_ekle)
        self.verticalLayout.addWidget(self.frame_11)
#--------------------------------

        self.frame_15 = QtWidgets.QFrame(parent=self.frame_left_bar)
        self.frame_15.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")       
        self.pushButton_dosya_ekle_2 = QtWidgets.QPushButton(parent=self.frame_15)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.pushButton_dosya_ekle_2.setFont(font)
        self.pushButton_dosya_ekle_2.setStyleSheet("QPushButton {\n"
"  border-radius: 25px;\n"
"  color: #000000;\n"
"  background-color: rgb(191,199,195);\n"
"  border-radius: 10px;\n"
"  padding: 10px 6px 6px 10px;\n"
"  font: 80 21pt \"Segoe UI Semibold\";\n"
"  color: #003C8C ;\n"
"  text-align: center;\n"
"  box-shadow: blue 5px 5px;\n"
"  border: 1px solid rgb(121, 140, 164); /* Çerçeve rengi */\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"  background-color: #bfc7c3;\n"
"  border-color: #000000; /* Basıldığında çerçeve rengi */\n"
"}")
        self.pushButton_dosya_ekle_2.setObjectName("dosya_ekle")
        self.horizontalLayout_2.addWidget(self.pushButton_dosya_ekle_2)
        self.verticalLayout.addWidget(self.frame_15)
        self.pushButton_dosya_ekle_2.setFixedSize(280, 150)




#--------------------------------
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
        self.pushButton_6.setObjectName("pushButton_8")
        self.horizontalLayout_3.addWidget(self.pushButton_6)


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

        self.pushButton_8 = QtWidgets.QPushButton(parent=self.frame_right_bar_top)
        self.pushButton_8.setStyleSheet("QPushButton{\n"
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
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_3.addWidget(self.pushButton_8)

        self.pushButton_9 = QtWidgets.QPushButton(parent=self.frame_right_bar_top)
        self.pushButton_9.setStyleSheet("QPushButton{\n"
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
        self.pushButton_9.setObjectName("pushButton_9")
        self.horizontalLayout_3.addWidget(self.pushButton_9)

        self.pushButton_10 = QtWidgets.QPushButton(parent=self.frame_right_bar_top)
        self.pushButton_10.setStyleSheet("QPushButton{\n"
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
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_3.addWidget(self.pushButton_10)

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
        self.column_info_goster = QtWidgets.QTableWidget(parent= self.frame_right_bar_center)

        #self.grafik_widget.setGeometry(self.frame_right_bar_center.geometry())
        self.grafik_gorsel.setHidden(True) # grafik değerini gizle
        self.table_widget.setHidden(True) # ana tabloyu gizle
        self.grafik_widget.setHidden(True) # grafikleri gizle
        self.column_info_goster.setHidden(True) #column info gizle

        self.frame_4.setHidden(True) #Sutun 1
        self.frame_5.setHidden(True) #Sutun 2
        self.frame_10.setHidden(True) #Sutun 3
        self.frame_6.setHidden(True) #Grafikler
        self.frame_7.setHidden(True) #Grafik Çizdir
        self.frame_8.setHidden(True) #boyut degeri gir
        self.frame_9.setHidden(True) #boyur degeri buton
        self.frame_11.setHidden(True) #dosya ekle buton
        self.frame_15.setHidden(False) #dosya ekle 2 buton
        self.pushButton_8.setHidden(True) #Yakinlastir
        self.pushButton_9.setHidden(True) #Uzaklastir
        self.pushButton_10.setHidden(True) #Reset

#---------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------

    def dosya_ekle(self):
        global columnA
        global logDf
        global logData

        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.AnyFile)
        file_dialog.setNameFilter("CSV Dosyaları (*.csv *.CSV);;Json Dosyaları (*.json *.JSON)")

        if file_dialog.exec_():
            import re
            selected_files = file_dialog.selectedFiles()
            file_path = selected_files[0]
            # Seçilen dosyayı kullanarak yapmak istediğiniz işlemi burada gerçekleştirebilirsiniz
            print("Seçilen dosya:", file_path)

            dosya_boyutu = os.path.getsize(file_path)

            if file_path.lower().endswith('.csv') and dosya_boyutu > 10000 or file_path.lower().endswith('.json') and dosya_boyutu>2500:

                if file_path.lower().endswith('.csv'):
                    try:
                        logData = pd.read_csv("{}".format(file_path)) # pd.read_csv

                        self.frame_4.setHidden(True) #Sutun 1
                        self.frame_5.setHidden(True) #Sutun 2
                        self.frame_10.setHidden(True) #Sutun 3
                        self.frame_6.setHidden(True) #Grafikler
                        self.frame_7.setHidden(True) #Grafik Çizdir
                        self.frame_8.setHidden(False) #boyut degeri gir
                        self.frame_9.setHidden(False) #boyur degeri buton
                        self.frame_11.setHidden(False) #dosya ekle buton
                        self.frame_15.setHidden(True) #dosya ekle 2 buton


                        print(logData)


                        logDf = pd.DataFrame(logData) # DataFrame haline getirip logDf ye atadım

                        logDf.columns = [re.sub(r'[^a-zA-Z0-9]', '', col) for col in logDf.columns]

                        column_names = logDf.columns.tolist()

                        # İçerikleri aynı olan sütunları bul
                        duplicated_columns = logDf.loc[:, logDf.T.duplicated()].columns.tolist()
                        # İçerikleri aynı olan sütunlardan sadece bir tanesini sil
                        logDf = logDf.drop(columns=duplicated_columns[1:])

                        logDf = logDf.dropna() # Boş değerleri sildim
                        logDf = logDf.applymap(lambda x: None if x == 0.000000 else x) # DataFrame içerisindeki tüm 0 değerlerini siler

                        print("é"*100)
                        print(logDf)

                        string_columns = logDf.select_dtypes(include=['object']).columns
                        logDf = logDf.drop(string_columns, axis=1)

                        string_columns = logDf.select_dtypes(include=['bool']).columns
                        logDf = logDf.drop(string_columns, axis=1)

                        logDf = logDf.astype(float)

                        logDf = logDf.applymap(lambda x: None if x == 0 else x) # DataFrame içerisindeki tüm 0 değerlerini siler

                        string_columns = logDf.select_dtypes(include=['object']).columns
                        logDf = logDf.drop(string_columns, axis=1)

                        string_columns = logDf.select_dtypes(include=['bool']).columns
                        logDf = logDf.drop(string_columns, axis=1)

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

                        columnA = dict(zip(logDf.columns, range(len(logDf.columns))))

                        # Tablodaki verilerin sayısal değerlerini 0-1 arasında sabitleme işlemi
                        # MinMaxScaler nesnesini oluşturma
                        global logDf_normalized
                        scaler = MinMaxScaler()

                        # Verileri normalize etme
                        logDf_normalized = scaler.fit_transform(logDf)

                        # Normalize edilmiş verileri yeni bir DataFrame'e dönüştürme
                        logDf_normalized = pd.DataFrame(logDf_normalized, columns=logDf.columns)

                        # Sayısal değerleri noktadan sonra 4 haneyle sınırlama
                        logDf_normalized = logDf_normalized.round(4)

                        print('-'*100)
                        print(logDf_normalized)

                    except:
                        message_box = QMessageBox()  # Mesaj kutusu oluşturma
                        message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                        message_box.setText("Dosya verileri hatalı!")
                        message_box.setIcon(QMessageBox.Information)
                        message_box.exec_()  # Mesaj kutusunu gösterme
            
    # eğer json dosyası seçilirse 
                elif file_path.lower().endswith('.json'):
                    print ("Hello World/n")
                    try:
                        self.frame_4.setHidden(True) #Sutun 1
                        self.frame_5.setHidden(True) #Sutun 2
                        self.frame_10.setHidden(True) #Sutun 3
                        self.frame_6.setHidden(True) #Grafikler
                        self.frame_7.setHidden(True) #Grafik Çizdir
                        self.frame_8.setHidden(False) #boyut degeri gir
                        self.frame_9.setHidden(False) #boyur degeri buton
                        self.frame_11.setHidden(False) #dosya ekle buton
                        self.frame_15.setHidden(True) #dosya ekle 2 buton

                        #logData = json_load("{}".format(file_path))
                        jsonData =  open("{}".format(file_path), 'r')

                        oku_json = jsonData.read()

                        logData=json.loads(oku_json)

                        logDf=pd.DataFrame(logData)
                        print(logDf)

                        logDf.columns = [re.sub(r'[^a-zA-Z0-9]', '', col) for col in logDf.columns]

                        column_names = logDf.columns.tolist()

                        # İçerikleri aynı olan sütunları bul
                        #ayni_columns = logDf.loc[:, logDf.T.duplicated()].columns.tolist()
                        # İçerikleri aynı olan sütunlardan sadece bir tanesini sil
                        #logDf = logDf.drop(columns=ayni_columns[1:])

                        logDf = logDf.dropna() # Boş değerleri sildim
                        logDf = logDf.applymap(lambda x: None if x == 0 else x) # DataFrame içerisindeki tüm 0 değerlerini siler


                        string_columns = logDf.select_dtypes(include=['object']).columns
                        logDf = logDf.drop(string_columns, axis=1)

                        string_columns = logDf.select_dtypes(include=['bool']).columns
                        logDf = logDf.drop(string_columns, axis=1)


                        logDf = logDf.astype(float)


                        logDf = logDf.applymap(lambda x: None if x == 0 else x) # DataFrame içerisindeki tüm 0 değerlerini siler

                        string_columns = logDf.select_dtypes(include=['object']).columns
                        logDf = logDf.drop(string_columns, axis=1)

                        string_columns = logDf.select_dtypes(include=['bool']).columns
                        logDf = logDf.drop(string_columns, axis=1)

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

                        columnA = dict(zip(logDf.columns, range(len(logDf.columns))))

                        # Tablodaki verilerin sayısal değerlerini 0-1 arasında sabitleme işlemi
                        # MinMaxScaler nesnesini oluşturma
                        scaler = MinMaxScaler()

                        # Verileri normalize etme
                        logDf_normalized = scaler.fit_transform(logDf)

                        # Normalize edilmiş verileri yeni bir DataFrame'e dönüştürme
                        logDf_normalized = pd.DataFrame(logDf_normalized, columns=logDf.columns)

                        # Sayısal değerleri noktadan sonra 4 haneyle sınırlama
                        logDf_normalized = logDf_normalized.round(4)

                        print('-'*100)
                        print(logDf_normalized)

                    except:
                        message_box = QMessageBox()  # Mesaj kutusu oluşturma
                        message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                        message_box.setText("Dosya verileri hatalı!")
                        message_box.setIcon(QMessageBox.Information)
                        message_box.exec_()  # Mesaj kutusunu gösterme

            else:
                message_box = QMessageBox()  # Mesaj kutusu oluşturma
                message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                message_box.setText("Dosya Boyutu Yetersiz!")
                message_box.setIcon(QMessageBox.Information)
                message_box.exec_()  # Mesaj kutusunu gösterme



#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    #Yakinlastir
    def zoom_in(self):
        scale_factor = 1.1  # Yakınlaştırma faktörü
        #self.sayac = self.sayac+1
        print('Yakinlas: '+ str(self.sayac))

        if self.sayac < 3:
            self.sayac = self.sayac+1
            # Mevcut pixmap alınıyor
            pixmap = self.grafik_widget.pixmap()

            # Yeni genişlik ve yükseklik hesaplanıyor
            new_width = int(pixmap.width() * scale_factor)
            new_height = int(pixmap.height() * scale_factor)

            # Pixmap yeniden boyutlandırılıyor
            resized_pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)

            # Pixmap'i QLabel'e set ediyoruz
            self.grafik_widget.setPixmap(resized_pixmap)

        else:
            message_box = QMessageBox()  # Mesaj kutusu oluşturma
            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            message_box.setText("Daha fazla yakınlaştırma işlemi yapılamaz!")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()  # Mesaj kutusunu gösterme

    
    #Uzaklastirma
    def zoom_out(self):   
        scale_factor = 0.9  # uzaklastirma faktörü
        #self.sayac =self.sayac-1
        print('Uzaklastir: '+ str(self.sayac))

        if self.sayac < 4 and self.sayac > 0:
            self.sayac = self.sayac-1
            # Mevcut pixmap alınıyor
            pixmap = self.grafik_widget.pixmap()

            # Yeni genişlik ve yükseklik hesaplanıyor
            new_width = int(pixmap.width() * scale_factor)
            new_height = int(pixmap.height() * scale_factor)

            # Pixmap yeniden boyutlandırılıyor
            resized_pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio)

            # Pixmap'i QLabel'e set ediyoruz
            self.grafik_widget.setPixmap(resized_pixmap)

        else:
            message_box = QMessageBox()  # Mesaj kutusu oluşturma
            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            message_box.setText("Uzaklaştırma işlemi yapılamıyor!")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()  # Mesaj kutusunu gösterme



    def reset_yap(self):
        self.sayac=0
        self.grafik_widget.setFixedSize(1600, 800)
        dosya_listesi = os.listdir("graphic-outputs/")
        dosya_listesi.sort(key=lambda x: os.path.getmtime(os.path.join("graphic-outputs/", x)), reverse=True)
        en_son_eklenen_dosya = dosya_listesi[0]

        # Dosya yolunu oluşturma
        dosya_yolu = os.path.join("graphic-outputs/", en_son_eklenen_dosya)
        self.grafik_widget.setPixmap(QtGui.QPixmap(dosya_yolu))


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def column_info(self):
        self.column_info_goster.setHidden(False) #column_info göster
        self.grafik_gorsel.setHidden(True) #grafik değerini gizle
        self.table_widget.setHidden(True) # tabloyu gizle
        self.grafik_widget.setHidden(True) # grafikleri gizle

        if 'logDf' in locals() or 'logDf' in globals():

            self.column_info_goster.setGeometry(QtCore.QRect(25, 25, 1390, 800))

            logDf_desc = logDf.describe() #verisetinin genel özeti max-min-std

            # Tablo boyutunu ayarla
            self.column_info_goster.setRowCount(len(logDf_desc.columns))  # sütun sayısı için setRowCount()
            self.column_info_goster.setColumnCount(len(logDf_desc))  # satır sayısı için setColumnCount()

            # Sütun başlıklarını ayarla
            self.column_info_goster.setHorizontalHeaderLabels(logDf_desc.index)  # index sütunları sütun başlıkları olarak kullanılır
            # Sütun adlarını ayarla
            self.column_info_goster.setVerticalHeaderLabels(logDf_desc.columns)  # sütun adları dikey başlıklar olarak kullanılır


            # Tabloya verileri yaz
            for row in range(len(logDf_desc.columns)):
                for column in range(len(logDf_desc)):
                    item = QtWidgets.QTableWidgetItem(str(logDf_desc.iloc[column, row]))  # satır ve sütun indeksleri yer değiştirir
                    self.column_info_goster.setItem(row, column, item)

        else:
            message_box = QMessageBox()  # Mesaj kutusu oluşturma
            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            message_box.setText("        Gösterilecek Log Dosyası Bulunamadı!\n             Lütfen Log Dosyasını Yükleyin! \n (Dosya ekle butonuna tıklayarak .csv veya .json dosyası ekleyin)")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()  # Mesaj kutusunu gösterme

    
    def tablo_tikla(self):
        self.table_widget.setHidden(False)  # tablo değerini göster
        self.column_info_goster.setHidden(True) #column_info göster
        self.grafik_gorsel.setHidden(True)  # grafik değerini gizle
        self.grafik_widget.setHidden(True)  # grafikleri gizle
    
        if 'logDf' in locals() or 'logDf' in globals():
            self.table_widget.setGeometry(QtCore.QRect(25, 25, 1390, 830))
            # Tablo boyutunu ayarla
            self.table_widget.setRowCount(len(logDf.head(100)))
            self.table_widget.setColumnCount(len(logDf.columns))
            # Sütun başlıklarını ayarla
            self.table_widget.setHorizontalHeaderLabels(logDf.columns)
            
            # Tabloyu doldur
            for i, row in enumerate(logDf.head(100).iterrows()):
                for j, value in enumerate(row[1]):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    self.table_widget.setItem(i, j, item)
            


        else:
            message_box = QMessageBox()  # Mesaj kutusu oluşturma
            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            message_box.setText("        Gösterilecek Log Dosyası Bulunamadı!\n             Lütfen Log Dosyasını Yükleyin! \n (Dosya ekle butonuna tıklayarak .csv veya .json dosyası ekleyin)")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()  # Mesaj kutusunu gösterme


         # QLabel öğesi oluşturuluyor, bu öğe frame_right_bar_center öğesinin alt öğesi olarak atanıyor
        self.grafik_gorsel = QtWidgets.QLabel(parent=self.frame_right_bar_center)
    def grafik_goster(self):
        self.grafik_gorsel.setHidden(False) #grafik değerini göster
        self.column_info_goster.setHidden(True) #column_info göster
        self.table_widget.setHidden(True) # tabloyu gizle
        self.grafik_widget.setHidden(True) # grafikleri gizle

        # Öğenin minimum boyutu 1050x600 olarak ayarlanıyor
        self.grafik_gorsel.setMinimumSize(QtCore.QSize(1400,800))
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
        self.boyut = self.lineEdit_column_number.text() #kullanıcının boyut olarak girdiği değer
        print("Boyut Değeri:  " + self.boyut)

        if 'logDf' in locals() or 'logDf' in globals():
            if self.boyut == '':
                message_box = QMessageBox()  # Mesaj kutusu oluşturma
                message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                message_box.setText("Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
                message_box.setIcon(QMessageBox.Information)
                message_box.exec_()  # Mesaj kutusunu gösterme              
            try:

                    #message_box.setText("Boyut Değeri String Olamaz! \n Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
                if int(self.boyut) == 1 or self.boyut == '1':
                    self.frame_4.setHidden(False) #Sutun 1
                    self.frame_5.setHidden(True) #Sutun 2
                    self.frame_10.setHidden(True) #Sutun 3
                    self.frame_6.setHidden(False) #Grafikler
                    self.frame_7.setHidden(False) #Grafik Çizdir
                    self.frame_8.setHidden(False) #boyut degeri gir
                    self.frame_9.setHidden(False) #boyur degeri buton
                    self.frame_11.setHidden(False) #dosya ekle buton
                    self.frame_15.setHidden(True) #dosya ekle 2 buton

                elif int(self.boyut) == 2 or self.boyut =='2': 
                    self.frame_4.setHidden(False) #Sutun 1
                    self.frame_5.setHidden(False) #Sutun 2
                    self.frame_10.setHidden(True) #Sutun 3
                    self.frame_6.setHidden(False) #Grafikler
                    self.frame_7.setHidden(False) #Grafik Çizdir
                    self.frame_8.setHidden(False) #boyut degeri gir
                    self.frame_9.setHidden(False) #boyur degeri buton
                    self.frame_11.setHidden(False) #dosya ekle buton
                    self.frame_15.setHidden(True) #dosya ekle 2 buton

                elif int(self.boyut) == 3 or self.boyut == '3':
                    self.frame_4.setHidden(False) #Sutun 1
                    self.frame_5.setHidden(False) #Sutun 2
                    self.frame_10.setHidden(False) #Sutun 3
                    self.frame_6.setHidden(False) #Grafikler
                    self.frame_7.setHidden(False) #Grafik Çizdir
                    self.frame_8.setHidden(False) #boyut degeri gir
                    self.frame_9.setHidden(False) #boyur degeri buton
                    self.frame_11.setHidden(False) #dosya ekle buton
                    self.frame_15.setHidden(True) #dosya ekle 2 buton

            except ValueError:
                message_box = QMessageBox()  # Mesaj kutusu oluşturma
                message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                message_box.setText("Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
                message_box.setIcon(QMessageBox.Information)
                message_box.exec_()  # Mesaj kutusunu gösterme

            if self.boyut.isdigit():
                if int(self.boyut) ==1 or int(self.boyut) ==2 or int(self.boyut) ==3: # bu kısım çalışıyor
                    print('Boyut= ', self.boyut)
                    self.combobox_ayarla()
                    self.boyut = int(self.boyut)

                else: 
                    message_box = QMessageBox()  # Mesaj kutusu oluşturma
                    message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                    message_box.setText("Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
                    message_box.setIcon(QMessageBox.Information)
                    message_box.exec_()  # Mesaj kutusunu gösterme

            #elif isinstance(self.boyut, str):
            #    message_box = QMessageBox()  # Mesaj kutusu oluşturma
            #    message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            #    message_box.setText("Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
            #    message_box.setIcon(QMessageBox.Information)
            #    message_box.exec_()  # Mesaj kutusunu gösterme
            

            #else:                
            #    message_box = QMessageBox()  # Mesaj kutusu oluşturma
            #    message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            #    message_box.setText("        Gösterilecek Log Dosyası Bulunamadı!\n             Lütfen Log Dosyasını Yükleyin! \n (Dosya ekle butonuna tıklayarak .csv veya .json dosyası ekleyin)")
            #    message_box.setIcon(QMessageBox.Information)
            #    message_box.exec_()  # Mesaj kutusunu gösterme
            
        #else:
        #    message_box = QMessageBox()  # Mesaj kutusu oluşturma
        #    message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
        #    message_box.setText("        Gösterilecek Log Dosyası Bulunamadı!\n             Lütfen Log Dosyasını Yükleyin! \n (Dosya ekle butonuna tıklayarak .csv veya .json dosyası ekleyin)")
        #    message_box.setIcon(QMessageBox.Information)
        #    message_box.exec_()  # Mesaj kutusunu gösterme

    def combobox_ayarla(self):
        _translate = QtCore.QCoreApplication.translate

        self.comboBox_column_number_1.clear()
        self.comboBox_column_number_2.clear()
        self.comboBox_column_number_3.clear()
        self.comboBox_plot_name.clear()
        
        if self.boyut.isdigit():
            if int(self.boyut) == 1:
                self.comboBox_column_number_1.addItems(columnA.keys())
                
                self.comboBox_plot_name.addItems(grafikler1.keys())
                
            elif int(self.boyut) == 2:
                self.comboBox_column_number_1.addItems(columnA.keys())
                self.comboBox_column_number_2.addItems(columnA.keys())
    
                self.comboBox_plot_name.addItems(grafikler2.keys())
    
            elif int(self.boyut) == 3:
                self.comboBox_column_number_1.addItems(columnA.keys())
                self.comboBox_column_number_2.addItems(columnA.keys())
                self.comboBox_column_number_3.addItems(columnA.keys())
    
                self.comboBox_plot_name.addItems(grafikler3.keys())
    
                
            else:
                self.comboBox_column_number_1.setItemText(0, _translate("MainWindow", "   "))
                self.comboBox_column_number_2.setItemText(0, _translate("MainWindow", "   "))
                self.comboBox_column_number_3.setItemText(0, _translate("MainWindow", "   "))
    
                self.comboBox_plot_name.setItemText(0, _translate("MainWindow", " "))

        elif isinstance(self.boyut, str):
            message_box = QMessageBox()  # Mesaj kutusu oluşturma
            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            message_box.setText("Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()  # Mesaj kutusunu gösterme


    def grafik_ciz(self):
        self.grafik_widget.setHidden(False) # grafikleri goster
        self.column_info_goster.setHidden(True)
        self.grafik_gorsel.setHidden(True) # grafik değerini gizle
        self.table_widget.setHidden(True) # tablo değerini gizle
        self.pushButton_8.setHidden(False) #Yakinlastir
        self.pushButton_9.setHidden(False) #Uzaklastir
        self.pushButton_10.setHidden(False) #Reset
        
        self.sayac=0

        self.deger1_column = self.comboBox_column_number_1.currentText()
        self.deger2_column = self.comboBox_column_number_2.currentText()
        self.deger3_column = self.comboBox_column_number_3.currentText()
        self.grafikDeger = self.comboBox_plot_name.currentText()
        self.grafik_widget.setObjectName("grafik_widget")

        if self.lineEdit_column_number.text().isdigit():
            if int(self.boyut)==1:
                grDgr1 = grafikler1[self.grafikDeger]
                dgr1 = columnA[self.deger1_column]
                firstColumn = list(columnA.keys())[dgr1]
                sirali = logDf_normalized.sort_values(by=[firstColumn], ascending=False, ignore_index=True)
                columnName1 = logDf_normalized[firstColumn].name
                

            # ---Grafikleri Ekrana Yazdırma---

                # HeatMap
                if grDgr1 == 1:
                    fig, ax = plt.subplots(figsize=(20, 12))  #Tablonun boyutunu belirliyor
                    heatmap(logDf_normalized.corr(), #HeadMap değerlerini alır
                        annot=True, #Saydamlık saplayarak yazıların gözükmesini sağlar
                        linewidths=.5, #her bir değer arasındaki çizgilerin kalınlığını veriyor
                        fmt= '.2f', #kaç sıfır olacağını belirler
                        linecolor='black',
                        ax=ax)
                    plt.title('HeatMap', fontsize=15)
                    self.grafik_widget.setFixedSize(1600, 800)
                    grafik_cizdirildi = plt.savefig("graphic-outputs/" + 'HeatMap Plot.png', dpi=70)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + 'HeatMap Plot.png'))
                    ax.set_xticks(range(len(logDf_normalized.columns)))  # x ekseni etiketlerini ayarla
                    ax.set_yticks(range(len(logDf_normalized.columns)))  # y ekseni etiketlerini ayarla
                    ax.set_xticklabels(logDf_normalized.columns, fontsize=13, rotation=90)  # x ekseni etiketlerinin boyutunu ve dönme açısını ayarla
                    ax.set_yticklabels(logDf_normalized.columns, fontsize=13)  # y ekseni etiketlerinin boyutunu ayarla
                    self.grafik_widget.setAlignment(Qt.AlignCenter)
                    




                # Line Chart
                elif grDgr1 == 2:
                    fig, ax = plt.subplots(figsize=(24, 12))
                    logDf_normalized.iloc[:, dgr1].plot(kind = 'line', #Türü line olacak
                               color = 'green', # çizgi rengi
                               label = columnName1, #çizginin adı
                               linewidth=2, #çizginin kalınlığı
                              alpha = 0.6, #saydamlık
                               grid = False, #arkaplan çizgileri
                              linestyle = ':')
                    plt.legend(loc='upper right', fontsize=15) # legend ın konumu
                    plt.xlabel(columnName1,fontsize=15) # x eksenindeki label adı
                    plt.ylabel('ID',fontsize=15) #y eksenindeki label adı
                    plt.xticks(rotation=90, fontsize=13)
                    plt.yticks(fontsize=13)
                    plt.title(columnName1 + ' Verisinin Line Grafiği', fontsize=23) #plotun başlığı
                    self.grafik_widget.setFixedSize(1600, 800)
                    plt.savefig("graphic-outputs/" + columnName1 + ' Line Plot.png', dpi=70)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + ' Line Plot.png'))
                    self.grafik_widget.setAlignment(Qt.AlignCenter)
                    



                # Histogram Plot
                elif grDgr1 == 3:
                    fig, ax = plt.subplots(figsize=(24, 12) )
                    histplot(x=logDf_normalized.columns[dgr1], data=logDf_normalized, ax=ax)
                    plt.xlabel(columnName1,fontsize=15)
                    plt.ylabel("Count",fontsize=15)
                    plt.xticks(rotation= 90, fontsize=13)
                    plt.yticks(fontsize=13)
                    plt.title(columnName1 + ' Verisinin Histogram Grafiği', fontsize=23) #plotun başlığı
                    self.grafik_widget.setFixedSize(1600, 800)
                    plt.savefig("graphic-outputs/" + columnName1 + ' Histogram Plot.png', dpi=70)                
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + ' Histogram Plot.png'))
                    self.grafik_widget.setAlignment(Qt.AlignCenter)
                    

                #Count Plot
                elif grDgr1 == 4:
                    fig, ax = plt.subplots(figsize=(24, 12) )
                    set(font_scale=0.5)
                    countplot( y = logDf_normalized.columns[dgr1], data=logDf_normalized,ax=ax)
                    plt.xlabel("Count",fontsize=15)
                    plt.ylabel(columnName1,fontsize=15)
                    plt.xticks(rotation= 70, fontsize=13)
                    plt.yticks(fontsize=13)
                    plt.title(columnName1 + ' Count Plot', fontsize=18)
                    plt.savefig("graphic-outputs/" + columnName1 + ' Count Plot.png', dpi=70)
                    self.grafik_widget.setFixedSize(1500, 800)
                    self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + ' Count Plot.png'))
                    self.grafik_widget.setAlignment(Qt.AlignCenter)

                else:
                    print('hatalı veri')

                
            # 2 Adet Column
            elif int(self.boyut) == 2:
                    grDgr2 = grafikler2[self.grafikDeger]
                    dgr1 = columnA[self.deger1_column]
                    dgr2 = columnA[self.deger2_column]
                    firstColumn = list(columnA.keys())[dgr1]
                    sirali = logDf_normalized.sort_values(by=[firstColumn], ascending=False, ignore_index=True)
                    secondColumn = list(columnA.keys())[dgr2]
                    columnName1 = logDf_normalized[firstColumn].name
                    columnName2 = logDf_normalized[secondColumn].name

                    # Line Chart
                    if grDgr2 == 1:
                        if firstColumn == secondColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("İki Sutun Değeri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme

                        else:
                            fig, ax = plt.subplots(figsize=(24, 12) )

                            logDf_normalized.iloc[:, dgr1].plot(kind = 'line', #Türü line olacak
                                        color = 'green', # çizgi rengi
                                        label = columnName1, #çizginin adı
                                        linewidth=2, #çizginin kalınlığı
                                        alpha = 0.5, #saydamlık
                                        grid = False, #arkaplan çizgileri
                                        linestyle = ':',ax=ax)
                            logDf_normalized.iloc[:, dgr2].plot(kind='line',
                                        color = 'red',
                                        label = columnName2,
                                        linewidth=2, 
                                        alpha = 0.5,
                                        grid = True, #Grid değeri en son girilen değeri alıyor. 
                                        linestyle = '-.',ax=ax)
    
                            plt.legend(loc='upper right', fontsize=15 ) # legend ın konumu
                            plt.xlabel(columnName1, fontsize=15) # x eksenindeki label adı
                            plt.ylabel(columnName2, fontsize=15) #y eksenindeki label adı
                            plt.xticks(rotation= 90, fontsize=13)
                            plt.yticks(fontsize=13)
                            plt.title(columnName1 + '  -  ' + columnName2 + ' Line Grafiği', fontsize=18) #plotun başlığı

                            plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Line Plot.png', dpi=70)                
                            self.grafik_widget.setFixedSize(1500, 800)
                            self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Line Plot.png'))
                            self.grafik_widget.setAlignment(Qt.AlignCenter)
                            

                    # Scatter Plot
                    elif grDgr2 == 2:
                        if firstColumn == secondColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("İki Sutun Değeri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme
                        
                        else:
                            fig, ax = plt.subplots(figsize=(24, 12))
                            fig.subplots_adjust(left=0.1)


                            logDf_normalized.plot(kind='scatter', x=dgr1, y=dgr2, alpha=0.5, color='red', figsize=(22,12), ax=ax)
                            plt.xlabel(logDf_normalized.columns[dgr1], fontsize=15)
                            plt.ylabel(logDf_normalized.columns[dgr2], fontsize=15)
                            plt.xticks(rotation= 90, fontsize=13)
                            plt.yticks(fontsize=13)
                            plt.title(columnName1 + '  -  ' + columnName2 + ' Scatter Plot', fontsize=18)
    
                            plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Scatter Plot.png', dpi=75)                
                            self.grafik_widget.setFixedSize(1500, 800)
                            self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Scatter Plot.png'))
                            self.grafik_widget.setAlignment(Qt.AlignCenter)
                            

                    # Bar Chart
                    elif grDgr2 == 3:
                        if firstColumn == secondColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("İki Sutun Değeri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme

                        else:
                            fig, ax = plt.subplots(figsize=(24, 12) )
                            barplot(x=sirali.index, y=sirali.columns[dgr1], data=sirali, ax=ax)
                            plt.xlabel(columnName1, fontsize=15) # x eksenindeki label adı
                            plt.ylabel(columnName2, fontsize=15) #y eksenindeki label adı
                            plt.xticks(rotation= 90, fontsize=8)
                            plt.yticks(fontsize=13)
                            plt.title(columnName1 + '  -  ' + columnName2 + ' Bar Grafiği', fontsize=18)

                            plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Bar Plot.png', dpi=70)                
                            self.grafik_widget.setFixedSize(1700, 850)
                            self.grafik_widget.setAlignment(Qt.AlignLeft)
                            self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Bar Plot.png'))


                    # Strip Plot
                    elif grDgr2 == 4:
                        if firstColumn == secondColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("İki Sutun Değeri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme
                        
                        else:
                            fig, ax = plt.subplots(figsize=(24, 12) ) # Grafik Boyutu

                            ax.set_title('{} - {} Scatter Plot'.format(firstColumn, secondColumn), fontsize=20) # Grafiğin başlığı
                            stripplot(data=logDf_normalized, x=firstColumn, y=secondColumn, ax=ax)
                            ax.set_xlabel(firstColumn, fontsize=15)
                            ax.set_ylabel(secondColumn, fontsize=15)
                            plt.xticks(rotation= 90, fontsize=13)
                            plt.yticks(fontsize=13)

                            self.grafik_widget.setFixedSize(1600, 900)
                            plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Strip Plot.png', dpi=70)                
                            self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Strip Plot.png'))
                            self.grafik_widget.setAlignment(Qt.AlignCenter)
                            

                    #Joint Plot
                    elif grDgr2 == 5:
                        if firstColumn == secondColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("İki Sutun Değeri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme

                        else:
                            fig, ax = plt.subplots(figsize=(40, 40))

                            grafik = jointplot(x=firstColumn, y=secondColumn, data=logDf_normalized)
                            grafik.plot(scatterplot, histplot)
                            plt.subplots_adjust(top=0.9)  # Grafiklerin başlık için yer bırakması için üst kenarı ayarla
                            plt.suptitle('{} - {} Joint Plot'.format(columnName1, columnName2), fontsize=20) # Grafiğin başlığı
                            grafik.set_axis_labels(xlabel=firstColumn, ylabel=secondColumn, fontsize=14)
                            plt.xticks(rotation= 90, fontsize=13)
                            plt.yticks(fontsize=13)
                            
                            
                            self.grafik_widget.setFixedSize(1500, 800)
                            plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Joint Plot.png', dpi=100)                
                            self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' Joint Plot.png'))
                            self.grafik_widget.setAlignment(Qt.AlignCenter)
                            
                    

                    # KDE Plot
                    elif grDgr2 == 6:
                        if firstColumn == secondColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("İki Sutun Değeri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme
                        
                        else:
                            fig, ax = plt.subplots(figsize=(24, 12))

                            kdeplot(data=logDf_normalized, x= firstColumn, y=secondColumn, maker="kind", fill=True, fontsize=15, ax=ax)
                            plt.title(columnName1 + '  -  ' + columnName2 + ' KDE Plot', fontsize=20)
                            ax.set_xlabel(firstColumn, fontsize=15)
                            ax.set_ylabel(secondColumn, fontsize=15)
                            plt.xticks(rotation= 90, fontsize=13)
                            plt.yticks(fontsize=13)

                            self.grafik_widget.setFixedSize(1500, 800)
                            plt.savefig("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' KDE Plot.png', dpi=70)                
                            self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + columnName1 + '  -  ' + columnName2 + ' KDE Plot.png'))
                            self.grafik_widget.setAlignment(Qt.AlignCenter)
                            


            # 3 Adet Column
            elif logDf.shape[1] > 2 and int(self.boyut)==3:
                grDgr3 = grafikler3[self.grafikDeger]
                dgr1 = columnA[self.deger1_column]
                dgr2 = columnA[self.deger2_column]
                dgr3 = columnA[self.deger3_column]
                firstColumn = list(columnA.keys())[dgr1]
                sirali = logDf_normalized.sort_values(by=[firstColumn], ascending=False, ignore_index=True)
                secondColumn = list(columnA.keys())[dgr2]
                thirdColumn = list(columnA.keys())[dgr3]
                columnName1 = logDf_normalized[firstColumn].name
                columnName2 = logDf_normalized[secondColumn].name
                columnName3 = logDf_normalized[thirdColumn].name

                if grDgr3==1:
                    if firstColumn == secondColumn or secondColumn == thirdColumn or firstColumn == thirdColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("Sutun Değerleri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme
                    
                    else:
                        fig = plt.figure(figsize=(17, 12))
                        ax = fig.add_subplot(111, projection="3d")

                        x_data = logDf_normalized[logDf_normalized.columns[dgr1]]
                        y_data = logDf_normalized[logDf_normalized.columns[dgr2]]
                        z_data = logDf_normalized[logDf_normalized.columns[dgr3]]

                        ax.scatter(x_data, y_data, z_data)

                        plt.title(firstColumn + ' - ' + secondColumn + ' - ' + thirdColumn + ' 3D Scatter Plot', fontsize=20)
                        ax.set_xlabel(firstColumn, fontsize=15)
                        ax.set_ylabel(secondColumn, fontsize=15)
                        ax.set_zlabel(thirdColumn, fontsize=15)
                        plt.xticks(rotation=90, fontsize=13)
                        plt.yticks(fontsize=13)
                        plt.xticks(fontsize=13)

                        plt.savefig("graphic-outputs/" + firstColumn + ' - ' + secondColumn + ' - ' + thirdColumn + ' 3D Scatter Plot.png', dpi=75)

                        self.grafik_widget.setFixedSize(1850, 800)
                        self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" + firstColumn + ' - ' + secondColumn + ' - ' + thirdColumn + ' 3D Scatter Plot.png'))
                        


                elif grDgr3 == 2:
                    if firstColumn == secondColumn or secondColumn == thirdColumn or firstColumn == thirdColumn:
                            message_box = QMessageBox()  # Mesaj kutusu oluşturma
                            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                            message_box.setText("Sutun Değerleri Aynı Olamaz! \nLütfen farklı bir sutun değeri seçiniz.")
                            message_box.setIcon(QMessageBox.Information)
                            message_box.exec_()  # Mesaj kutusunu gösterme
                    
                    else:
                        fig, ax = plt.subplots(figsize=(20, 12))

                        logDf_normalized.iloc[:, dgr1].plot(kind = 'line', #Türü line olacak
                                    color = 'green', # çizgi rengi
                                    label = columnName1, #çizginin adı
                                    linewidth=2, #çizginin kalınlığı
                                    alpha = 0.5, #saydamlık
                                    grid = True, #arkaplan çizgileri
                                    linestyle = ':')
                        logDf_normalized.iloc[:, dgr2].plot(kind='line',
                                    color = 'red',
                                    label = columnName2,
                                    linewidth=2, 
                                    alpha = 0.5,
                                    grid = True, #Grid değeri en son girilen değeri alıyor. 
                                    linestyle = '-.')
                        logDf_normalized.iloc[:, dgr3].plot(kind='line',
                                    color = 'blue',
                                    label = columnName3,
                                    linewidth=2, 
                                    alpha = 0.5,
                                    grid = True, #Grid değeri en son girilen değeri alıyor. 
                                    linestyle = '-.')
                        plt.legend(loc='upper right', fontsize=13) # legend ın konumu
                        plt.xlabel('x axis',fontsize=15) # x eksenindeki label adı
                        plt.ylabel('y axis',fontsize=15) #y eksenindeki label adı
                        plt.xticks(rotation=90, fontsize=13)
                        plt.yticks(fontsize=13)
                        plt.title(firstColumn + ' - ' + secondColumn + ' - ' + thirdColumn + ' 3 Adet Line Plot', fontsize=20)

                        self.grafik_widget.setFixedSize(1400, 700)
                        plt.savefig("graphic-outputs/" + firstColumn + '  -  ' + secondColumn + '  -  ' + thirdColumn + ' 3 Adet Line Plot.png', dpi=70)                
                        self.grafik_widget.setPixmap(QtGui.QPixmap("graphic-outputs/" +  firstColumn + '  -  ' + secondColumn + '  -  ' + thirdColumn +' 3 Adet Line Plot.png'))  
                        

            else:
                message_box = QMessageBox()  # Mesaj kutusu oluşturma
                message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
                message_box.setText("Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
                message_box.setIcon(QMessageBox.Information)
                message_box.exec_()  # Mesaj kutusunu gösterme
        
        elif isinstance(self.boyut, str):
            message_box = QMessageBox()  # Mesaj kutusu oluşturma
            message_box.setWindowTitle("Grafik Çizim Aracı Uyarı!")
            message_box.setText("Lütfen Geçerli Bir Boyut Değeri Giriniz! \n Boyut= 1 - 2 - 3")
            message_box.setIcon(QMessageBox.Information)
            message_box.exec_()  # Mesaj kutusunu gösterme


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
        self.pushButton_dosya_ekle.setText(_translate("MainWindow", "Dosya Ekle"))
        self.pushButton_dosya_ekle.clicked.connect(self.dosya_ekle)
        self.pushButton_dosya_ekle_2.setText(_translate("MainWindow", "Dosya Ekle"))
        self.pushButton_dosya_ekle_2.clicked.connect(self.dosya_ekle)
        self.pushButton_boyut_ekle.setText(_translate("MainWindow", "Boyut Ekle"))
        self.pushButton_boyut_ekle.clicked.connect(self.boyut_al)        
        self.pushButton_4.setText(_translate("MainWindow", "Veri Tablosu"))
        self.pushButton_4.clicked.connect(self.tablo_tikla)        
        self.pushButton_5.setText(_translate("MainWindow", "Veri Seti Bilgileri"))
        self.pushButton_5.clicked.connect(self.column_info)
        self.pushButton_8.setText(_translate("MainWindow", "Yakınlaştır"))
        self.pushButton_8.clicked.connect(self.zoom_in) 
        self.pushButton_9.setText(_translate("MainWindow", "Uzaklaştır"))
        self.pushButton_9.clicked.connect(self.zoom_out)
        self.pushButton_10.setText(_translate("MainWindow", "Reset"))
        self.pushButton_10.clicked.connect(self.reset_yap)
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