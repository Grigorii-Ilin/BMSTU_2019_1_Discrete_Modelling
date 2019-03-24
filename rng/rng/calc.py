from collections import Counter

import pandas as pd


class Calc(object):
    def __init__(self, entered_numbers):
        self.rngs = [[] for _ in range(7)] 
        self.rngs[6] = entered_numbers

        self.counter_holder=[Counter() for _ in range(7)]
        for col in range(7):
            for digit in range(10):
                self.counter_holder[col][str(digit)]=0 

        tmp_calculated = ('max_val', 'min_val', 'scope_of_variation', 'dispersion','stddev')
        self.result = [{k:{} for k in tmp_calculated} for _ in range(7)]


    def work(self):
        self.load_table()
        self.calc_rng()
        self.max_counts()
        self.calc_variations()


    def load_table(self):
        dfExcel = pd.read_excel('table.xlsx')
        self.rngs[3] = dfExcel['one'].tolist()
        self.rngs[4] = dfExcel['two'].tolist()
        self.rngs[5] = dfExcel['three'].tolist()


    @staticmethod
    def _lehmer(seed):
        A = 16807 #one of Lehmer's counts
        M = 2147483647 #max int32

        result = A * seed / M
        return result


    @staticmethod
    def _get_rng(lehmer_str, numeral_count):
        BAD_SYMBOLS = ['.', ',', '-', 'e'] 

        rng = ''
        while len(rng) < numeral_count:
            cur_char = lehmer_str[0]
            next_char = lehmer_str[1]
            lehmer_str = lehmer_str[1:]

            if cur_char in BAD_SYMBOLS or next_char in BAD_SYMBOLS:
                continue

            if rng == '' and cur_char == '0':
                continue

            if numeral_count == 1 and next_char == '0':
                cur_char = '0'

            rng+=cur_char

        return lehmer_str, int(rng)


    def calc_rng(self):
        for col in reversed(range(3)): # for 1 2 and 3 digits in number
            for row in range(1000):
                residual = row % 100

                if residual == 0:
                    index = row // 100
                    seed = self.rngs[6][index]
                    seed = int(str(seed)[:3]) 
                else:
                    seed = self.rngs[2][row - 1]

                lehmer_str = str(self._lehmer(seed))
                lehmer_str = lehmer_str[::-1]
            
                lehmer_str, rng = self._get_rng(lehmer_str, col + 1)
                self.rngs[col].append(rng)

    def max_counts(self):
        

        for col in range(7):
            c=self.counter_holder[col]

            for number in self.rngs[col]:
                for ch in str(number):
                    c[ch]+=1

            for key, fn in zip(['max_val', 'min_val'], [max, min]):
                digit, count = fn(c.items(), key=lambda x: x[1])

                d = self.result[col][key]
                d['digit'] = digit
                d['count'] = count


    def calc_variations(self):
        for col in range(7):
            d=self.result[col]
            c=self.counter_holder[col]
            r=self.rngs[col]
            d['scope_of_variation']=d['max_val']['count']-d['min_val']['count']

            mean=sum(c.values())/len(r)

            sqr_i_minus_mean=[]
            for row in range(len(r)):
                tmp=(r[row]-mean)**2
                sqr_i_minus_mean.append(tmp)

            d['dispersion']=sum(sqr_i_minus_mean)/len(sqr_i_minus_mean)

            d['stddev']=d['dispersion']**0.5


