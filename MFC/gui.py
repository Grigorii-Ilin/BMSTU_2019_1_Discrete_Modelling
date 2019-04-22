import sys

from PyQt5.QtWidgets import QApplication, QMainWindow,  QPushButton,  QLabel,   QTableWidget, QTableWidgetItem
from PyQt5.QtCore import  QSize

import mfc


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)       
        self.setMinimumSize(QSize(400, 300))   

        self.create_table()
        self.create_main_button()
        self.create_about()


    def create_table(self):
        self.tbl_result = QTableWidget(self)
        
        headers_horiz = ['Результат']
        self.tbl_result.setColumnCount(len(headers_horiz))
        self.tbl_result.setHorizontalHeaderLabels(headers_horiz)

        headers_vert = ['Кол-во посетителей', 
                        'Из них не обслужено',
                       'Вероятность отказа', 
                       'Ti спец. 1', 
                       'Ti спец. 2', 
                       'Ti спец. 3',
                       'Ti комп. 1',
                       'Ti комп. 2']
        self.tbl_result.setRowCount(len(headers_vert))
        self.tbl_result.setVerticalHeaderLabels(headers_vert)

        self.tbl_result.resize(280,210)


    def create_main_button(self):
        self.btn_calc = QPushButton('Посчитать', self)
        self.btn_calc.move(0,215)
        self.btn_calc.clicked.connect(self.calc)  


    def create_about(self):
        self.lbl_about = QLabel(self)
        self.lbl_about.move(0, 250)
        self.lbl_about.setText('Лабораторная работа № 5. Автор: Г.Б. Ильин, ИУ7-68Б(В)')
        self.lbl_about.adjustSize()


    def calc(self):
        result = mfc.calc()

        for i in range(3):
            t = str(result['ppl'][i])
            self.tbl_result.setItem(i-1,1, QTableWidgetItem(t))

        for i in range(3):
            t = str(result['spec'][i])
            self.tbl_result.setItem(i+2,1, QTableWidgetItem(t))

        for i in range(2):
            t = str(result['cpu'][i])
            self.tbl_result.setItem(i+5,1, QTableWidgetItem(t))


app = QApplication(sys.argv)
main_window = MyWindow()  
main_window.show()
app.exec_()

