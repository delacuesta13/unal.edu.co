# -*- coding: iso-8859-1 -*-

import random, datetime

class SandPile(object):
    def __init__(self):
        self.matriz = []
        self. grilla = 400 # número de filas y columnas
        self.colores_rgb = ('255 255 255', # blanco
                            '255 255 0', # amarillo
                            '255 165 0', # naranja
                            '255 0 0', # rojo
                            '0 255 0', # verde
                            '0 255 255', # cyan
                            '0 0 255', # azul
                            '0 0 0' # negro
                            )
        self.limite = 4 # número máximo de granos en una celda
        self.total_iteraciones = 0
        self.poblar_matriz()
        self.agregar_granos_iniciales()
        self.generar_sandpile()
        self.dibujar_sandpile()
    
    def poblar_matriz(self):
        for i in xrange(self.grilla):
            fila = []
            for j in xrange(self.grilla):
                granos_arena = int(random.randint(0, len(self.colores_rgb)-1))
                fila.append(granos_arena)
            self.matriz.append(fila)
            
    def agregar_granos_iniciales(self):
        i = int(random.randint(0, self.grilla - 1))
        j = int(random.randint(0, self.grilla - 1))
        self.matriz[i][j]= len(self.colores_rgb) - 1
            
    def generar_sandpile(self):
        inestable = True
        while inestable:
            i = 0
            if self.total_iteraciones % 500 == 0:
                self.dibujar_sandpile()
            self.total_iteraciones += 1
            inestable = False
            while i < self.grilla:
                j = 0
                while j < self.grilla:
                    if self.matriz[i][j] > 3:
                        inestable = True
                        self.matriz[i][j] -= 4
                        self.compartir_granos(i, j)
                    j += 1
                i += 1
        self.dibujar_sandpile()
            
    def compartir_granos(self, fil, col):
        fil_ant, fil_sig = fil - 1, fil + 1
        col_ant, col_sig = col - 1, col + 1
        # celda de arriba
        if fil_ant >= 0:
            self.matriz[fil_ant][col] += 1
        # celda superior
        if fil_sig <= self.grilla - 1:
            self.matriz[fil_sig][col] += 1
        # celda a la izquierda
        if col_ant >= 0:
            self.matriz[fil][col_ant] += 1
        # celda a la derecha
        if col_sig <= self.grilla - 1:
            self.matriz[fil][col_sig] += 1
        
    def dibujar_sandpile(self):
        s = 'P3\n{0} {0}\n255\n'.format(self.grilla)
        for i in xrange(self.grilla):
            linea = ''
            for j in xrange(self.grilla):
                linea += self.colores_rgb[self.matriz[i][j]] + (' ' * 3)
            s += linea.rstrip() + ('\n' if i < self.grilla - 1 else '')
        tiempo = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
        n_archivo = 'img/{1}/sandpile_i{0}_{2}.ppm'.format(str(self.total_iteraciones), str(self.grilla), tiempo)
        sandpile = open(n_archivo, 'w+')
        sandpile.write(s)
        sandpile.flush()

if __name__ == '__main__':
    SandPile()
