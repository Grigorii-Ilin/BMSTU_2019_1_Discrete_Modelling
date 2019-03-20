import sys

import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow,  QPushButton,  QLabel, QErrorMessage, QTableWidget,QTableWidgetItem
from PyQt5.QtCore import  QSize


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)      
 
        self.setMinimumSize(QSize(800, 600))    

        self.ROWS_COUNT=10

        headers=[]
        for typ in ('алг.', 'табл.'):
            for i in range(1, 4):
                header=' '.join([typ, str(i), 'цифр.'])
                headers.append(header)
        headers.append('случ. 1-999')

        self.tbl_rng = QTableWidget(self)
        self.tbl_rng.setColumnCount(len(headers))
        self.tbl_rng.setHorizontalHeaderLabels(headers)
        self.tbl_rng.resize(760,400)
        self.tbl_rng.setRowCount(self.ROWS_COUNT)
        
        self.btn_calc = QPushButton('Посчитать', self)
        self.btn_calc.move(0,400)
        self.btn_calc.clicked.connect(self.calc)   
        
        self.lbl_input_exponen = QLabel(self)
        self.lbl_input_exponen.move(0, 440)
        self.lbl_input_exponen.setText('Лабораторная работа № 2. Автор: Г.Б. Ильин, ИУ7-68Б(В)')
        self.lbl_input_exponen.adjustSize()

    @staticmethod
    def show_error_message():
        msg = QErrorMessage()
        msg.showMessage('Неправильно введены случайные числа!')
        msg.exec_()

    @staticmethod
    def lehmer(seed):
        A = 16807 #one of Lehmer's counts
        M = 2147483647 #max int32

        result=A * seed / M
        return result

    @staticmethod
    def get_rng(lehmer_str, numeral_count):
        BAD_SYMBOLS= ['.', ',', '-', 'e'] 

        rng=''
        while len(rng)<numeral_count:
            cur_char=lehmer_str[0]
            next_char=lehmer_str[1]
            lehmer_str=lehmer_str[1:]

            if cur_char in BAD_SYMBOLS or next_char in BAD_SYMBOLS:
                continue

            if rng=='' and cur_char=='0':
                continue

            if numeral_count==1 and next_char=='0':
                cur_char='0'

            rng+=cur_char

        return lehmer_str, rng

    def calc(self):
        df=pd.read_excel('table.xlsx')

        for row in range(self.ROWS_COUNT):
            try:
                seed=int(self.tbl_rng.item(row, 6).text())
                assert(seed>=1 and seed<=999)
            except:
                self.show_error_message()
                return

            lehmer_str=str(self.lehmer(seed))
            lehmer_str=lehmer_str[::-1]
            for col in range(3):
                lehmer_str, rng=self.get_rng(lehmer_str, col+1)
                self.tbl_rng.setItem(row,col, QTableWidgetItem(rng))

            for col in range(3):
                rng=str(df.iat[seed, col])
                self.tbl_rng.setItem(row,col+3, QTableWidgetItem(rng))


app = QApplication(sys.argv)
main_window = MyWindow()  
main_window.show()

sys.exit(app.exec_())




