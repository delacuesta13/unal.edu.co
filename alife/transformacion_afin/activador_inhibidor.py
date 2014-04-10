# -*- coding: iso-8859-1 -*-

"""
Implementación de un sistema activador e inhibidor a través de autómatas celulares.

Referencias:
[1] http://classes.yale.edu/fractals/Panorama/Biology/Leopard/Leopard.html
[2] http://fias.uni-frankfurt.de/fileadmin/fias/triesch/Complex_Systems_Course/slides/CellularAutomata.pdf
[3] http://jonathanpace.wordpress.com/2008/10/31/cellular-automata-how-the-leopard-gets-its-spots/
[4] http://netpbm.sourceforge.net/doc/ppm.html (Portable pixelmap)
"""

import datetime, random, sys

class ActivadorInhibidor(object):
    def __init__(self, inhibicion, rad_int, rad_ext, casillas, iteraciones):
        self.w = inhibicion # constante de inhibición
        self.A = 1.0 # constante de activación
        self.radio_int = rad_int # (radio de) vecindad de activación
        self.radio_ext = rad_ext # (radio de) vecindad de inhibición
        self.filas = casillas # filas del autómata
        self.columnas = casillas # columnas del autómata
        self.iteraciones = iteraciones
        self.automata = []
        
        self.generar_automata()
        self.procesar_automata()
        
    def generar_automata(self):
        for i in xrange(self.filas):
            fil_automata = []
            for j in xrange(self.columnas):
                fil_automata.append(str(int(random.randint(0,1))))
            self.automata.append(fil_automata)
    
    def procesar_automata(self):
        for iteracion in xrange(self.iteraciones):
            automata_iteracion = []
            for i in xrange(self.filas):
                fil_automata = []
                for j in xrange(self.columnas):
                    elementos_vivos = self.contar_celdas_vivas(i, j)
                    AD = elementos_vivos['radio_int']
                    ID = elementos_vivos['radio_ext']
                    regla_automata = (self.A*AD) - (self.w*ID)
                    if regla_automata > 0:
                        fil_automata.append('1')
                    elif regla_automata < 0:
                        fil_automata.append('0')
                    else:
                        fil_automata.append(self.automata[i][j])
                automata_iteracion.append(fil_automata)
            self.automata = automata_iteracion
                    
    def contar_celdas_vivas(self, fil, col):
        """Contar para la celda -> automata[fil][col] los elementos vivos en eje X.
        
        Además, para cada celda en el mismo eje, los elementos vivos en su eje Y.
        """
        # elementos vivos en el eje Y para la celda central
        elementos_vivos = self.contar_celdas_vivas_eje_y(fil, col)
        # sumar a elementos vivos
        elementos_vivos['radio_int'] += (1 if self.automata[fil][col] == '1' else 0)
        """
        Contar elementos vivos en el eje X para la celda central,
        y para cada celda su correspondiente en el eje Y.
        """
        radio = self.radio_ext
        col_ant, col_sig = col - 1, col + 1
        i = 0
        while i < radio:
            if col_ant < 0:
                col_ant = self.columnas - 1
            if col_sig >= self.columnas:   
                col_sig = 0
            # hacia la izquierda
            if self.automata[fil][col_ant] == '1':
                if i < self.radio_int:
                    elementos_vivos['radio_int'] += 1
                else:
                    elementos_vivos['radio_ext'] += 1
            # hacia la derecha
            if self.automata[fil][col_sig] == '1':
                if i < self.radio_int:
                    elementos_vivos['radio_int'] += 1
                else:
                    elementos_vivos['radio_ext'] += 1
            # celdas vivas en eje Y para cada celda en eje X
            celda_ant_vivas = self.contar_celdas_vivas_eje_y(fil, col_ant)
            celda_sig_vivas = self.contar_celdas_vivas_eje_y(fil, col_sig)
            if i < self.radio_int:
                elementos_vivos['radio_int'] += celda_ant_vivas['radio_int'] + celda_sig_vivas['radio_int']
            else:
                elementos_vivos['radio_ext'] += celda_ant_vivas['radio_int'] + celda_sig_vivas['radio_int']
            elementos_vivos['radio_ext'] += celda_ant_vivas['radio_ext'] + celda_sig_vivas['radio_ext']
            col_ant -= 1
            col_sig += 1
            i += 1
            
        return elementos_vivos
    
    def contar_celdas_vivas_eje_y(self, fil, col):
        """Contar elementos vivos en el eje Y para la celda -> automata[fil,col]."""
        elementos_vivos = {'radio_int': 0, 'radio_ext': 0}
        radio = self.radio_ext
        fil_ant, fil_sig = fil - 1, fil + 1
        i = 0
        while i < radio:
            if fil_ant < 0:
                fil_ant = self.filas - 1
            if fil_sig >= self.filas:
                fil_sig = 0
            # hacia arriba de la celda
            if self.automata[fil_ant][col] == '1':
                if i < self.radio_int:
                    elementos_vivos['radio_int'] += 1
                else:
                    elementos_vivos['radio_ext'] += 1
            # hacia abajo de la celda
            if self.automata[fil_sig][col] == '1':
                if i < self.radio_int:
                    elementos_vivos['radio_int'] += 1
                else:
                    elementos_vivos['radio_ext'] += 1
            fil_ant -= 1
            fil_sig += 1
            i += 1
    
        return elementos_vivos

    def colorear_automata(self):
        # colores
        colores_rgb = (('188 143 143', '222 184 135'), ('47 79 79', '220 220 220'),
                       ('233 150 122', '230 230 250'))
        colores = int(random.randint(0, len(colores_rgb) - 1))
        color_activador = colores_rgb[colores][0]
        color_inhibidor = colores_rgb[colores][1]
        # colorear automata
        automata_coloreado = []
        for i in xrange(self.filas):
            fila = []
            for j in xrange(self.columnas):
                pixel = color_inhibidor
                if self.automata[i][j] == '1':
                    pixel = color_activador
                fila.append(pixel)
            automata_coloreado.append(fila)
        return automata_coloreado
