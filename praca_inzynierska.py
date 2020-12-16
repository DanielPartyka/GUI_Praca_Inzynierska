import os
import shutil
import traceback
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QFont
from PyQt5.QtWidgets import QGraphicsRectItem, QMainWindow, QFileDialog, QMessageBox, \
    QGraphicsTextItem
from PIL import Image
from zipfile import ZipFile
import tarfile
import cv2
import pandas as pd
import numpy as np
import scipy.io
from uamf import BlockMeta
from uamf.ds import Size, Point

from window import MainWindow1, rect_list

# Block object list
moveObjectList = []
# Block numeration list
textObjectList = []
# Block index and object dictionary
block_definition_dict = {}
# Contrast and brightness values
alpha_beta = [50,10]

# class, stands for block numeration
class NumerationOfSpot(QGraphicsTextItem):
    def __init__(self,id):
        super().__init__()
        self.id = id
        self.setPos(0,0)
        self.setFont(QFont('Times', 80))
        self.setDefaultTextColor((QColor(255, 255, 255, 100)))

    def get_id(self):
        return self.id

    def visibility_f(self):
        self.setVisible(False)

    def visibility_t(self):
        self.setVisible(True)

# class, stands for block created by block definition
class StaticObject(QGraphicsRectItem):
    x0cord = 0
    x1cord = 0
    y0cord = 0
    y1cord = 0
    def __init__(self, x, y, w, h,id):
        super().__init__(0, 0, w, h)
        self.id = id
        self.w = w
        self.h = h
        self.setBrush(QBrush(QColor(255, 0, 0, 100)))
        self.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        self.setPos(x, y)
        self.setAcceptHoverEvents(True)
        StaticObject.amount_of_spots = 0
        StaticObject.x0cord = 0
        StaticObject.x1cord = 0
        StaticObject.y0cord = 0
        StaticObject.y1cord = 0
        StaticObject.mode_of_working = 'AD'

    # Getters and Setters of class

    def get_id(self):
        return self.id

    def get_w(self):
        return self.w

    def get_h(self):
        return self.h

    def set_x0cord(self,x0):
        StaticObject.x0cord = x0

    def set_x1cord(self,x1):
        StaticObject.x1cord = x1

    def set_y0cord(self,y0):
        StaticObject.y0cord = y0

    def set_y1cord(self,y1):
        StaticObject.y1cord = y1

    def get_x0cord(self):
        return StaticObject.x0cord

    def get_x1cord(self):
        return StaticObject.x1cord

    def get_y0cord(self):
        return StaticObject.y0cord

    def get_y1cord(self):
        return StaticObject.y1cord

    def set_amount_of_spots(self,value):
        StaticObject.amount_of_spots = value

    def get_amount_of_spots(self):
        return StaticObject.amount_of_spots

    def set_mode_of_working(self, mode):
        StaticObject.mode_of_working = mode

    def get_mode_of_working(self):
        return StaticObject.mode_of_working

    # Mouse events, triggered by block move

    def mouseMoveEvent(self, event):

        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        # Current block cords
        y0 = int(self.y())
        x0 = int(self.x())
        y1 = int(StaticObject.get_h(self))
        x1 = int(StaticObject.get_w(self))

        block_size_x = StaticObject.get_w(self)
        block_size_y = StaticObject.get_h(self)

        # Checking image borders
        if updated_cursor_x >= 0 and updated_cursor_y >= 0 and updated_cursor_x <= im_size[1] - block_size_x and updated_cursor_y <= im_size[0] - block_size_y:
                self.setPos(QPointF(updated_cursor_x, updated_cursor_y))
                # Updating the cords of block
                block_definition_dict[StaticObject.get_id(self)].position.x = x0
                block_definition_dict[StaticObject.get_id(self)].position.y = y0
                block_definition_dict[StaticObject.get_id(self)].width = x1
                block_definition_dict[StaticObject.get_id(self)].height = y1

        # Change color of block after moving
        self.setBrush(QBrush(QColor(0, 0, 255, 100)))
        self.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        # Setting block modification status to true
        block_definition_dict['block' + str(StaticObject.get_id(self))] = 'Yes'

    def mousePressEvent(self, event):
        for tol in textObjectList:
            if tol.id == int(StaticObject.get_id(self)):
                tol.visibility_f()

    def mouseReleaseEvent(self,event):

        self.set_net_of_spots_on_image()
        Ui_MainWindow.open_new_window(self, 'temporary_images/temporaryimage1.png','Block: ' + str(StaticObject.get_id(self)),StaticObject.get_id(self))

    # Function which creates a spot net in block
    def set_net_of_spots_on_image(self):

        image_o = Image.open(path_of_file)
        img = np.array(image_o)
        y0 = int(self.y())
        x0 = int(self.x())
        y1 = int(StaticObject.get_h(self) + int(self.y()))
        x1 = int(StaticObject.get_w(self) + int(self.x()))

        npimg = image_o.crop((x0, y0, x1, y1))
        imsave = npimg.save('temporary_images/temporaryimage.png')

        imagee = cv2.imread('temporary_images/temporaryimage.png')[..., ::-1]

        alpha = alpha_beta[0]
        beta = alpha_beta[1]

        resized = cv2.convertScaleAbs(imagee, alpha=alpha, beta=beta)
        h, w, c = resized.shape

        nColumns = block_definition_dict[StaticObject.get_id(self)].columns_number
        nRows = block_definition_dict[StaticObject.get_id(self)].rows_number

        # x0 left corner green block
        start_x0_cord_green = 0
        # x0 left corner red block
        start_x0_cord_red = 14
        # y0 start top margin
        y0 = 0
        # x1 cord
        x1_cord = 0

        padding = 4

        width_of_block = int(w / nColumns)
        height_of_block = int((h + (nRows * 5)) / nRows)

        thickness = 1
        iteration = 0
        block_width = width_of_block
        block_width_red = width_of_block + start_x0_cord_red

        # Draw the spot
        for rows in range(0, nRows):
            iteration += 1
            if iteration > 1:
                y0 += height_of_block - 5
                block_width = width_of_block
                start_x0_cord_green = 0
                start_x0_cord_red = 15
                block_width_red = width_of_block + start_x0_cord_red
            for columns in range(0, nColumns):
                if iteration % 2 != 0:
                    resized = cv2.rectangle(resized, (start_x0_cord_green + padding, y0),
                                            (block_width, height_of_block + y0), (0, 255, 0), thickness)
                    start_x0_cord_green += width_of_block
                    block_width += width_of_block
                else:
                    resized = cv2.rectangle(resized, (start_x0_cord_red + padding, y0),
                                            (block_width_red, height_of_block + y0), (0, 0, 255), thickness)
                    start_x0_cord_red += width_of_block
                    block_width_red += width_of_block

        cv2.imwrite('temporary_images/temporaryimage1.png', resized)

        for tol in textObjectList:
            if tol.id == int(StaticObject.get_id(self)):
                tol.visibility_t()
                tol.setPos(int(self.x() + 35), int(self.y()))

# Main window class
class Ui_MainWindow(object):
    # Generate a new window
    def open_new_window(self, image, name, block_id):
        if block_id in rect_list:
            if self.window.isHidden():
                self.window = QtWidgets.QMainWindow()
                rect_list.remove(block_id)
                self.window.setWindowTitle(name)
                self.ui = MainWindow1()
                self.ui.setupUi(self.window)
                self.ui.setImage(image, block_id)
                self.window.show()
            else:
                self.ui.setImage(image,block_id)
        else:
            self.window = QtWidgets.QMainWindow()
            self.window.setWindowTitle(name)
            self.ui = MainWindow1()
            self.ui.setupUi(self.window)
            self.ui.setImage(image,block_id)
            self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1045)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1920, 1080))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.graphicsView = QtWidgets.QGraphicsView(self.tab)
        self.graphicsView.setGeometry(QtCore.QRect(50, 50, 1811, 771))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.viewport().installEventFilter(self)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(240, 10, 681, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(880, 10, 681, 31))
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label")
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.tab)
        self.horizontalScrollBar.setGeometry(QtCore.QRect(340, 890, 291, 31))
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.horizontalScrollBar_2 = QtWidgets.QScrollBar(self.tab)
        self.horizontalScrollBar_2.setGeometry(QtCore.QRect(700, 890, 291, 31))
        self.horizontalScrollBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar_2.setObjectName("horizontalScrollBar_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(390, 830, 221, 51))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(740, 830, 221, 51))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(1070, 870, 211, 51))
        self.pushButton.setObjectName("pushButton")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tableWidget = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget.setGeometry(QtCore.QRect(50, 50, 1811, 771))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(11)
        self.tableWidget.setHorizontalHeaderLabels(['Block number','x0 (pixels)','y0 (pixels)','x1 (pixels)','y1 (pixels)','width (pixels)','height (pixels)','rows number','column number', 'amount of spots', 'Modified'])
        self.tableWidget.setColumnWidth(0, 163)
        self.tableWidget.setColumnWidth(1, 163)
        self.tableWidget.setColumnWidth(2, 163)
        self.tableWidget.setColumnWidth(3, 163)
        self.tableWidget.setColumnWidth(4, 163)
        self.tableWidget.setColumnWidth(5, 163)
        self.tableWidget.setColumnWidth(6, 163)
        self.tableWidget.setColumnWidth(7, 163)
        self.tableWidget.setColumnWidth(8, 163)
        self.tableWidget.setColumnWidth(9, 163)
        self.tableWidget.setColumnWidth(10, 163)
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(540, 10, 681, 31))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1548, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSave_as = QtWidgets.QMenu(self.menuFile)
        self.menuSave_as.setObjectName("menuSave_as")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpenBlockDef = QtWidgets.QAction(MainWindow)
        self.actionOpenBlockDef.setObjectName("actionOpenBlockDef")
        self.actionHTML = QtWidgets.QAction(MainWindow)
        self.actionHTML.setObjectName("actionHTML")
        self.actionJSON = QtWidgets.QAction(MainWindow)
        self.actionJSON.setObjectName("actionJSON")
        self.actionMS_Excel = QtWidgets.QAction(MainWindow)
        self.actionMS_Excel.setObjectName("actionMS_Excel")
        self.actioncsv = QtWidgets.QAction(MainWindow)
        self.actioncsv.setObjectName("actioncsv")
        self.actionHDF5 = QtWidgets.QAction(MainWindow)
        self.actionHDF5.setObjectName("actionHDF5")
        self.menuSave_as.addAction(self.actionHTML)
        self.menuSave_as.addAction(self.actionJSON)
        self.menuSave_as.addAction(self.actionMS_Excel)
        self.menuSave_as.addAction(self.actioncsv)
        self.menuSave_as.addAction(self.actionHDF5)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpenBlockDef)
        self.menuFile.addAction(self.menuSave_as.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Listeners
        self.horizontalScrollBar.valueChanged.connect(self.change_size_alpha)
        self.horizontalScrollBar_2.valueChanged.connect(self.change_size_beta)
        self.pushButton.clicked.connect(self.change_alpha_beta_listener)
        self.actionHTML.triggered.connect(lambda: self.save_results("html"))
        self.actioncsv.triggered.connect(lambda: self.save_results("csv"))
        self.actionHDF5.triggered.connect(lambda: self.save_results("hdf5"))
        self.actionJSON.triggered.connect(lambda: self.save_results("json"))
        self.actionMS_Excel.triggered.connect(lambda: self.save_results("excel"))
        self.actionOpenBlockDef.triggered.connect(self.change_spot_definition)
        self.actionOpen.triggered.connect(self.add_im)

        self.pushButton.setVisible(False)
        self.horizontalScrollBar.setVisible(False)
        self.horizontalScrollBar_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_4.setVisible(False)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.graphicsView.setScene(self.scene)
        start_im = 'project_images/image_not_available.png'
        self.scene.clear()
        self.pixmap = QPixmap(start_im)
        self.scale = 1.0
        size = self.pixmap.size()
        scaled_pixmap = self.pixmap.scaled(self.scale * size)
        self.scene.addPixmap(scaled_pixmap)
        self.view.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
        self.label.setText("No image uploaded, you have to upload an image")
        self.label_8.setText("No block definition uploaded, you have to load the definition of blocks")
        self.label_2.setText("No block definition uploaded, you have to load the definition of blocks to see table results")
        self.actionOpenBlockDef.setVisible(False)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GUI wspomagające proces postprocessingu obrazów mikromacierzowych"))
        MainWindow.setStyleSheet(open("QSS/style.qss", "r").read())
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Value of Alpha (Contrast)"))
        self.label_4.setText(_translate("MainWindow", "Value of Beta (Brightness)"))
        self.pushButton.setText(_translate("MainWindow","Change"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Blocks on image"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Table with results"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpenBlockDef.setText(_translate("MainWindow","Open block definition"))
        self.menuSave_as.setTitle(_translate("MainWindow", "Save results as"))
        self.actionOpen.setText(_translate("MainWindow", "Open Image"))
        self.actionHTML.setText(_translate("MainWindow", "HTML"))
        self.actionJSON.setText(_translate("MainWindow", "JSON"))
        self.actionMS_Excel.setText(_translate("MainWindow", "MS Excel"))
        self.actioncsv.setText(_translate("MainWindow", "CSV"))
        self.actionHDF5.setText(_translate("MainWindow", "HDF5"))

    # Event filter which catches exiting of the block spot net
    def eventFilter(self, source, event):
        if event.type() == 24 and len(block_definition_dict) > 0:
            n = 48
            self.filltable(n)
        return super(MainWindow, self).eventFilter(source, event)

    # Opening the block definition spot
    def define_block_spot(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            file, _ = QFileDialog.getOpenFileName(None, 'Openfile', '', 'Compresed file(*.zip *.tar.gz)')

            if file:
                splited_file = file.split('/')[-1]
                extension = splited_file.split('.')[-1]

                self.clear_MatReading_folder()

                try:
                    if extension == 'gz':
                        my_tar = tarfile.open(file)
                        my_tar.extractall('MatReading/')
                        my_tar.close()
                    elif extension == 'zip':
                        zf = ZipFile(file, 'r')
                        zf.extractall('MatReading/')
                        zf.close()
                except:
                    msg = QMessageBox()
                    msg.setWindowTitle("Extracting")
                    msg.setText("There is a problem with extracting file. Files must have extensions .zip or .tar.gz")
                    msg.setIcon(QMessageBox.Warning)
                    x = msg.exec_()
                    return 0

                for files in os.walk('MatReading'):
                    st = str(files[0])
                    if st != 'MatReading':
                        name_of_block_location_folder = os.path.split(st)[-1]

                image = path_of_file

                moveObjectList.clear()
                textObjectList.clear()
                rect_list.clear()

                self.scene.clear()
                self.clearing_table()
                self.scene.addPixmap(QPixmap(image))

                Number_Of_Files = 0
                path = os.path.dirname(__file__)
                path_of_mat = path + "/MatReading/" + name_of_block_location_folder

                for files in os.walk(path_of_mat):
                    for files in path:
                        Number_Of_Files = Number_Of_Files + 1

                tif = image.split('/')[-1]
                tif2 = tif.split('.')[-1]

                if tif2 == 'tif':
                    image_o = Image.open(image)
                    im = np.array(image_o)
                    w, h = im.shape
                else:
                    im = cv2.imread(image)
                    w, h, c = im.shape

                im_size = w, h
                # amount of blocks
                n = Number_Of_Files - 4
                counter = 0
                if n >= 3:
                    for i in range(0, n):

                        for files in os.walk(path_of_mat):
                            for f in files:
                                for x in f:
                                    if str(i+1) in x:
                                        mat_path = x
                                        break

                        # Reading MetaData from .mat files
                        mat = scipy.io.loadmat('MatReading/' + name_of_block_location_folder + '/' + mat_path)
                        math_key = mat_path.split('.')
                        posy = mat[math_key[0]]['blockHeightPix'][0][0][0][0]
                        posx = mat[math_key[0]]['blockWidthPix'][0][0][0][0]
                        centerx = mat[math_key[0]]['blockCornerX'][0][0][0][0]
                        centery = mat[math_key[0]]['blockCornerY'][0][0][0][0]
                        amount_of_columns = mat[math_key[0]]['nColumns'][0][0][0][0]
                        amount_of_rows = mat[math_key[0]]['nRows'][0][0][0][0]
                        amount_of_spots = mat[math_key[0]]['nFeatures'][0][0][0][0]

                        block = BlockMeta(mat_path, Size(posy, posx), amount_of_rows, amount_of_columns, amount_of_spots, mat_path, Point(centerx,centery),list)
                        block_definition_dict[i+1] = block
                        block_definition_dict['block' + str(i+1)] = 'No'

                        # Draw blocks on image
                        if counter == 0:
                            moveObject = StaticObject(centerx, centery, posx, posy, i + 1)
                            nos = NumerationOfSpot(i + 1)
                            nos.setPos(centerx * 1.15, centery)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter += 1
                        elif counter == 1:
                            moveObject = StaticObject(centerx, centery, posx, posy, i + 1)
                            nos = NumerationOfSpot(i + 1)
                            nos.setPos(centerx * 1.05, centery)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter += 1
                        elif counter == 2:
                            moveObject = StaticObject(centerx, centery, posx, posy, i + 1)
                            nos = NumerationOfSpot(i + 1)
                            nos.setPos(centerx * 1.02, centery)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter += 1
                        elif counter == 3:
                            moveObject = StaticObject(centerx, centery, posx, posy, i + 1)
                            nos = NumerationOfSpot(i + 1)
                            nos.setPos(centerx * 1.01, centery)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter = 0

                for x in moveObjectList:
                    self.scene.addItem(x)
                for y in textObjectList:
                    self.scene.addItem(y)

                self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
                self.filltable(n)
                self.horizontalScrollBar.setVisible(True)
                self.horizontalScrollBar_2.setVisible(True)
                self.label_3.setVisible(True)
                self.label_4.setVisible(True)
                self.pushButton.setVisible(True)
                self.horizontalScrollBar.setMinimum(0)
                self.horizontalScrollBar.setMaximum(100)
                self.horizontalScrollBar_2.setMinimum(0)
                self.horizontalScrollBar_2.setMaximum(100)
                self.horizontalScrollBar.setValue(50)
                self.horizontalScrollBar_2.setValue(10)
                self.label_3.setText('Value of Alpha (Contrast): ' + str(self.horizontalScrollBar.value()))
                self.label_4.setText('Value of Beta (Brightness): ' + str(self.horizontalScrollBar_2.value()))
                self.label_8.setText('Uploaded block definition: ' + str(splited_file))

            else:
                msg = QMessageBox()
                msg.setWindowTitle("block definition")
                msg.setText("Block definition loading has been canceled")
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()
        except Exception:
            msg = QMessageBox()
            msg.setWindowTitle("Block definition")
            msg.setText("Something went wrong with loading block definition " +  str(traceback.print_exc()))
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

    # Changing value of contrast
    def change_size_alpha(self):
        value = self.horizontalScrollBar.value()
        self.label_3.setText('Value of Alpha (Contrast): ' + str(value))

    # Changing value of brightness
    def change_size_beta(self):
        value = self.horizontalScrollBar_2.value()
        self.label_4.setText('Value of Beta (Brightness): ' + str(value))

    # Changing value of brightness and contrast
    def change_alpha_beta_listener(self):
        alpha = self.horizontalScrollBar.value()
        beta = self.horizontalScrollBar_2.value()
        alpha_changed = False
        beta_changed = False
        msg = QMessageBox()
        if alpha_beta[0] != alpha:
            alpha_beta[0] = alpha
            alpha_changed = True
        if alpha_beta[1] != beta:
            alpha_beta[1] = beta
            beta_changed = True

        msg.setWindowTitle("Changed Values")
        if alpha_changed == True and beta_changed == True:
            msg.setText("The contrast and the brightness have been set to: " + str(alpha) + " and " + str(beta))
        elif alpha_changed == True and beta_changed == False:
            msg.setText("The contrast have been set to: " + str(alpha))
        elif alpha_changed == False and beta_changed == True:
            msg.setText("The brightness have been to: " + str(beta))
        else: msg.setText("Nothing changed")

        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

    # Function which saves the result of table
    def save_results(self, save_as):
        try:
            sResultList = []
            for i in range(0,48):
                sResultList.append([block_definition_dict[i+1].position.x,block_definition_dict[i+1].position.y,
                                    block_definition_dict[i+1].width + block_definition_dict[i+1].position.x,
                                    block_definition_dict[i+1].height + block_definition_dict[i+1].position.y,
                                    block_definition_dict[i+1].width, block_definition_dict[i+1].height,
                                    block_definition_dict[i+1].rows_number, block_definition_dict[i+1].columns_number,
                                    block_definition_dict[i+1].spots_number, block_definition_dict['block' + str(i+1)]])
            if not sResultList:
                msg = QMessageBox()
                msg.setWindowTitle("Saving data")
                msg.setText("There is no data to save")
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()
            else:
                options = QFileDialog.Options()
                options |= QFileDialog.DontUseNativeDialog
                res = QFileDialog.getSaveFileName()
                name_of_file = res[0].split('/')

                df = pd.DataFrame(sResultList, index=list(range(1,len(sResultList)+1)), columns=list(['x0 (pixels)','y0 (pixels)','x1 (pixels)','y1 (pixels)',
                                                            'width (pixels)','height (pixels)','rows number','columns number', 'amount of spots', 'Modified']))
                if save_as == 'html':
                    df.to_html(res[0] + '.html')

                    msg = QMessageBox()
                    msg.setWindowTitle("Saving")
                    msg.setText("Saved data as html file")
                    msg.setIcon(QMessageBox.Information)
                    x = msg.exec_()

                elif save_as == "csv":
                    df.to_csv(res[0] + '.csv')

                    msg = QMessageBox()
                    msg.setWindowTitle("Saving")
                    msg.setText("Saved data as csv file")
                    msg.setIcon(QMessageBox.Information)
                    x = msg.exec_()

                elif save_as == 'hdf5':
                    df.to_hdf(res[0] + '.h5', 'df', append=True)

                    msg = QMessageBox()
                    msg.setWindowTitle("Saving")
                    msg.setText("Saved data as h5 file")
                    msg.setIcon(QMessageBox.Information)
                    x = msg.exec_()

                elif save_as == 'json':
                    df.to_json(res[0] + '.json')

                    msg = QMessageBox()
                    msg.setWindowTitle("Saving")
                    msg.setText("Saved data as json file")
                    msg.setIcon(QMessageBox.Information)
                    x = msg.exec_()

                elif save_as == 'excel':
                    df.to_excel(res[0] + '.xlsx', sheet_name=str(name_of_file[-1]))

                    msg = QMessageBox()
                    msg.setWindowTitle("Saving")
                    msg.setText("Saved data as excel file")
                    msg.setIcon(QMessageBox.Information)
                    x = msg.exec_()

                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("Saving data")
                    msg.setText("There is a problem with saving results")
                    msg.setIcon(QMessageBox.Information)
                    x = msg.exec_()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Saving data")
            msg.setText("There is a problem with saving")
            msg.setIcon(QMessageBox.Warning)
            x = msg.exec_()

    # Open an image
    def opening_im(self):
        try:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            image, _ = QFileDialog.getOpenFileName(None, 'Openfile', '', 'im file(*.png *.jpg *.tif *jpeg)')
            if image:
                self.clearing_table()
                self.scene.clear()
                # Checking if files are in in /Images folder
                ROOT_DIR = os.path.abspath(os.curdir)
                file_n =  image.split('/')[-1]

                image_folder_file = ROOT_DIR + '/Images'
                fixed_image_folder = os.path.abspath(image_folder_file)
                file_nd = '/Images/' + file_n
                p = str(ROOT_DIR) + file_nd
                fixed_path = os.path.abspath(p)
                if os.path.exists(fixed_path) == False:
                    buttonReply = QMessageBox.question(self, 'Image', "Do you want save Image to the Image storage folder?",
                                                       QMessageBox.Yes | QMessageBox.No)
                    if buttonReply == QMessageBox.Yes:
                        shutil.copy(image,fixed_image_folder)
                    else:
                        pass
                else:
                    pass

                global im_size, start_photo, path_of_file, extension
                tif = image.split('/')[-1]
                tif2 = tif.split('.')[-1]

                if tif2 == 'tif':
                    image_o = Image.open(image)
                    im = np.array(image_o)
                    w, h = im.shape
                else:
                    im = cv2.imread(image)
                    w, h, c = im.shape

                path_of_file = image
                self.scene.addPixmap(QPixmap(image))
                im_size = w, h
                im_name = image.split('/')
                self.label_2.setText('You are currently working on: ' + str(im_name[-1]))
                self.label.setText('You are currently working on: ' + str(im_name[-1]))
                self.actionOpenBlockDef.setVisible(True)

            else:
                msg = QMessageBox()
                msg.setWindowTitle("Image")
                if image.endswith('.png') or image.endswith('.jpg') or image.endswith('.tif') or image.endswith('.jpeg') or not image:
                    msg.setText("Opening photo has been canceled")
                else:
                    msg.setText("Invalid format of file. Files must end with extension .png .jpg .tif .jpeg")
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()

        except Exception:
                msg = QMessageBox()
                msg.setWindowTitle("Image")
                msg.setText("There is a problem with image opening: " + str(traceback.print_exc()))
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()

    # Function that inform user that he will lose data if continue
    def change_spot_definition(self):
        if len(block_definition_dict)>0:
            buttonRep = QMessageBox.question(self, 'Result Data',"Do you want to continue? Unsaved data will be lost",
                                               QMessageBox.Yes | QMessageBox.Cancel)
            if buttonRep == QMessageBox.Yes:
                self.define_block_spot()
            else:
                return 0
        else:
            self.define_block_spot()

    # Delete the MatReading and it's content
    def clear_MatReading_folder(self):
        path = os.path.dirname(__file__)
        path_full = path + "/MatReading"
        shutil.rmtree(path_full)
        os.makedirs(path_full)


    # Change an image
    def add_im(self):
        if len(block_definition_dict)>0:
            buttonReply = QMessageBox.question(self, 'Result Data', "Do you want to continue? Unsaved data will be lost",
                                               QMessageBox.Yes | QMessageBox.Cancel)
            if buttonReply == QMessageBox.Yes:
                block_definition_dict.clear()
                self.scene.clear()
                self.opening_im()

            if buttonReply == QMessageBox.Cancel:
                return 0
        else:
            moveObjectList.clear()
            textObjectList.clear()
            self.opening_im()

    # Clearing table
    def clearing_table(self):
        self.tableWidget.setRowCount(0)

    # Filling table with block definiton data
    def filltable(self, amount_of_blocks):
        i = 0
        row = 0
        self.tableWidget.setRowCount(amount_of_blocks)
        for i in range(0,amount_of_blocks):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i+1)))
            self.tableWidget.setItem(row, 1 ,QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].position.x)))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].position.y)))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].width + block_definition_dict[i + 1].position.x)))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].height + block_definition_dict[i + 1].position.y)))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].width)))
            self.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].height)))
            self.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].rows_number)))
            self.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].columns_number)))
            self.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(str(block_definition_dict[i + 1].spots_number)))
            self.tableWidget.setItem(row, 10, QtWidgets.QTableWidgetItem(str(block_definition_dict['block' + str(i+1)])))
            row = row + 1
            i = i + 1

# MainWindow window class, parent of Ui_MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('project_images/TitleImage.png'))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
