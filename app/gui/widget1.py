import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QDialog
from PyQt5.QtGui import QPainter, QColor,QPen
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtCore import *
import math
import  numpy as np
import traceback
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from app import reshape_ordered_state as ros
from app import serial_to_arduino as sta
from app import algorism
from app import alogorism1
import threading

#0 1 2 3 4 5 6 7 8

#4 2 1 0 3 5 6 7 8


global_idx = 1

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.block_positions = []
        self.positions = []
        self.local_event_loop = QEventLoop()
        self.timer = QTimer(self)
        self.warning()
        self.initUI()

    def set_xy_num(self,x_num,y_num):
        self.x_num = x_num
        self.y_num = y_num

    def set_block_num(self,block_num):
        self.block_num = block_num

    def set_puzzle_x_interval(self,puzzle_x_size,puzzle_x_num):
        # set x interval
        interval = puzzle_x_size // (puzzle_x_num+1)
        return interval

    def set_puzzle_y_interval(self,puzzle_y_size,puzzle_y_num):
        # set y interval
        interval = puzzle_y_size // (puzzle_y_num+1)
        return interval

    def warning(self):
        # warning message
        self.warning =QDialog()
        warning = QLabel('It\'s impossible',  self.warning)
        # show warnning message
        btnDialog = QPushButton("OK",  self.warning)
        btnDialog.clicked.connect(self.dialog_close)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(warning)
        hbox.addWidget(btnDialog)
        hbox.addStretch(1)
        self.warning.setLayout(hbox)
        self.warning.setWindowTitle('Warning')
        self.warning.setWindowModality(Qt.ApplicationModal)
        self.warning.resize(200, 100)

    def dialog_open(self):
        # warning message open
        self.warning.show()

    def dialog_close(self):
        # warning message close
        self.warning.close()


    def initUI(self):
        self.setWindowTitle('sliding_puzzle')
        self.setGeometry(300, 100, 1000, 800)
        self.show()

        self.main_widget = QWidget()

        self.puzzle = QWidget()
        self.puzzle.setStyleSheet("background-color:white")
        puzzle_x_size = 600
        puzzle_y_size = 600
        self.puzzle.setFixedSize(600, 600)

        self.puzzle_pieces = []

        self.set_block_num(9)

        contents = self.block_num
        # set number of block

        self.set_xy_num(3,3)

        puzzle_x_num =self.x_num
        puzzle_y_num =self.y_num

        interval_x = self.set_puzzle_x_interval(puzzle_x_size,puzzle_x_num)
        interval_y = self.set_puzzle_y_interval(puzzle_y_size,puzzle_y_num)

        # set blocks
        for i in range(0,contents):
            weight = 50
            if i == 0:
                self.puzzle_pieces.append(QLabel('', self.puzzle))
                self.puzzle_pieces[0].setStyleSheet("background-color:white;border-radius:15px ;")
                self.puzzle_pieces[0].setFixedSize(100, 100)
                self.puzzle_pieces[0].move( (i+1)*interval_y-weight,puzzle_y_num*interval_y-weight)
                self.positions.append([(i+1)*interval_y-weight,puzzle_y_num*interval_y-weight])

            else :
                row = puzzle_y_num - (i // puzzle_y_num)
                col = i - (i//puzzle_x_num)*puzzle_x_num+1
                self.puzzle_pieces.append(QLabel(str(i), self.puzzle))

                font=self.puzzle_pieces[i].font()
                font.setFamily('Times New Roman')
                font.setPointSizeF(20)
                font.setBold(True)

                self.puzzle_pieces[i].setFont(font)
                self.puzzle_pieces[i].setAlignment(Qt.AlignCenter)
                self.puzzle_pieces[i].setStyleSheet("background-color:red;border-radius:15px;")
                self.puzzle_pieces[i].setFixedSize(100, 100)
                self.puzzle_pieces[i].move(col * interval_x-weight,row * interval_y-weight,)
                self.positions.append([col * interval_x-weight,row * interval_y-weight,])

        self.block_positions = [ i  for i in range(len(self.puzzle_pieces))]

        input = QLineEdit()
        putIn = QPushButton('put in')
        putOut = QPushButton('put out')
        intialize= QPushButton('intialize')
        nobody = QPushButton('')
        reshape = QPushButton('reshape')

        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        vbox = QVBoxLayout()

        hbox1.addStretch(1)
        hbox1.addWidget(self.puzzle)
        hbox1.addStretch(1)

        hbox2.addStretch(1)
        hbox2.addWidget(input)
        hbox2.addStretch(1)


        hbox3.addStretch(1)
        hbox3.addWidget(putIn)
        hbox3.addWidget(putOut)
        hbox3.addWidget(reshape)
        hbox3.addWidget(intialize)
        hbox3.addStretch(1)

        vbox.addStretch(3)
        vbox.addLayout(hbox1)
        vbox.addStretch(1)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        vbox.addLayout(hbox3)
        vbox.addStretch(5)

        self.main_widget.setLayout(vbox)
        self.setCentralWidget(self.main_widget)

        # add animey Properties to Each Block
        self.puzzle_pieces_anim = [QPropertyAnimation(self.puzzle_pieces[i], b"pos") for i in
                                   range(len(self.puzzle_pieces))]

        reshape.clicked.connect(lambda: self.reshape_puzzle(input.text()))
        # Forward the entire matrix

        putOut.clicked.connect(lambda: self.put_out(input.text()))
        # Forward the target block

        intialize.clicked.connect(lambda: self.initialize())
        # back to the initial position


    def get_pres_shape(self):
        # get initial postions of blocks
        init_shape = ''
        pres_position = [ [puzzle_piece.pos().x(),puzzle_piece.pos().y()] for puzzle_piece in self.puzzle_pieces]
        pres_shape = [pres_position.index(position) for position in self.positions]

        j = 0
        for i in range(len(pres_shape)*2-1) :
            if i%2 == 0:
                init_shape +=str(pres_shape[j])
                j +=1
            else:
                init_shape += ' '
        #print(init_shape)
        return init_shape

    def input2order(self,input):
        # convert input from gui to input for solver
        order = ''
        times = len(input)/self.x_num
        input=input.split(' ')
        input = np.array(input)
        input=input.reshape(self.x_num,-1)
        input = np.flip(input,axis=0)
        input = input.flatten()
        result =''
        j =0
        for i in range(len(input)*2-1) :
            if i%2 == 0:
                result +=str(input[j])
                j +=1
            else:
                result += ' '
        return result

    def make_order(self,goal_shape): # for reshape, initialize
        init_shape = self.input2order(self.get_pres_shape())
        goal_shape = self.input2order(goal_shape)
        result = ros.get_order(init_shape, goal_shape) # make the command
        print(sta.push_orders(result)) # passing the command to master aduino
        orders = [ order[1] for order in result] # make the command for gui
        return orders

    def make_order_1(self,goal_shape): # for put in
        init_shape = self.input2order(self.get_pres_shape())
        goal_shape = self.input2order(goal_shape)
        result  = ros.get_order_1(init_shape, goal_shape) # make the command
        print(sta.push_orders(result)) # passing the command to master aduino
        orders = [order[1] for order in result] # make the command for gui
        return orders

    def reshape_puzzle(self, goal_shape):
        try:
            if len(goal_shape)!=17:
                raise Exception
            try:
                orders = self.make_order(goal_shape)
            except:
                raise Exception
        except :
            err_msg = traceback.format_exc() # print error message
            print(err_msg)
            self.dialog_open()
        else:
            for order in orders:
                # one by one method call in 3 seconds
                # start event loop
                self.timer.singleShot(300, lambda: self.one_by_one(order))
                # wait until evect loop ends
                self.local_event_loop.exec()

    def initialize(self):
        try:

            try:
                orders = self.make_order('0 1 2 3 4 5 6 7 8')
            except:
                raise Exception
        except :
            err_msg = traceback.format_exc() # print error message
            print(err_msg)
            self.dialog_open()
        else:
            for order in orders:
                # one by one method call in 3 seconds
                # start event loop
                self.timer.singleShot(300, lambda: self.one_by_one(order))
                # wait until evect loop ends
                self.local_event_loop.exec()

    def put_out(self, target_block):
        goal_shape = target_block + ' 0 0 0 0 0 0 0 0'
        try:
            if len(goal_shape)!=17:
                raise Exception
            try:
                orders = self.make_order_1(goal_shape)
            except:
                raise Exception
        except :
            err_msg = traceback.format_exc() # print error message
            print(err_msg)
            self.dialog_open()
        else:
            for order in orders:
                # one by one method call in 3 seconds
                # start event loop
                self.timer.singleShot(300, lambda: self.one_by_one(order))
                # wait until evect loop ends
                self.local_event_loop.exec()


    def one_by_one(self,i):
        i = int(i)

        blank_x = self.puzzle_pieces[0].pos().x()
        blank_y = self.puzzle_pieces[0].pos().y()

        block_x = self.puzzle_pieces[i].pos().x()
        block_y = self.puzzle_pieces[i].pos().y()

        self.puzzle_pieces_anim[i].setStartValue(QPoint(block_x, block_y))
        self.puzzle_pieces_anim[i].setEndValue(QPoint(blank_x, blank_y))
        self.puzzle_pieces_anim[i].setDuration(200)
        self.puzzle_pieces_anim[i].start() # move block

        self.puzzle_pieces[0].move(block_x, block_y)
        # exit event loop
        self.local_event_loop.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())