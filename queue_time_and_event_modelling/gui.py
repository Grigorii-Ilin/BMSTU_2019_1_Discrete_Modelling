import sys
import functools
import itertools

from PyQt5.QtWidgets import QApplication, QMainWindow,  QPushButton,  QLabel, QErrorMessage, QMessageBox, QTableWidget#,QTableWidgetItem
from PyQt5.QtCore import  QSize
import matplotlib.pyplot as plt

#from pprint import pprint
import delta_time_modelling
import events_modelling

class MyWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)       
        self.setMinimumSize(QSize(640, 300))   

        self.create_table()
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
        #m_dt=model_result['delta_time']['memory_blocks_max']
        #m_e=model_result['events']['memory_blocks_max']

        msg = QMessageBox(
            QMessageBox.Information,
            'Успех!',
            'Максимальный объем памяти: \nв Δt алгоритме: {0:d}, \nв событийном алгоритме: {1:d}.'.format(m_dt, m_e), 
            QMessageBox.Ok)
        msg.exec_() 
    
    @staticmethod
    def show_diagrams(model_result):

        #def one_diag(index, title, model_result_current):
        #    diagrams[index].set_title(title)
        #    diagrams[index].plot(model_result_current['times'], model_result_current['memory_blocks_count']) 

        figure, diagrams = plt.subplots(2, 1)
        figure.suptitle('Использование памяти в Δt алгоритме и событийном алгоритме')

        #index_increment = functools.partial(next, itertools.count())
        #one_diag(index_increment(), 'Δt алгоритм', model_result['delta_time'])
        #one_diag(index_increment(), '\nСобытийный алгоритм', model_result['events'])
        
        #diag_indexes=range(0,2)
        #diag_titles=['Δt алгоритм', 'Событийный алгоритм']
        #model_result_keys=['delta_time', 'events']
        #for diag_index, diag_title, model_result_key in zip(diag_indexes, diag_titles, model_result_keys):
        #    pass

        #diagrams[0].set_title('Δt алгоритм')
        diagrams[0].plot(model_result['delta_time']['times'], model_result['delta_time']['memory_blocks_count']) 
        
        #diagrams[1].set_title('Событийный алгоритм')
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


        #"""
        #t = times, 
        #q = memory_blocks_count, 
        #m = memory_blocks_max
        #_dt = delta_time_modelling
        #_e = events_modelling
        #"""
        #t_dt, q_dt, m_dt=delta_time_modelling.model(a,
        #                                            b,
        #                                            lmbd,
        #                                            dt,
        #                                            t_end,
        #                                            reentry_prob)

        #t_e, q_e, m_e=delta_time_modelling.model(a,
        #                                        b,
        #                                        lmbd,
        #                                        dt,
        #                                        t_end,
        #                                        reentry_prob)

#t, q, m = delta_time_modelling.model(2, 5, 1.0, 1.0, 200.0, 0.8)
#pprint(t, compact=True)
#pprint(q, compact=True)
#print(m)

#t, q, m = events_modelling.model(2, 5, 1.0, 1.0, 200.0, 0.8)
#pprint(t, compact=True)
#pprint(q, compact=True)
#print(m)
app = QApplication(sys.argv)
main_window = MyWindow()  
main_window.show()
fin = app.exec_()
print(fin)