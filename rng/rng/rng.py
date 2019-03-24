import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow,  QPushButton,  QLabel, QErrorMessage, QTableWidget,QTableWidgetItem
from PyQt5.QtCore import  QSize

from calc import Calc


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)       

        self.setMinimumSize(QSize(900, 600))    


        self.tbl_rng = QTableWidget(self)

        headers_horiz=[]
        for typ in ('алг.', 'табл.'):
            for i in range(1, 4):
                header=' '.join([typ, str(i), 'цифр.'])
                headers_horiz.append(header)
        headers_horiz.append('случ. 1-999')
        self.tbl_rng.setColumnCount(len(headers_horiz))
        self.tbl_rng.setHorizontalHeaderLabels(headers_horiz)

        headers_vert=[]
        self.ROWS_WITH_NUMBERS_COUNT=10
        for i in range(self.ROWS_WITH_NUMBERS_COUNT):
            headers_vert.append(str(i+1))
        headers_vert.extend(['Частое число', 'Редкое число', 'Размах вариации', 'Дисперсия', 'СКО'])

        self.tbl_rng.setRowCount(len(headers_vert))
        self.tbl_rng.setVerticalHeaderLabels(headers_vert)

        self.tbl_rng.resize(860,400)

        
        self.btn_calc = QPushButton('Посчитать', self)
        self.btn_calc.move(0,400)
        self.btn_calc.clicked.connect(self.calc)   

        
        self.lbl_about = QLabel(self)
        self.lbl_about.move(0, 440)
        self.lbl_about.setText('Лабораторная работа № 2. Автор: Г.Б. Ильин, ИУ7-68Б(В)')
        self.lbl_about.adjustSize()


    @staticmethod
    def show_error_message():
        msg = QErrorMessage()
        msg.showMessage('Неправильно введены случайные числа!')
        msg.exec_()

    def show_final_result(self, col, row, value):        
        value=str(value)
        self.tbl_rng.setItem(row,col, QTableWidgetItem(value))
        row+=1
        return row


    def calc(self):
        entered_numbers=[]
        for row in range(self.ROWS_WITH_NUMBERS_COUNT):
            try:
                tmp=int(self.tbl_rng.item(row, 6).text())
                tmp=abs(tmp)
                entered_numbers.append(tmp)
            except:
                self.show_error_message()
                return

        calc=Calc(entered_numbers)
        calc.work()

        for row in range(self.ROWS_WITH_NUMBERS_COUNT):
            for col in range(3):
                rng=str(calc.rngs[col][row*100])
                self.tbl_rng.setItem(row,col, QTableWidgetItem(rng))

            for col in range(3,6):
                seed=entered_numbers[row]
                rng=str(calc.rngs[col][seed])
                self.tbl_rng.setItem(row,col, QTableWidgetItem(rng))

        for col in range(7):
            row=self.show_final_result(col,
                                    self.ROWS_WITH_NUMBERS_COUNT,
                                    calc.result[col]['max_val']['digit'])

            row=self.show_final_result(col,
                                    row,
                                    calc.result[col]['min_val']['digit'])

            row=self.show_final_result(col,
                                    row,
                                    calc.result[col]['scope_of_variation'])

            row=self.show_final_result(col,
                                    row,
                                    calc.result[col]['dispersion'])

            row=self.show_final_result(col,
                                    row,
                                    calc.result[col]['stddev'])


app = QApplication(sys.argv)
main_window = MyWindow()  
main_window.show()

fin=app.exec_()


