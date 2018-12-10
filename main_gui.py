import os
import sys
import json
import time
from os.path import basename
import traceback
import logging
import copy
from logging.handlers import RotatingFileHandler
import ModuleJSON_class
from functools import partial

import Simulation_class

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from numpy import arange, logspace
from scipy.interpolate import splev, splrep  # for curve smoothing

import sim_tools
import cProfile

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(629, 440)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainTabWidget = QtWidgets.QTabWidget(self.centralWidget)
        self.mainTabWidget.setObjectName("tabWidget")
        self.moduleSelect = QtWidgets.QWidget()
        self.moduleSelect.setObjectName("moduleSelect")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.moduleSelect)
        self.gridLayout_2.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(self.moduleSelect)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addCustomModuleFile = QtWidgets.QPushButton(self.frame)
        self.addCustomModuleFile.setObjectName("addCustomModuleFile")
        self.horizontalLayout.addWidget(self.addCustomModuleFile)
        self.removeCustomModuleFile = QtWidgets.QPushButton(self.frame)
        self.removeCustomModuleFile.setObjectName("removeCustomModuleFile")
        self.horizontalLayout.addWidget(self.removeCustomModuleFile)
        self.gridLayout_2.addWidget(self.frame, 1, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 1, 2, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.moduleSelect)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_4 = QtWidgets.QFrame(self.frame_6)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sendModuleFiletoStack = QtWidgets.QPushButton(self.frame_4)
        self.sendModuleFiletoStack.setObjectName("sendModuleFiletoStack")
        self.verticalLayout_3.addWidget(self.sendModuleFiletoStack)
        self.pullModuleFilefromStack = QtWidgets.QPushButton(self.frame_4)
        self.pullModuleFilefromStack.setObjectName("pullModuleFilefromStack")
        self.verticalLayout_3.addWidget(self.pullModuleFilefromStack)
        self.gridLayout.addWidget(self.frame_4, 1, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        self.moduleSelectTreeWidget = QtWidgets.QTreeWidget(self.frame_6)
        self.moduleSelectTreeWidget.setObjectName("moduleFileTreeWidget")
        self.moduleSelectTreeWidget.headerItem().setText(0, "1")
        self.gridLayout.addWidget(self.moduleSelectTreeWidget, 0, 0, 3, 1)
        self.selectedModuleStackListWidget = QtWidgets.QListWidget(self.frame_6)
        self.selectedModuleStackListWidget.setObjectName("moduleFileStack")
        self.gridLayout.addWidget(self.selectedModuleStackListWidget, 0, 2, 3, 1)
        self.gridLayout_2.addWidget(self.frame_6, 0, 0, 1, 3)
        self.mainTabWidget.addTab(self.moduleSelect, "")
        self.info_2Level = QtWidgets.QWidget()
        self.info_2Level.setObjectName("info_2Level")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.info_2Level)
        self.gridLayout_12.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_12.setSpacing(6)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.frame_2 = QtWidgets.QFrame(self.info_2Level)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_4.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_4.setSpacing(6)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.pullModuleFileStack_2Level = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(121)
        sizePolicy.setVerticalStretch(23)
        sizePolicy.setHeightForWidth(self.pullModuleFileStack_2Level.sizePolicy().hasHeightForWidth())
        self.pullModuleFileStack_2Level.setSizePolicy(sizePolicy)
        self.pullModuleFileStack_2Level.setObjectName("pullModuleFileStack_2Level")
        self.gridLayout_4.addWidget(self.pullModuleFileStack_2Level, 1, 0, 1, 2)
        self.moduleFileListWidget_2Level = QtWidgets.QListWidget(self.frame_2)
        self.moduleFileListWidget_2Level.setObjectName("moduleFileListWidget_2Level")
        self.gridLayout_4.addWidget(self.moduleFileListWidget_2Level, 0, 0, 1, 2)
        self.gridLayout_12.addWidget(self.frame_2, 0, 0, 3, 1)
        self.modulationTypeCombo_2Level = QtWidgets.QComboBox(self.info_2Level)
        self.modulationTypeCombo_2Level.setObjectName("modulationTypeCombo_2Level")
        self.modulationTypeCombo_2Level.addItem("")
        self.modulationTypeCombo_2Level.addItem("")
        self.modulationTypeCombo_2Level.addItem("")
        self.modulationTypeCombo_2Level.addItem("")
        self.modulationTypeCombo_2Level.addItem("")
        self.modulationTypeCombo_2Level.addItem("")
        self.gridLayout_12.addWidget(self.modulationTypeCombo_2Level, 1, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem4, 0, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_12.addItem(spacerItem5, 2, 1, 1, 1)
        self.mainTabWidget.addTab(self.info_2Level, "")
        self.info_3Level = QtWidgets.QWidget()
        self.info_3Level.setObjectName("info_3Level")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.info_3Level)
        self.gridLayout_5.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_5.setSpacing(6)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBox_4 = QtWidgets.QGroupBox(self.info_3Level)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_9.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_9.setSpacing(6)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.outsideModuleListWidget_3Level = QtWidgets.QListWidget(self.groupBox_4)
        self.outsideModuleListWidget_3Level.setObjectName("outsideModuleListWidget_3Level")
        self.gridLayout_9.addWidget(self.outsideModuleListWidget_3Level, 0, 0, 1, 2)
        self.pullModuleFileStack_outside_3Level = QtWidgets.QPushButton(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(121)
        sizePolicy.setVerticalStretch(23)
        sizePolicy.setHeightForWidth(self.pullModuleFileStack_outside_3Level.sizePolicy().hasHeightForWidth())
        self.pullModuleFileStack_outside_3Level.setSizePolicy(sizePolicy)
        self.pullModuleFileStack_outside_3Level.setObjectName("pullModuleFileStack_outside_3Level")
        self.gridLayout_9.addWidget(self.pullModuleFileStack_outside_3Level, 1, 0, 1, 2)
        self.gridLayout_5.addWidget(self.groupBox_4, 3, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.info_3Level)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_7.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_7.setSpacing(6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.insideModuleListWidget_3Level = QtWidgets.QListWidget(self.groupBox_2)
        self.insideModuleListWidget_3Level.setObjectName("insideModuleListWidget_3Level")
        self.gridLayout_7.addWidget(self.insideModuleListWidget_3Level, 0, 0, 1, 2)
        self.pullModuleFileStack_inside_3Level = QtWidgets.QPushButton(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(121)
        sizePolicy.setVerticalStretch(23)
        sizePolicy.setHeightForWidth(self.pullModuleFileStack_inside_3Level.sizePolicy().hasHeightForWidth())
        self.pullModuleFileStack_inside_3Level.setSizePolicy(sizePolicy)
        self.pullModuleFileStack_inside_3Level.setObjectName("pullModuleFileStack_inside_3Level")
        self.gridLayout_7.addWidget(self.pullModuleFileStack_inside_3Level, 1, 0, 1, 2)
        self.gridLayout_5.addWidget(self.groupBox_2, 3, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.info_3Level)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_8.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.pullModuleFileStack_diode_3Level = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(121)
        sizePolicy.setVerticalStretch(23)
        sizePolicy.setHeightForWidth(self.pullModuleFileStack_diode_3Level.sizePolicy().hasHeightForWidth())
        self.pullModuleFileStack_diode_3Level.setSizePolicy(sizePolicy)
        self.pullModuleFileStack_diode_3Level.setObjectName("pullModuleFileStack_diode_3Level")
        self.gridLayout_8.addWidget(self.pullModuleFileStack_diode_3Level, 1, 0, 1, 2)
        self.diodeModuleListWidget_3Level = QtWidgets.QListWidget(self.groupBox_3)
        self.diodeModuleListWidget_3Level.setObjectName("diodeModuleListWidget_3Level")
        self.gridLayout_8.addWidget(self.diodeModuleListWidget_3Level, 0, 0, 1, 2)
        self.gridLayout_5.addWidget(self.groupBox_3, 3, 2, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem6, 4, 2, 1, 1)
        self.frame_7 = QtWidgets.QFrame(self.info_3Level)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_6.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.modulationTypeCombo_3Level = QtWidgets.QComboBox(self.frame_7)
        self.modulationTypeCombo_3Level.setObjectName("modulationTypeCombo_3Level")
        self.modulationTypeCombo_3Level.addItem("")
        self.modulationTypeCombo_3Level.addItem("")
        self.modulationTypeCombo_3Level.addItem("")
        self.modulationTypeCombo_3Level.addItem("")
        self.modulationTypeCombo_3Level.addItem("")
        self.modulationTypeCombo_3Level.addItem("")
        self.horizontalLayout_6.addWidget(self.modulationTypeCombo_3Level)
        self.layoutCombo_3Level = QtWidgets.QComboBox(self.frame_7)
        self.layoutCombo_3Level.setObjectName("layoutCombo_3Level")
        self.layoutCombo_3Level.addItem("")
        self.layoutCombo_3Level.addItem("")
        self.layoutCombo_3Level.addItem("")
        self.horizontalLayout_6.addWidget(self.layoutCombo_3Level)
        self.gridLayout_5.addWidget(self.frame_7, 4, 1, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem7, 4, 0, 1, 1)
        self.mainTabWidget.addTab(self.info_3Level, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_6.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_6.setSpacing(6)
        self.gridLayout_6.setObjectName("gridLayout_6")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem8, 2, 3, 1, 1)
        self.groupBox_8 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_8.setObjectName("groupBox_8")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_8)
        self.gridLayout_11.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_11.setSpacing(6)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.pullModuleFileStack_diode_Chopper = QtWidgets.QPushButton(self.groupBox_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(121)
        sizePolicy.setVerticalStretch(23)
        sizePolicy.setHeightForWidth(self.pullModuleFileStack_diode_Chopper.sizePolicy().hasHeightForWidth())
        self.pullModuleFileStack_diode_Chopper.setSizePolicy(sizePolicy)
        self.pullModuleFileStack_diode_Chopper.setObjectName("pullModuleFileStack_diode_Chopper")
        self.gridLayout_11.addWidget(self.pullModuleFileStack_diode_Chopper, 1, 0, 1, 3)
        self.diodeModuleListWidget_Chopper = QtWidgets.QListWidget(self.groupBox_8)
        self.diodeModuleListWidget_Chopper.setObjectName("diodeModuleListWidget_Chopper")
        self.gridLayout_11.addWidget(self.diodeModuleListWidget_Chopper, 0, 0, 1, 3)
        self.enableDiodeModule = QtWidgets.QCheckBox(self.groupBox_8)
        self.enableDiodeModule.setObjectName("enableDiodeModule")
        self.gridLayout_11.addWidget(self.enableDiodeModule, 2, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_8, 0, 2, 1, 2)
        self.layoutCombo_Chopper = QtWidgets.QComboBox(self.tab_4)
        self.layoutCombo_Chopper.setObjectName("layoutCombo_Chopper")
        self.layoutCombo_Chopper.addItem("")
        self.layoutCombo_Chopper.addItem("")
        self.layoutCombo_Chopper.addItem("")
        self.gridLayout_6.addWidget(self.layoutCombo_Chopper, 2, 1, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_6.addItem(spacerItem9, 2, 0, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox_5.setObjectName("groupBox_5")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_5)
        self.gridLayout_10.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_10.setSpacing(6)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.pullModuleFileStack_chopper_Chopper = QtWidgets.QPushButton(self.groupBox_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(121)
        sizePolicy.setVerticalStretch(23)
        sizePolicy.setHeightForWidth(self.pullModuleFileStack_chopper_Chopper.sizePolicy().hasHeightForWidth())
        self.pullModuleFileStack_chopper_Chopper.setSizePolicy(sizePolicy)
        self.pullModuleFileStack_chopper_Chopper.setObjectName("pullModuleFileStack_chopper_Chopper")
        self.gridLayout_10.addWidget(self.pullModuleFileStack_chopper_Chopper, 1, 0, 1, 2)
        self.chopperModuleListWidget_Chopper = QtWidgets.QListWidget(self.groupBox_5)
        self.chopperModuleListWidget_Chopper.setObjectName("chopperModuleListWidget_Chopper")
        self.gridLayout_10.addWidget(self.chopperModuleListWidget_Chopper, 0, 0, 1, 2)
        self.gridLayout_6.addWidget(self.groupBox_5, 0, 0, 1, 2)
        self.mainTabWidget.addTab(self.tab_4, "")
        self.verticalLayout.addWidget(self.mainTabWidget)
        self.frame_5 = QtWidgets.QFrame(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setMinimumSize(QtCore.QSize(611, 81))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.groupBox = QtWidgets.QGroupBox(self.frame_5)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.userInput__SimulationInputFileLocation = QtWidgets.QLineEdit(self.groupBox)
        self.userInput__SimulationInputFileLocation.setObjectName("simulationFileLocation")
        self.horizontalLayout_4.addWidget(self.userInput__SimulationInputFileLocation)
        self.openSimulationFile = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openSimulationFile.sizePolicy().hasHeightForWidth())
        self.openSimulationFile.setSizePolicy(sizePolicy)
        self.openSimulationFile.setMinimumSize(QtCore.QSize(47, 0))
        self.openSimulationFile.setObjectName("openSimulationFile")
        self.horizontalLayout_4.addWidget(self.openSimulationFile)
        self.horizontalLayout_5.addWidget(self.groupBox)
        self.groupBox_6 = QtWidgets.QGroupBox(self.frame_5)
        self.groupBox_6.setMinimumSize(QtCore.QSize(150, 0))
        self.groupBox_6.setObjectName("groupBox_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox_6)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.enableStepSize = QtWidgets.QCheckBox(self.groupBox_6)
        self.enableStepSize.setObjectName("enableStepSize")
        self.horizontalLayout_3.addWidget(self.enableStepSize)
        self.stepSizeValue = QtWidgets.QSpinBox(self.groupBox_6)
        self.stepSizeValue.setMinimum(1)
        self.stepSizeValue.setMaximum(360)
        self.stepSizeValue.setObjectName("stepSizeValue")
        self.horizontalLayout_3.addWidget(self.stepSizeValue)
        self.horizontalLayout_5.addWidget(self.groupBox_6)
        self.groupBox_9 = QtWidgets.QGroupBox(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy)
        self.groupBox_9.setMinimumSize(QtCore.QSize(150, 0))
        self.groupBox_9.setObjectName("groupBox_9")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_12.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_12.setSpacing(6)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.maxCurrentOutputEnable = QtWidgets.QCheckBox(self.groupBox_9)
        self.maxCurrentOutputEnable.setObjectName("maxCurrentOutputEnable")
        self.horizontalLayout_12.addWidget(self.maxCurrentOutputEnable)
        self.maxCurrentTemp = QtWidgets.QDoubleSpinBox(self.groupBox_9)
        self.maxCurrentTemp.setMinimum(-25.0)
        self.maxCurrentTemp.setMaximum(200.0)
        self.maxCurrentTemp.setProperty("value", 175.0)
        self.maxCurrentTemp.setObjectName("maxCurrentTemp")
        self.horizontalLayout_12.addWidget(self.maxCurrentTemp)
        self.horizontalLayout_5.addWidget(self.groupBox_9)
        self.groupBox_7 = QtWidgets.QGroupBox(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.groupBox_7.setMinimumSize(QtCore.QSize(150, 71))
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.RGSuppressCheckbox = QtWidgets.QCheckBox(self.groupBox_7)
        self.RGSuppressCheckbox.setObjectName("ignoreRGinputs")
        self.verticalLayout_2.addWidget(self.RGSuppressCheckbox)
        self.advancedOutputCheckbox = QtWidgets.QCheckBox(self.groupBox_7)
        self.advancedOutputCheckbox.setObjectName("advancedOutput")
        self.verticalLayout_2.addWidget(self.advancedOutputCheckbox)
        self.horizontalLayout_5.addWidget(self.groupBox_7)
        self.verticalLayout.addWidget(self.frame_5)
        self.frame_3 = QtWidgets.QFrame(self.centralWidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.frame_3)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.simulationProgressBar = QtWidgets.QProgressBar(self.frame_3)
        self.simulationProgressBar.setProperty("value", 24)
        self.simulationProgressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.simulationProgressBar)
        self.verticalLayout.addWidget(self.frame_3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 629, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuCreate_Input_Template = QtWidgets.QMenu(self.menuFile)
        self.menuCreate_Input_Template.setObjectName("menuCreate_Input_Template")
        self.menuHelp = QtWidgets.QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.windowStatusBar = QtWidgets.QStatusBar(MainWindow)
        self.windowStatusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.windowStatusBar)
        self.actionOpen_Datasheet_Compare = QtWidgets.QAction(MainWindow)
        self.actionOpen_Datasheet_Compare.setObjectName("actionOpen_Datasheet_Compare")
        self.actionOpen_Single_Simulation = QtWidgets.QAction(MainWindow)
        self.actionOpen_Single_Simulation.setObjectName("actionOpen_Single_Simulation")
        self.action2_Level = QtWidgets.QAction(MainWindow)
        self.action2_Level.setObjectName("action2_Level")
        self.action3_Level = QtWidgets.QAction(MainWindow)
        self.action3_Level.setObjectName("action3_Level")
        self.actionChopper = QtWidgets.QAction(MainWindow)
        self.actionChopper.setObjectName("actionChopper")
        self.actionCreate_Module_Template = QtWidgets.QAction(MainWindow)
        self.actionCreate_Module_Template.setObjectName("actionCreate_Module_Template")
        self.actionNo_one_can_help_you_now = QtWidgets.QAction(MainWindow)
        self.actionNo_one_can_help_you_now.setObjectName("actionNo_one_can_help_you_now")
        self.menuCreate_Input_Template.addAction(self.action2_Level)
        self.menuCreate_Input_Template.addAction(self.action3_Level)
        self.menuCreate_Input_Template.addAction(self.actionChopper)
        self.menuFile.addAction(self.actionOpen_Datasheet_Compare)
        self.menuFile.addAction(self.actionOpen_Single_Simulation)
        self.menuFile.addAction(self.menuCreate_Input_Template.menuAction())
        self.menuFile.addAction(self.actionCreate_Module_Template)
        self.menuHelp.addAction(self.actionNo_one_can_help_you_now)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.mainTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.setup__widgets_and_views()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "IGBT Sim"))
        self.addCustomModuleFile.setText(_translate("MainWindow", "Add module file"))
        self.removeCustomModuleFile.setText(_translate("MainWindow", "Remove Module FIle"))
        self.sendModuleFiletoStack.setText(_translate("MainWindow", ">"))
        self.pullModuleFilefromStack.setText(_translate("MainWindow", "<"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.moduleSelect), _translate("MainWindow", "Module Select"))
        self.pullModuleFileStack_2Level.setText(_translate("MainWindow", "Pull List from Selection"))
        self.modulationTypeCombo_2Level.setItemText(0, _translate("MainWindow", "Sinusoidal"))
        self.modulationTypeCombo_2Level.setItemText(1, _translate("MainWindow", "SVPWM"))
        self.modulationTypeCombo_2Level.setItemText(2, _translate("MainWindow", "Two Phase I"))
        self.modulationTypeCombo_2Level.setItemText(3, _translate("MainWindow", "2-Phase 2"))
        self.modulationTypeCombo_2Level.setItemText(4, _translate("MainWindow", "High-Side Chopping"))
        self.modulationTypeCombo_2Level.setItemText(5, _translate("MainWindow", "First-Half Chopping"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.info_2Level), _translate("MainWindow", "2-Level"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Outside Module"))
        self.pullModuleFileStack_outside_3Level.setText(_translate("MainWindow", "Pull List from Selection"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Inside Module"))
        self.pullModuleFileStack_inside_3Level.setText(_translate("MainWindow", "Pull List from Selection"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Diode Module"))
        self.pullModuleFileStack_diode_3Level.setText(_translate("MainWindow", "Pull List from Selection"))
        self.modulationTypeCombo_3Level.setItemText(0, _translate("MainWindow", "Sinusoidal"))
        self.modulationTypeCombo_3Level.setItemText(1, _translate("MainWindow", "SVPWM"))
        self.modulationTypeCombo_3Level.setItemText(2, _translate("MainWindow", "Two Phase I"))
        self.modulationTypeCombo_3Level.setItemText(3, _translate("MainWindow", "2-Phase 2"))
        self.modulationTypeCombo_3Level.setItemText(4, _translate("MainWindow", "High-Side Chopping"))
        self.modulationTypeCombo_3Level.setItemText(5, _translate("MainWindow", "First-Half Chopping"))
        self.layoutCombo_3Level.setItemText(0, _translate("MainWindow", "I-Type NPC 1"))
        self.layoutCombo_3Level.setItemText(1, _translate("MainWindow", "I-Type NPC 2"))
        self.layoutCombo_3Level.setItemText(2, _translate("MainWindow", "T-Type NPC (AC Switch)"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.info_3Level), _translate("MainWindow", "3-Level"))
        self.groupBox_8.setTitle(_translate("MainWindow", "Diode Module"))
        self.pullModuleFileStack_diode_Chopper.setText(_translate("MainWindow", "Pull List from Selection"))
        self.enableDiodeModule.setText(_translate("MainWindow", "Enable Diode"))
        self.layoutCombo_Chopper.setItemText(0, _translate("MainWindow", "Down"))
        self.layoutCombo_Chopper.setItemText(1, _translate("MainWindow", "Boost"))
        self.layoutCombo_Chopper.setItemText(2, _translate("MainWindow", "Motor Lock"))
        self.groupBox_5.setTitle(_translate("MainWindow", "Chopper Module"))
        self.pullModuleFileStack_chopper_Chopper.setText(_translate("MainWindow", "Pull List from Selection"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.tab_4), _translate("MainWindow", "Chopper"))
        self.groupBox.setTitle(_translate("MainWindow", "Simulator File"))
        self.openSimulationFile.setText(_translate("MainWindow", "Open..."))
        self.groupBox_6.setTitle(_translate("MainWindow", "Step Size"))
        self.enableStepSize.setText(_translate("MainWindow", "Enable"))
        self.groupBox_9.setTitle(_translate("MainWindow", "Max Current Output"))
        self.maxCurrentOutputEnable.setText(_translate("MainWindow", "Enable"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Options"))
        self.RGSuppressCheckbox.setText(_translate("MainWindow", "Ignore RG inputs"))
        self.advancedOutputCheckbox.setText(_translate("MainWindow", "Advanced Output"))
        self.pushButton.setText(_translate("MainWindow", "Giddy up"))
        self.menuFile.setTitle(_translate("MainWindow", "Tools"))
        self.menuCreate_Input_Template.setTitle(_translate("MainWindow", "Create Input Template"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen_Datasheet_Compare.setText(_translate("MainWindow", "Open Datasheet Compare..."))
        self.actionOpen_Single_Simulation.setText(_translate("MainWindow", "Open Single Simulation"))
        self.action2_Level.setText(_translate("MainWindow", "2 Level"))
        self.action3_Level.setText(_translate("MainWindow", "3 Level"))
        self.actionChopper.setText(_translate("MainWindow", "Chopper"))
        self.actionCreate_Module_Template.setText(_translate("MainWindow", "Create Module Template"))
        self.actionNo_one_can_help_you_now.setText(_translate("MainWindow", "No one can help you now"))

        # My additions

        self.master_module_file_dict = {}

    def setup__widgets_and_views(self):
        self.simulationProgressBar.setValue(0)
        self.moduleSelectTreeWidget.setHeaderHidden(True)
        self.load_module_info()
        self.set__module_select_tree()

        # set up input file buttons
        self.openSimulationFile.clicked.connect(self.open__simulation_file)

        # click or double click to add modules to stack
        self.sendModuleFiletoStack.clicked.connect(self.send__selected_module_to_stack)
        self.moduleSelectTreeWidget.doubleClicked.connect(self.send__selected_module_to_stack)

        # click or double click to remove modules from stack
        self.pullModuleFilefromStack.clicked.connect(self.remove__selected_module_from_stack)
        self.selectedModuleStackListWidget.doubleClicked.connect(self.remove__selected_module_from_stack)

        self.addCustomModuleFile.clicked.connect(self.add__custom_module_to_tree_widget)
        # self.removeCustomModuleFile.clicked.connect(self.remove_module_file_from_tree)

        self.pullModuleFileStack_2Level.clicked.connect(partial(self.set__target_from_module_stack, self.moduleFileListWidget_2Level))
        self.pullModuleFileStack_outside_3Level.clicked.connect(partial(self.set__target_from_module_stack, self.outsideModuleListWidget_3Level))
        self.pullModuleFileStack_inside_3Level.clicked.connect(partial(self.set__target_from_module_stack, self.insideModuleListWidget_3Level))
        self.pullModuleFileStack_diode_3Level.clicked.connect(partial(self.set__target_from_module_stack, self.diodeModuleListWidget_3Level))
        self.pullModuleFileStack_chopper_Chopper.clicked.connect(partial(self.set__target_from_module_stack, self.chopperModuleListWidget_Chopper))
        self.pullModuleFileStack_diode_Chopper.clicked.connect(partial(self.set__target_from_module_stack, self.diodeModuleListWidget_Chopper))

        self.pushButton.clicked.connect(self.click__run_simulation)

        # self.templateInputFileButton_TwoLevel.clicked.connect(self.click__templateInputFileButton_TwoLevel)
        # self.templateModuleFileButton_TwoLevel.clicked.connect(self.click__templateModuleFileButton)
        # self.templateInputFileButton_ThreeLevel.clicked.connect(self.click__templateInputFileButton_ThreeLevel)
        # self.templateModuleFileButton_ThreeLevel.clicked.connect(self.click__templateModuleFileButton)
        #

    def set__module_select_tree(self):
        self.moduleSelectTreeWidget.clear()
        self.fill_item(self.moduleSelectTreeWidget.invisibleRootItem(), self.master_module_file_dict, 0)

    def send__selected_module_to_stack(self):
        if self.moduleSelectTreeWidget.currentItem().childCount() == 0:
            self.selectedModuleStackListWidget.addItem(self.moduleSelectTreeWidget.currentItem().text(0))

    def remove__selected_module_from_stack(self):
        if self.selectedModuleStackListWidget.currentItem() is not None:
            _ = self.selectedModuleStackListWidget.takeItem(self.selectedModuleStackListWidget.currentRow())
            del _

    def set__target_from_module_stack(self, target_list_widget):
        target_list_widget.clear()
        widget_items = []
        for i in range(self.selectedModuleStackListWidget.count()):
            widget_items.append(self.selectedModuleStackListWidget.item(i))
        for item in widget_items:
            target_list_widget.addItem(item.clone())
        target_list_widget.show()

    def add__custom_module_to_tree_widget(self):
        self.windowStatusBar.showMessage("Open a module file.")
        user_input__module_file, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Module File", "", "Excel Files (*.xlsx)")
        self.windowStatusBar.clearMessage()
        if user_input__module_file is not "":
            user_input__part_category, _ = QtWidgets.QInputDialog.getText(None, "Part Description", "Please enter a part description (i.e. Automotive, Competitor Name, etc.)")
            user_input__voltage_class_category, _ = QtWidgets.QInputDialog.getText(None, "Voltage Class", "Please enter a voltage class (i.e. 650, 1200, etc.)")
            refactored_module_file = ModuleJSON_class.ModuleForJSON(user_input__module_file)
            if "My Files" not in self.master_module_file_dict.keys():
                self.master_module_file_dict.update({"My Files": {user_input__part_category: {user_input__voltage_class_category: refactored_module_file}}})
            else:
                if user_input__part_category not in self.master_module_file_dict["My Files"].keys():
                    self.master_module_file_dict["My Files"].update({user_input__part_category: {user_input__voltage_class_category: refactored_module_file}})
                else:
                    if user_input__voltage_class_category not in self.master_module_file_dict["My Files"][user_input__part_category].keys():
                        self.master_module_file_dict["My Files"][user_input__part_category].update({user_input__voltage_class_category: refactored_module_file})
                    else:
                        self.master_module_file_dict["My Files"][user_input__part_category][user_input__voltage_class_category].update(refactored_module_file)
            self.set__module_select_tree()

    # def remove_module_file_from_tree(self):
    #     module_json_dict_copy = copy.deepcopy(self.module_json_dict)
    #     if self.moduleFileTreeWidget.currentItem() is not None:
    #         if self.get_top_level_parent(self.moduleFileTreeWidget.currentItem()) == "My Files":
    #             del self.find_current_item_in_dict(self.moduleFileTreeWidget.currentItem())
    #         self.module_json_dict = module_json_dict_copy
    #         self.fill_module_tree()

    def fill_item(self, item, value, count):
        if type(value) is dict:
            count += 1
            if count < 5:
                for key, val in sorted(value.items()):
                    child = QtWidgets.QTreeWidgetItem()
                    child.setText(0, str(key))
                    item.addChild(child)
                    self.fill_item(child, val, count)
        elif type(value) is list:
            for val in value:
                child = QtWidgets.QTreeWidgetItem()
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, '[dict]')
                    self.fill_item(child, val, count)
                elif type(val) is list:
                    child.setText(0, '[list]')
                    self.fill_item(child, val, count)
                else:
                    child.setText(0, str(val))
                child.setExpanded(True)
        else:
            child = QtWidgets.QTreeWidgetItem()
            child.setText(0, str(value))
            item.addChild(child)
            count = 0

    def load_module_info(self):
        with open('module_info.json') as f:
            self.master_module_file_dict = json.loads(f.read())

    def open__simulation_file(self):
        self.windowStatusBar.showMessage("Open an input file.")
        user_input__simulation_input_file_location, _ = QtWidgets.QFileDialog.getOpenFileName(None, "Open Input File", "", "Excel Files (*.xlsx)")
        self.userInput__SimulationInputFileLocation.setText(user_input__simulation_input_file_location)
        self.windowStatusBar.clearMessage()

    def click__run_simulation(self):
        simulation_instance = None
        ok_to_simulate = False
        self.simulationProgressBar.setValue(0)

        if self.check__problem_with_inputs():
            return

        user_input__output_file_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Output File Location", os.getcwd())

        if user_input__output_file_location == "":
            self.popup__error_box("No output file selected.")
            return

        if self.mainTabWidget.currentIndex() == 1:
            three_level_flag = False
            module_list = self.get__list_from_target_widget(self.moduleFileListWidget_2Level)
            user_input__modulation_type = self.modulationTypeCombo_2Level.currentText()
            ok_to_simulate = True

        if self.mainTabWidget.currentIndex() == 2:
            three_level_flag = True
            inside_module_list = self.get__list_from_target_widget(self.insideModuleListWidget_3Level)
            outside_module_list = self.get__list_from_target_widget(self.outsideModuleListWidget_3Level)
            diode_module_list = self.get__list_from_target_widget(self.diodeModuleListWidget_3Level)
            user_input__modulation_type = self.modulationTypeCombo_3Level.currentText()
            ok_to_simulate = True

        if self.mainTabWidget.currentIndex() == 3:
            self.popup__error_box("Chopper config not done yet, try later.")
            return

        if ok_to_simulate:
            simulation_instance = Simulation_class.InputOperation(self.master_module_file_dict,
                                                                  self.RGSuppressCheckbox.isChecked(),
                                                                  user_input__modulation_type,
                                                                  three_level_flag,
                                                                  module_max_temp=self.maxCurrentTemp.value(),
                                                                  nerd_output_flag=self.advancedOutputCheckbox.isChecked(),
                                                                  tj_hold_flag=self.maxCurrentOutputEnable.isChecked())

        if self.mainTabWidget.currentIndex() == 1:
            simulation_instance.load__module_filename_list(module_list)

        if self.mainTabWidget.currentIndex() == 2:
            simulation_instance.load__module_filename_list(inside_module_list, outside_module_list, diode_module_list)

        if simulation_instance is not None:
            simulation_instance.load_user_inputs(self.userInput__SimulationInputFileLocation.text())
            simulation_instance.set_output_file_location(user_input__output_file_location)
            simulation_instance.run__straight_simulation(self.simulationProgressBar)
            simulation_instance.save__output_file()
            print("Finished at: " + time.strftime("%H:%M:%S"))
        else:
            self.popup__error_box("Something went wrong")
            return

    def popup__error_box(self, input_string):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText(input_string)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        msg.exec_()

    def check__problem_with_inputs(self):
        tab = self.mainTabWidget.currentIndex()
        if tab == 0:
            return True
        if self.userInput__SimulationInputFileLocation.text() == "":
            self.popup__error_box("There is no simulation input file.")
            return True
        if tab == 1:
            if self.moduleFileListWidget_2Level.count() == 0:
                self.popup__error_box("There are no module files to simulate.")
                return True
        if tab == 2:
            outside_list__is_empty = self.outsideModuleListWidget_3Level.count() == 0
            inside_list__is_empty = self.insideModuleListWidget_3Level.count() == 0
            diode_list__is_empty = self.diodeModuleListWidget_3Level.count() == 0
            if outside_list__is_empty or inside_list__is_empty or diode_list__is_empty:
                self.popup__error_box("One of your module lists is empty.")
                return True
        if tab == 3:
            diode_list__is_empty = self.diodeModuleListWidget_Chopper.count() == 0 and self.enableDiodeModule.isChecked()
            chopper_list_empty = self.chopperModuleListWidget_Chopper.count() == 0
            if diode_list__is_empty or chopper_list_empty:
                self.popup__error_box("One of your module lists is empty.")
                return True
        return False

    def get__list_from_target_widget(self, list_widget):
        items = []
        for index in range(list_widget.count()):
            items.append(list_widget.item(index))
        labels = [i.text() for i in items]
        return labels

    def click__templateInputFileButton_TwoLevel(self):
        output_file_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Output File Location", os.getcwd())
        if output_file_location is not "":
            sim_tools.input_file_template_maker(output_file_location)

    def click__templateModuleFileButton(self):  # Module file will still apply for all devices
        output_file_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Output File Location", os.getcwd())
        if output_file_location is not "":
            sim_tools.module_file_template_maker(output_file_location)

    def click__templateInputFileButton_ThreeLevel(self):  # will need to fix when three level input template is made
        output_file_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Output File Location", os.getcwd())
        if output_file_location is not "":
            sim_tools.input_file_template_maker(output_file_location)

    # def click__module_file_template(self):
    #     output_file_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Output File Location", os.getcwd())
    #     if output_file_location is not "":
    #         sim_tools.module_file_template_maker(output_file_location)
    #
    # def click__input_file_template_two_level(self):
    #     output_file_location = QtWidgets.QFileDialog.getExistingDirectory(None, "Output File Location", os.getcwd())
    #     if output_file_location is not "":
    #         sim_tools.input_file_template_maker(output_file_location)

    # !!! DON'T DELETE YET, NOT IMPLEMENTED

    # def click__datasheet_compare(self):
    #     if self.main_tab.currentIndex() == 1:
    #         try:
    #             plt.figure(1)
    #             plt.clf()
    #             plt.figure(2)
    #             plt.clf()
    #             plt.figure(5)
    #             plt.clf()
    #             plt.figure(6)
    #             plt.clf()
    #             plt.figure(3)
    #             plt.clf()
    #             plt.figure(4)
    #             plt.clf()
    #             count = 1
    #             for module_file in self.module_file_list:
    #                 file_values = sim_tools.module_file_reader(module_file)  # gets module file information
    #                 ic__ic_vce = file_values["IC - IC VCE"]
    #                 vce__ic_vce = file_values["VCE - IC VCE"]
    #                 if__if_vf = file_values["IF - IF VF"]
    #                 vf__if_vf = file_values["VF - IF VF"]
    #                 ic__ic_eswon = file_values["IC - IC ESWON"]
    #                 ic__ic_eswon_temp = sim_tools.origin_remover(ic__ic_eswon)
    #                 eswon__ic_eswon = file_values["ESWON - IC ESWON"]
    #                 eswon__ic_eswon_temp = sim_tools.origin_remover(eswon__ic_eswon)
    #                 ic__ic_eswoff = file_values["IC - IC ESWOFF"]
    #                 ic__ic_eswoff_temp = sim_tools.origin_remover(ic__ic_eswoff)
    #                 eswoff__ic_eswoff = file_values["ESWOFF - IC ESWOFF"]
    #                 eswoff__ic_eswoff_temp = sim_tools.origin_remover(eswoff__ic_eswoff)
    #                 ic__ic_err = file_values["IC - IC ERR"]
    #                 ic__ic_err_temp = sim_tools.origin_remover(ic__ic_err)
    #                 err__ic_err = file_values["ERR - IC ERR"]
    #                 err__ic_err_temp = sim_tools.origin_remover(err__ic_err)
    #                 module_name = file_values["Module Name"]
    #                 print(module_name)
    #
    #                 plt.figure(5)
    #                 tck = splrep(vce__ic_vce, ic__ic_vce, s=0)  # smooth curves for better viewing
    #                 xnew = arange(vce__ic_vce.min(), vce__ic_vce.max(), 0.01)
    #                 ynew = splev(xnew, tck, der=0)
    #                 plt.plot(xnew, ynew, label=module_name)
    #                 plt.xlabel(r'$V_{CE}$ [V]')
    #                 plt.ylabel(r'$I_C$ [A]')
    #                 plt.title(r'$I_C-V_{CE}$')
    #                 plt.legend()
    #                 plt.figure(5).canvas.draw()
    #
    #                 plt.figure(6)
    #                 tck = splrep(vf__if_vf, if__if_vf, s=0)  # smooth curves for better viewing
    #                 xnew = arange(vf__if_vf.min(), vf__if_vf.max(), 0.01)
    #                 ynew = splev(xnew, tck, der=0)
    #                 plt.plot(xnew, ynew, label=module_name)
    #                 plt.xlabel(r'$V_F$ [V]')
    #                 plt.ylabel(r'$I_F$ [A]')
    #                 plt.title(r'$I_F-V_F$')
    #                 plt.legend()
    #                 plt.figure(6).canvas.draw()
    #
    #                 plt.figure(3)
    #                 tck = splrep(ic__ic_eswon_temp, eswon__ic_eswon_temp, s=0)  # smooth curves for better viewing
    #                 xnew = arange(ic__ic_eswon_temp.min(), ic__ic_eswon_temp.max(), 0.01)
    #                 ynew = splev(xnew, tck, der=0)
    #                 plt.plot(xnew, ynew, label=module_name)
    #                 tck = splrep(ic__ic_eswoff_temp, eswoff__ic_eswoff_temp, s=0)  # smooth curves for better viewing
    #                 xnew = arange(ic__ic_eswoff_temp.min(), ic__ic_eswoff_temp.max(), 0.01)
    #                 ynew = splev(xnew, tck, der=0)
    #                 plt.plot(xnew, ynew, label=module_name)
    #                 plt.xlabel(r'$I_C$ [A]')
    #                 plt.ylabel(r'$E_{SW}$ [mJ]')
    #                 plt.title(r'$I_C-E_{SW}$')
    #                 plt.legend()
    #                 plt.figure(3).canvas.draw()
    #
    #                 plt.figure(4)
    #                 tck = splrep(ic__ic_err_temp, err__ic_err_temp, s=0)  # smooth curves for better viewing
    #                 xnew = arange(ic__ic_err_temp.min(), ic__ic_err_temp.max(), 0.01)
    #                 ynew = splev(xnew, tck, der=0)
    #                 plt.plot(xnew, ynew, label=module_name)
    #                 plt.xlabel(r'$I_C$ [A]')
    #                 plt.ylabel(r'$E_{RR}$ [mJ]')
    #                 plt.title(r'$I_C-E_{RR}$')
    #                 plt.legend()
    #                 plt.figure(4).canvas.draw()
    #
    #                 plt.figure(1)
    #                 count2 = 0
    #                 for x in [count, count + len(self.module_file_list), count + 2 * len(self.module_file_list)]:
    #                     rth_list = [file_values['IGBT RTH DC'], file_values['FWD RTH DC'], file_values['Module RTH DC']]
    #                     if x < len(self.module_file_list) + 1:
    #                         plt.bar(x, rth_list[count2], label=file_values['Module Name'])
    #                     else:
    #                         plt.bar(x, rth_list[count2])
    #                     count2 = count2 + 1
    #                 ind = [0.5 + 0.5 * len(self.module_file_list), 0.5 + 1.5 * len(self.module_file_list), 0.5 + 2.5 * len(self.module_file_list)]
    #                 plt.xticks(ind, ["IGBT RTH", "FWD RTH", "Module Contact RTH"])
    #                 plt.legend()
    #                 plt.ylabel(r'$r_{th}$ [K/kW]')
    #                 plt.title('Thermal Impedance (DC)')
    #                 plt.figure(1).canvas.draw()
    #
    #                 plt.figure(2)
    #                 t = logspace(-7, .301, 500)
    #                 fwd_trans = []
    #                 igbt_trans = []
    #                 for t_val in t:
    #                     fwd_trans.append(float(sim_tools.get_fwd_rth_from_time(t_val, file_values)) / file_values['FWD RTH DC'])
    #                     igbt_trans.append(float(sim_tools.get_igbt_rth_from_time(t_val, file_values)) / file_values['IGBT RTH DC'])
    #                 plt.loglog(t, igbt_trans, label=str(module_name) + ' IGBT')
    #                 plt.loglog(t, fwd_trans, label=str(module_name) + ' FWD')
    #                 plt.xlabel('time [s]')
    #                 plt.ylabel(r'$r_{th}$ [K/kW]')
    #                 plt.title('Transient Thermal Impedance')
    #                 plt.legend()
    #                 plt.figure(2).canvas.draw()
    #
    #                 count = count + 1
    #
    #         except UnboundLocalError:
    #             msg = QtWidgets.QMessageBox()
    #             msg.setIcon(QtWidgets.QMessageBox.Information)
    #             msg.setText("Something is missing.")
    #             msg.setInformativeText("Make sure you have an input file, an output file and a modulation type.")
    #             msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
    #             msg.exec_()
    #         except KeyError:
    #             msg = QtWidgets.QMessageBox()
    #             msg.setIcon(QtWidgets.QMessageBox.Information)
    #             msg.setText("A value I need is not here.")
    #             msg.setInformativeText("Check your input and module files and compare them to a template file.")
    #             msg.setStandardButtons(QtWidgets.QMessageBox.Cancel)
    #             msg.exec_()


sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = my_exception_hook

logger = logging.getLogger("Rotating Log")
logger.setLevel(logging.ERROR)
handler = RotatingFileHandler("log.txt", maxBytes=10000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

if __name__ == "__main__":
    try:
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(str(e))
        logger.error(traceback.format_exc())
