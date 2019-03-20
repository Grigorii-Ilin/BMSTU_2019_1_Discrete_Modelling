import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,  QPushButton, QLineEdit,  QLabel, QErrorMessage
from PyQt5.QtCore import  QSize
import matplotlib.pyplot as plt
import numpy as np


def show_error_message():
    msg = QErrorMessage()
    msg.showMessage('Неправильно введены значения отрезка!')
    msg.exec_()


def get_x_array(min_val, max_val):
    STEPS_IN_DIAGRAM = 10000
    STEPS_BEFORE_OR_AFTER_INPUTED = 3500

    one_step = (max_val - min_val) / STEPS_IN_DIAGRAM
    start_diagr = min_val - one_step * STEPS_BEFORE_OR_AFTER_INPUTED
    stop_diagr = max_val + one_step * STEPS_BEFORE_OR_AFTER_INPUTED

    return np.arange(start_diagr, stop_diagr, one_step)


class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)      
 
        self.setMinimumSize(QSize(500, 170))    

        self.lbl_input_ravn = QLabel(self)
        self.lbl_input_ravn.setText('Введите начальный (A)      и конечный (B) значения отрезка для равномерного распределения:')
        self.lbl_input_ravn.adjustSize()

        self.lbl_input_exponen = QLabel(self)
        self.lbl_input_exponen.move(0, 15)
        self.lbl_input_exponen.setText('Либо введите значение Лямбда в левое поле для экспоненциального распределения:')
        self.lbl_input_exponen.adjustSize()

        self.le_a_or_lmb = QLineEdit(self)
        self.le_a_or_lmb.move(0, 35)

        self.le_b = QLineEdit(self)
        self.le_b.move(140, 35)
        
        self.btn_ravn = QPushButton('Равномерное', self)
        self.btn_ravn.move(0,80)
        self.btn_ravn.clicked.connect(self.ravn)   
        
       
        self.btn_exponen = QPushButton('Экспоненциальное', self)
        self.btn_exponen.move(0,110)
        self.btn_exponen.clicked.connect(self.exponen)   


        self.lbl_input_exponen = QLabel(self)
        self.lbl_input_exponen.move(120, 140)
        self.lbl_input_exponen.setText('Лабораторная работа № 1. Автор: Г.Б. Ильин, ИУ7-68Б(В)')
        self.lbl_input_exponen.adjustSize()

    def ravn(self):
        def func_ravnomern(x):
            if x <= a:
                return 0
            elif x < b:
                return (x - a) / (b - a)
            else:
                return 1

        def plotn_ravnomern(x):
            if x >= a and x <= b:
                return 1 / (b - a)
            else:
                return 0

        try:
            a = float(self.le_a_or_lmb.text())
            b = float(self.le_b.text())
        except:
            show_error_message()
            return

        figure, diagrams = plt.subplots(2, 1)
        figure.suptitle('Функция и плотность равномерного распределения:')

        x_array = get_x_array(min_val=a, max_val=b)

        y_array = list(map(func_ravnomern, x_array))
        diagrams[0].plot(x_array, y_array) 

        y_array = list(map(plotn_ravnomern, x_array))
        diagrams[1].plot(x_array, y_array) 

        plt.show() 


    def exponen(self):
        def func_exponential(x):
            if x < 0:
                return 0
            else:
                return 1 - np.e ** (-lmb * x)

        def plotn_exponential(x):
            if x < 0:
                return 0
            else:
                return lmb * np.e ** (-lmb * x)

        try:
            lmb = float(self.le_a_or_lmb.text())
        except:
            show_error_message()
            return

        figure, diagrams = plt.subplots(2, 1)
        figure.suptitle('Функция и плотность экспоненциального распределения:')
        
        x_array = get_x_array(min_val=0, max_val=lmb)

        y_array = list(map(func_exponential, x_array))
        diagrams[0].plot(x_array, y_array) 

        y_array = list(map(plotn_exponential, x_array))
        diagrams[1].plot(x_array, y_array) 

        plt.show() 


app = QApplication(sys.argv)
main_window = MyWindow()  
main_window.show()

sys.exit(app.exec_())