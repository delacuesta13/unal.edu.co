# -*- coding: iso-8859-1 -*-

"""
Implementación de un autómata celular elemental de una dimensión.

Referencias:
[1] http://www-inst.eecs.berkeley.edu/~selfpace/cs9honline/P1/
[2] http://atlas.wolfram.com/01/01/ (lista de autómatas)
"""

import datetime, math, random, sys

class AutomataCelular1D(object):
    def __init__(self, regla, iteraciones, inicio_aleatorio=False):
        self.regla = regla
        self.iteraciones = iteraciones
        self.inicio_aleatorio = inicio_aleatorio
        self.regla_interpretada = {}
        self.automata_celular = []
        
        self.interpretar_regla()
        self.iterar_automata()
        
    def interpretar_regla(self):
        sum_binario = 0
        for i in xrange(7,-1,-1):
            self.regla_interpretada[i] = ["{0:b}".format(i).zfill(3)]
            dos_i = int(math.pow(2, i))
            if dos_i <= self.regla and sum_binario + dos_i <= self.regla:
                sum_binario += dos_i
                self.regla_interpretada[i].append('1')
            else:
                self.regla_interpretada[i].append('0')
    
    def iterar_automata(self):
        if not self.inicio_aleatorio:
            self.automata_celular.append(['0']*self.iteraciones + ['1'] + ['0']*self.iteraciones)
        else:
            self.automata_celular.append([str(random.randint(0,1)) for i in xrange((self.iteraciones * 2) + 1)])
        for i in xrange(1, self.iteraciones + 1):
            ultima_fila = self.automata_celular[i - 1]
            nueva_fila = []
            for j in xrange(len(ultima_fila)):
                if j == 0:
                    temp_automata = ['0'] + ultima_fila[0:2]
                elif j == (len(ultima_fila) - 1):
                    ind_inf = len(ultima_fila) - 2
                    temp_automata = ultima_fila[ind_inf:]  + ['0']
                else:
                    ind_inf = j - 1
                    ind_sup = ind_inf + 3                
                    temp_automata = ultima_fila[ind_inf:ind_sup]
                nueva_fila.append(self.aplicar_regla(temp_automata))
            self.automata_celular.append(nueva_fila)
    
    def aplicar_regla(self, parte_automata):
        traduccion = ''
        for regla in sorted(self.regla_interpretada.iterkeys(), reverse=True):
            if list(self.regla_interpretada[regla][0]) == parte_automata:
                traduccion = self.regla_interpretada[regla][1]
                break
        else:
            traduccion = 0
        return traduccion
        
    def dibujar_automata(self):
        s = ''
        for i in xrange(len(self.automata_celular)):
            linea = ''
            for j in xrange(len(self.automata_celular[i])):
                if i == 0 and j == 0:
                    s += 'P1 {} {}\n'.format(len(self.automata_celular[i]), len(self.automata_celular))
                linea += self.automata_celular[i][j] + ' '
            s += linea.rstrip() + ('\n' if i < len(self.automata_celular) - 1 else '')
        return s

def main():
    iteraciones = 1000
    if len(sys.argv) == 3:
        try:
            iteraciones = int(sys.argv[2])
        except:
            pass                        
    ac_1d = AutomataCelular1D(int(sys.argv[1]), iteraciones, True)
    tiempo = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
    pbm = open("img/r{}_{}.pbm".format(sys.argv[1], tiempo), 'w+')
    pbm.write(ac_1d.dibujar_automata())
    pbm.flush()

if __name__ == '__main__':
    main()
