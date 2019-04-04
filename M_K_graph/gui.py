import sys

from PyQt5.QtWidgets import QApplication, QMainWindow,  QPushButton,  QLabel, QErrorMessage, QTableWidget,QTableWidgetItem
from PyQt5.QtCore import  QSize

from M_K_graph import calc


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)       
        self.setMinimumSize(QSize(640, 300))   

        self.MATRIX_DIMENSION = 4
       
        self.create_table()
        self.create_main_button()
        self.create_about()


    def create_table(self):
        self.tbl_rng = QTableWidget(self)
        headers_horiz = [str(i + 1) for i in range(self.MATRIX_DIMENSION)]
        headers_horiz.append('Ср. вр. пребыв.')
        self.tbl_rng.setColumnCount(len(headers_horiz))
        self.tbl_rng.setHorizontalHeaderLabels(headers_horiz)

        headers_vert = [str(i + 1) for i in range(self.MATRIX_DIMENSION)]
        self.tbl_rng.setRowCount(len(headers_vert))
        self.tbl_rng.setVerticalHeaderLabels(headers_vert)

        self.tbl_rng.resize(560,200)


    def create_main_button(self):
        self.btn_calc = QPushButton('Посчитать', self)
        self.btn_calc.move(0,210)
        self.btn_calc.clicked.connect(self.calc)  


    def create_about(self):
        self.lbl_about = QLabel(self)
        self.lbl_about.move(0, 250)
        self.lbl_about.setText('Лабораторная работа № 3. Автор: Г.Б. Ильин, ИУ7-68Б(В)')
        self.lbl_about.adjustSize()


    @staticmethod
    def show_error_message():
        msg = QErrorMessage()
        msg.showMessage('Неправильно введены числа!')
        msg.exec_()


    def show_final_result(self, col, row, value):        
        value = str(value)
        self.tbl_rng.setItem(row,col, QTableWidgetItem(value))
        row+=1
        return row


    def calc(self):
        entered_numbers = [[] for i in range(self.MATRIX_DIMENSION)]
        for row in range(self.MATRIX_DIMENSION):
            for col in range(self.MATRIX_DIMENSION):
                try:
                    cell_value = self.tbl_rng.item(row, col)
                    tmp = float(cell_value.text()) if cell_value else 0.0
<<<<<<< HEAD
                    assert(tmp >= 0.0)
=======
                    assert(tmp >= 0.0 and tmp <= 1.0)
>>>>>>> d3b7c0f37353f0e3d489d25f41af6fac0183cc6a
                    entered_numbers[row].append(tmp)
                except:
                    self.show_error_message()
                    return

        mean_time_probability = calc(entered_numbers)

        for row  in range(self.MATRIX_DIMENSION):
<<<<<<< HEAD
            value = str(round(mean_time_probability[row], 3))
=======
            value= str(round(mean_time_probability[row], 3))
>>>>>>> d3b7c0f37353f0e3d489d25f41af6fac0183cc6a
            self.tbl_rng.setItem(row,4, QTableWidgetItem(value))


app = QApplication(sys.argv)
main_window = MyWindow()  
main_window.show()

fin = app.exec_()


