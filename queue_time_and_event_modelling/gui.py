import sys
import functools
import itertools

from PyQt5.QtWidgets import QApplication, QMainWindow,  QPushButton,  QLabel, QErrorMessage, QMessageBox, QTableWidget
from PyQt5.QtCore import  QSize
from PyQt5.QtGui import QPixmap

import matplotlib.pyplot as plt

import delta_time_modelling
import events_modelling

class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)       
        self.setMinimumSize(QSize(800, 300))   

        self.create_table()
        self.create_image()
        self.create_main_button()
        self.create_about()


    def create_table(self):
        self.tbl_input = QTableWidget(self)
        
        headers_horiz = ['Ввод']
        self.tbl_input.setColumnCount(len(headers_horiz))
        self.tbl_input.setHorizontalHeaderLabels(headers_horiz)

        headers_vert = ['A', 'B', 'λ', 'Δt', 'T конечное', 'Вер-ть повтора']
        self.tbl_input.setRowCount(len(headers_vert))
        self.tbl_input.setVerticalHeaderLabels(headers_vert)

        self.tbl_input.resize(220,210)


    def create_image(self):
        self.lbl_scheme_image = QLabel(self)
        pixmap=QPixmap('scheme.png')
        self.lbl_scheme_image.setPixmap(pixmap)
        self.lbl_scheme_image.move(225, 0)
        self.lbl_scheme_image.resize(pixmap.width(), pixmap.height())


    def create_main_button(self):
        self.btn_calc = QPushButton('Посчитать', self)
        self.btn_calc.move(0,215)
        self.btn_calc.clicked.connect(self.calc)  


    def create_about(self):
        self.lbl_about = QLabel(self)
        self.lbl_about.move(0, 250)
        self.lbl_about.setText('Лабораторная работа № 4. Автор: Г.Б. Ильин, ИУ7-68Б(В)')
        self.lbl_about.adjustSize()


    @staticmethod
    def show_error_message():
        msg = QErrorMessage()
        msg.showMessage('Неправильно введены числа!')
        msg.exec_()

    
    @staticmethod
    def show_max_memory_size(m_dt, m_e):
        msg = QMessageBox(
            QMessageBox.Information,
            'Успех!',
            'Максимальный объем памяти: \nв Δt алгоритме: {0:d}, \nв событийном алгоритме: {1:d}.'.format(m_dt, m_e), 
            QMessageBox.Ok)
        msg.exec_() 
 
        
    @staticmethod
    def show_diagrams(model_result):
        figure, diagrams = plt.subplots(2, 1)
        figure.suptitle('Использование памяти в Δt алгоритме и событийном алгоритме')

        diagrams[0].plot(model_result['delta_time']['times'], model_result['delta_time']['memory_blocks_count']) 
        diagrams[1].plot(model_result['events']['times'], model_result['events']['memory_blocks_count']) 

        plt.show() 


    def read_cell(self, row, left_border=0.0, right_border=sys.float_info.max):
        cell_item = self.tbl_input.item(row, 0)
        result = float(cell_item.text()) if cell_item else 0.0
        assert(result >= left_border and result <= right_border)
        return result


    def calc(self):
        try:
            MAX_DT_PER_TIME = 10000
            row_increment = functools.partial(next, itertools.count())

            a = self.read_cell(row_increment())
            b = self.read_cell(row_increment(), a)
            lmbd = self.read_cell(row_increment())
            dt = self.read_cell(row_increment(), 0.0001, sys.float_info.max / MAX_DT_PER_TIME)
            t_end = self.read_cell(row_increment(), dt, dt * MAX_DT_PER_TIME)
            reentry_prob = self.read_cell(row_increment(), 0.0, 1.0)
        except :
            self.show_error_message()
            return

        model_result={}
        model_result['delta_time']=delta_time_modelling.model(a, b, lmbd, dt, t_end, reentry_prob)
        model_result['events']=events_modelling.model(a, b, lmbd, dt, t_end, reentry_prob)

        self.show_max_memory_size(model_result['delta_time']['memory_blocks_max'], model_result['events']['memory_blocks_max'])
        self.show_diagrams(model_result)


app = QApplication(sys.argv)
main_window = MyWindow()  
main_window.show()
app.exec_()
