from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QPixmap, QPen, QColor, QBrush, QFont, QImage
from PyQt5.QtWidgets import QGraphicsRectItem, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem, \
    QGraphicsTextItem, QLabel
from PIL import Image
from window import Ui_AnotherWindow
import cv2
import pandas as pd
import numpy as np
import scipy.io

wResultList = []
sResultList = []
moveObjectList = []
textObjectList = []
alpha_beta = [50,10]

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

    def getPos(self):
        xi = self.pos().x()
        yi = self.pos().y()
        print('xi: ' + str(xi))
        print('yi: ' + str(yi))


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

    def mouseMoveEvent(self, event):
        orig_cursor_position = event.lastScenePos()
        updated_cursor_position = event.scenePos()

        orig_position = self.scenePos()

        updated_cursor_x = updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        updated_cursor_y = updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()

        block_size_x = int(im_size[1] / 4)
        block_size_y = int(im_size[0] / 12)

        if updated_cursor_x >= 0 and updated_cursor_y >= 0 and updated_cursor_x <= im_size[1] - block_size_x and updated_cursor_y <= im_size[0] - block_size_y:
                self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mousePressEvent(self, event):
        for tol in textObjectList:
            if tol.id == int(StaticObject.get_id(self)):
                tol.visibility_f()

    def mouseReleaseEvent(self,event):
        image_o = Image.open(path_of_file)
        img = np.array(image_o)
        y0 = int(self.y())
        x0 = int(self.x())
        y1 = int(StaticObject.get_h(self) + int(self.y()))
        x1 = int(StaticObject.get_w(self) + int(self.x()))
        npimg = image_o.crop((x0,y0,x1,y1))
        imsave = npimg.save('temporary_images/Mojobrazek.png')

        imagee = cv2.imread('temporary_images/Mojobrazek.png')[...,::-1]

        alpha = alpha_beta[0]
        beta = alpha_beta[1]

        resized = cv2.convertScaleAbs(imagee, alpha=alpha, beta=beta)
        h, w, c = resized.shape
        # in cv2.rectangle (#im, (x0,y0), (x1,y1) ...
        mat = scipy.io.loadmat('MatReading/block01CordDef.mat')
        nColumns = mat['block01CordDef']['nColumns'][0][0][0][0]
        nRows = mat['block01CordDef']['nRows'][0][0][0][0]

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

        cv2.imwrite('temporary_images/obraz.png', resized)

        for tol in textObjectList:
            if tol.id == int(StaticObject.get_id(self)):
                tol.visibility_t()
                tol.setPos(int(self.x()+35),int(self.y()))

        #change color of block after moving
        self.setBrush(QBrush(QColor(0, 0, 255, 100)))
        self.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))

        Ui_MainWindow.open_new_window(self, 'temporary_images/obraz.png','Block: ' + str(StaticObject.get_id(self)))

class MovingObject(QGraphicsRectItem):
    amount_of_spots = 0
    x0cord = 0
    x1cord = 0
    y0cord = 0
    y1cord = 0
    """" There are three modes or working: AD = Automatic Detection which allows to dragging net with mouse and autosaving process to table,
    MD = Manual Detection which allows to manually adding values to table, and different mode which allows to clicking on X nets and performing
    some things """""
    mode_of_working = ['MD','AD','DM']
    def __init__(self, x, y, w, h):
        super().__init__(0, 0, w, h)
        self.setBrush(QBrush(QColor(0, 0, 255, 100)))
        self.setPen(QPen(QColor(0, 0, 0), 1.0, Qt.SolidLine))
        self.setPos(x, y)
        self.setAcceptHoverEvents(True)
        MovingObject.amount_of_spots = 0
        MovingObject.x0cord = 0
        MovingObject.x1cord = 0
        MovingObject.y0cord = 0
        MovingObject.y1cord = 0
        MovingObject.mode_of_working = 'AD'

    def set_x0cord(self,x0):
        MovingObject.x0cord = x0

    def set_x1cord(self,x1):
        MovingObject.x1cord = x1

    def set_y0cord(self,y0):
        MovingObject.y0cord = y0

    def set_y1cord(self,y1):
        MovingObject.y1cord = y1

    def get_x0cord(self):
        return MovingObject.x0cord

    def get_x1cord(self):
        return MovingObject.x1cord

    def get_y0cord(self):
        return MovingObject.y0cord

    def get_y1cord(self):
        return MovingObject.y1cord

    def set_amount_of_spots(self,value):
        MovingObject.amount_of_spots = value

    def get_amount_of_spots(self):
        return MovingObject.amount_of_spots

    def set_mode_of_working(self, mode):
        MovingObject.mode_of_working = mode

    def get_mode_of_working(self):
        return MovingObject.mode_of_working
    # mouse hover event

class Ui_MainWindow(object):
    def open_new_window(self, image, name):
        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(name)
        self.ui = Ui_AnotherWindow()
        self.ui.setupUi(self.window)
        self.ui.setImage(image)
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
        self.label.setGeometry(QtCore.QRect(630, 10, 681, 31))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
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
        self.tableWidget.setGeometry(QtCore.QRect(450, 70, 841, 551))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(['Photo Width','Photo Height','Net Size','NetCord_X0', 'NetCord_X1','NetCord_Y0','NetCord_Y1','Amount of Spots'])
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
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        self.menuClear = QtWidgets.QMenu(self.menubar)
        self.menuClear.setObjectName("menuClear")
        self.menuSave_as = QtWidgets.QMenu(self.menuFile)
        self.menuSave_as.setObjectName("menuSave_as")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
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
        self.actionAuto_Detection = QtWidgets.QAction(MainWindow)
        self.actionAuto_Detection.setObjectName("actionAuto_Detection")
        self.actionManual_Detection = QtWidgets.QAction(MainWindow)
        self.actionManual_Detection.setObjectName("actionManual_Detection")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionClearR = QtWidgets.QAction(MainWindow)
        self.actionClearR.setObjectName("actionClearR")
        self.menuClear.addAction(self.actionClear)
        self.menuClear.addAction(self.actionClearR)
        self.menuSave_as.addAction(self.actionHTML)
        self.menuSave_as.addAction(self.actionJSON)
        self.menuSave_as.addAction(self.actionMS_Excel)
        self.menuSave_as.addAction(self.actioncsv)
        self.menuSave_as.addAction(self.actionHDF5)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuSave_as.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuMode.addAction(self.actionAuto_Detection)
        self.menuMode.addAction(self.actionManual_Detection)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuClear.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #Listeners
        self.horizontalScrollBar.valueChanged.connect(self.change_size_alpha)
        self.horizontalScrollBar_2.valueChanged.connect(self.change_size_beta)
        self.pushButton.clicked.connect(self.change_alpha_beta_listener)
        self.actionHTML.triggered.connect(lambda: self.save_results("html"))
        self.actioncsv.triggered.connect(lambda: self.save_results("csv"))
        self.actionHDF5.triggered.connect(lambda: self.save_results("hdf5"))
        self.actionJSON.triggered.connect(lambda: self.save_results("json"))
        self.actionMS_Excel.triggered.connect(lambda: self.save_results("excel"))
        self.actionAuto_Detection.triggered.connect(self.auto_detection_mode)
        self.actionManual_Detection.triggered.connect(self.manual_detection_mode)
        self.menuClear.triggered.connect(self.clearing_table)
        self.actionOpen.triggered.connect(self.add_im)
        self.actionClearR.triggered.connect(self.clearRow)

        self.pushButton.setVisible(False)
        self.actionAuto_Detection.setCheckable(True)
        self.actionAuto_Detection.setChecked(True)
        self.horizontalScrollBar.setVisible(False)
        self.horizontalScrollBar_2.setVisible(False)
        self.label_3.setVisible(False)
        self.label_4.setVisible(False)
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.graphicsView.setScene(self.scene)
        start_im = 'Images/NoPhotoAvailable.jpg'
        self.scene.clear()
        self.pixmap = QPixmap(start_im)
        self.scale = 1.5
        size = self.pixmap.size()
        scaled_pixmap = self.pixmap.scaled(self.scale * size)
        self.scene.addPixmap(scaled_pixmap)
        self.view.fitInView(self.scene.sceneRect(),Qt.KeepAspectRatio)
        self.moveObject = MovingObject(150,150,100,100)
        self.nos = NumerationOfSpot(653424)
        self.label.setText("No image uploaded")
        self.label_2.setText("No image uploaded")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GUI wspomagające proces postprocessingu obrazów mikromacierzowych"))
        MainWindow.setStyleSheet(open("QSS/style.qss", "r").read())
        self.label.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Value of Alpha (Contrast)"))
        self.label_4.setText(_translate("MainWindow", "Value of Beta (Brightness)"))
        self.pushButton.setText(_translate("MainWindow","Change"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Blocks on image"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Table with results"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.menuClear.setTitle(_translate("MainWindow", "Table"))
        self.actionClear.setText(_translate("MainWindow", "Clear Table"))
        self.actionClearR.setText(_translate("MainWindow", "Clear Row"))
        self.menuSave_as.setTitle(_translate("MainWindow", "Save results as"))
        self.actionOpen.setText(_translate("MainWindow", "Open Image"))
        self.actionHTML.setText(_translate("MainWindow", "HTML"))
        self.actionJSON.setText(_translate("MainWindow", "JSON"))
        self.actionMS_Excel.setText(_translate("MainWindow", "MS Excel"))
        self.actioncsv.setText(_translate("MainWindow", "CSV"))
        self.actionHDF5.setText(_translate("MainWindow", "HDF5"))
        self.actionAuto_Detection.setText(_translate("MainWindow", "Auto-Detection"))
        self.actionManual_Detection.setText(_translate("MainWindow", "Manual-Detection"))

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseMove:
            aos = self.moveObject.get_amount_of_spots()
        if len(wResultList)>0:
            self.adddatatotable()
        return super(MainWindow, self).eventFilter(source, event)


    def change_size_alpha(self):
        value = self.horizontalScrollBar.value()
        self.label_3.setText('Value of Alpha (Contrast): ' + str(value))

    def change_size_beta(self):
        value = self.horizontalScrollBar_2.value()
        self.label_4.setText('Value of Beta (Brightness): ' + str(value))

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

    def save_results(self, save_as):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        res = QFileDialog.getSaveFileName()
        name_of_file = res[0].split('/')

        df = pd.DataFrame(sResultList, index=list(range(1,len(sResultList)+1)), columns=list(['Photo Width','Photo Height','Net Size','NetCord_X0',
                                                                                'NetCord_X1','NetCord_Y0','NetCord_Y1','Amount of Spots']))
        if save_as == 'html':
            df.to_html(res[0] + '.html')
        elif save_as == "csv":
            df.to_csv(res[0] + '.csv')
        elif save_as == 'hdf5':
            df.to_hdf(res[0] + '.h5', 'df', append=True)
        elif save_as == 'json':
            df.to_json(res[0] + '.json')
        elif save_as == 'excel':
            df.to_excel(res[0] + '.xlsx', sheet_name=str(name_of_file[-1]))
        else:
            print('Nie udalo sie zapisac')

    def opening_im(self):
        # Fix opening  another im
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        image, _ = QFileDialog.getOpenFileName(None, 'Openfile', '', 'im file(*.png *.jpg *.tif)')
        if image:
            global im_size, start_photo, path_of_file, rectangle_size, path_of_file, extension
            rectangle_size = 0

            tif = image.split('/')[-1]
            tif2 = tif.split('.')[-1]

            if tif2 == 'tif':
                image_o = Image.open(image)
                im = np.array(image_o)
                w, h = im.shape
            else:
                im = cv2.imread(image)
                w, h, c = im.shape

            # Skalowanie, ale tworzy sporo problemów

            # self.pixmap2 = QPixmap(image)
            # self.scale = 0.6
            # size = self.pixmap2.size()
            # scaled_pixmap2 = self.pixmap2.scaled(self.scale * size)
            # self.scene.addPixmap(scaled_pixmap2)
            path_of_file = image
            self.scene.addPixmap(QPixmap(image))
            im_size = w, h
            #amount of blocks
            n = 48
            if n >= 3:
                aofir = int(im_size[1] / 4)
                counter = 0
                aofix = im_size[0] / (n/4)
                aofic = 0
                second_spot = True
                first_spot = True
                for i in range(0,n):
                    if n % 3 != 0 and n-i <= 2:
                        if n % 2 == 0:
                            if n % 3 != 1:
                                if n-i == 1:
                                    second_spot = False
                                else:
                                    aofix = im_size[0] - aofic
                            else:
                                if n-i == 2:
                                    first_spot = False
                                else:
                                    aofix = im_size[0] - aofic
                        else:
                            if n % 3 != 1:
                                if n - i == 1:
                                    second_spot = False
                                else:
                                    aofix = im_size[0] - aofic
                            else:
                                if n - i == 2:
                                    first_spot = False
                                else:
                                    aofix = im_size[0] - aofic

                    if counter == 0:
                        if first_spot:
                            moveObject = StaticObject(0,aofic,aofir,aofix,i+1)
                            nos = NumerationOfSpot(i+1)
                            nos.setPos(aofir * 0.4, aofic)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter += 1
                        else:
                            moveObject = StaticObject(0, aofic, 3*aofir, aofix,i+1)
                            nos = NumerationOfSpot(i+1)
                            nos.setPos(aofir * 0.4, aofic)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter += 1
                    elif counter == 1:
                        if second_spot:
                            moveObject = StaticObject(aofir, aofic, aofir, aofix,i+1)
                            nos = NumerationOfSpot(i+1)
                            nos.setPos(aofir*1.4, aofic)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter += 1
                        else:
                            moveObject = StaticObject(aofir, aofic, aofir * 2, aofix,i+1)
                            nos = NumerationOfSpot(i+1)
                            nos.setPos(aofir*1.4, aofic)
                            nos.setPlainText(str(str(i + 1) + '.'))
                            moveObjectList.append(moveObject)
                            textObjectList.append((nos))
                            counter += 1
                    elif counter == 2:
                        moveObject = StaticObject(aofir+aofir, aofic, aofir, aofix,i+1)
                        nos = NumerationOfSpot(i+1)
                        nos.setPos((aofir+aofir)*1.2, aofic)
                        nos.setPlainText(str(str(i + 1) + '.'))
                        moveObjectList.append(moveObject)
                        textObjectList.append((nos))
                        counter += 1
                    elif counter == 3:
                        moveObject = StaticObject(aofir + aofir + aofir, aofic, aofir, aofix,i+1)
                        nos = NumerationOfSpot(i+1)
                        nos.setPos((aofir + aofir + aofir) * 1.115, aofic)
                        nos.setPlainText(str(str(i + 1) + '.'))
                        moveObjectList.append(moveObject)
                        textObjectList.append((nos))
                        counter = 0
                        aofic += aofix

            for x in moveObjectList:
                self.scene.addItem(x)
            for y in textObjectList:
                self.scene.addItem(y)
            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
            rectangle_size = 100
            start_photo = False
            im_name = image.split('/')

            self.horizontalScrollBar.setVisible(True)
            self.horizontalScrollBar_2.setVisible(True)
            self.label_3.setVisible(True)
            self.label_4.setVisible(True)
            self.pushButton.setVisible(True)
            self.label_2.setText('You are currently working on: ' + str(im_name[-1]))
            self.label.setText('You are currently working on: ' + str(im_name[-1]))
            self.horizontalScrollBar.setMinimum(0)
            self.horizontalScrollBar.setMaximum(100)
            self.horizontalScrollBar_2.setMinimum(0)
            self.horizontalScrollBar_2.setMaximum(100)
            self.horizontalScrollBar.setValue(50)
            self.horizontalScrollBar_2.setValue(10)
            self.label_3.setText('Value of Alpha (Contrast): ' + str(self.horizontalScrollBar.value()))
            self.label_4.setText('Value of Beta (Brightness): ' + str(self.horizontalScrollBar_2.value()))

            if self.actionAuto_Detection.isChecked():
                print('auto_detection')
            else: print('manual_detection')
        else:
            start_im = 'Images/NoPhotoAvailable.jpg'
            self.scene.clear()
            self.pixmap = QPixmap(start_im)
            self.scale = 1.5
            size = self.pixmap.size()
            scaled_pixmap = self.pixmap.scaled(self.scale * size)
            self.scene.addPixmap(scaled_pixmap)

    def add_im(self):
        if 'start_photo' in globals() and len(sResultList)>0:
            buttonReply = QMessageBox.question(self, 'Result Data', "Do you want to continue? Unsaved data will be lost",
                                               QMessageBox.Yes | QMessageBox.Cancel)
            if buttonReply == QMessageBox.Yes:
                wResultList.clear()
                self.scene.clear()
                self.opening_im()

            if buttonReply == QMessageBox.Cancel:
                return 0
        else:
            self.scene.clear()
            moveObjectList.clear()
            textObjectList.clear()
            self.opening_im()

    def clearing_table(self):
        self.tableWidget.setRowCount(0)

    def clearRow(self):
        indices = self.tableWidget.selectionModel().selectedRows()
        for index in sorted(indices):
            self.tableWidget.removeRow(index.row())

    def adddatatotable(self):
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        col = 0
        for items in wResultList:
            for i in items:
                cell = QTableWidgetItem(str(i))
                self.tableWidget.setItem(row,col,cell)
                col+=1

        sResultList.extend(wResultList)
        wResultList.clear()

    def auto_detection_mode(self):
        self.actionAuto_Detection.setCheckable(True)
        self.actionAuto_Detection.setChecked(True)
        self.actionManual_Detection.setCheckable(False)
        self.actionManual_Detection.setChecked(False)
        self.pushButton.setVisible(False)
        self.label_5.setText(str(self.moveObject.get_mode_of_working()))
        self.moveObject.set_mode_of_working('AD')

    def manual_detection_mode(self):
        self.actionAuto_Detection.setCheckable(False)
        self.actionAuto_Detection.setChecked(False)
        self.actionManual_Detection.setCheckable(True)
        self.actionManual_Detection.setChecked(True)
        self.pushButton.setVisible(True)
        self.moveObject.set_mode_of_working('MD')
        self.label_5.setText(str(self.moveObject.get_mode_of_working()))

    def adding_data_to_table(self):
        hL = [[im_size[1],im_size[0], self.horizontalScrollBar.value(),self.moveObject.get_y0cord(),self.moveObject.get_y1cord(),
              self.moveObject.get_x0cord(),self.moveObject.get_x1cord(), self.moveObject.get_amount_of_spots()]]
        row = self.tableWidget.rowCount()
        self.tableWidget.setRowCount(row + 1)
        col = 0
        for h in hL:
            for i in h:
                cell = QTableWidgetItem(str(i))
                self.tableWidget.setItem(row, col, cell)
                col += 1

        sResultList.extend(hL)
        wResultList.clear()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.showMaximized()
    sys.exit(app.exec_())
