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
        self.dibujar_automata()
        
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

    def dibujar_automata(self, rgb=False):
        # dimensión de las imágenes
        dimension_img = str(self.columnas) + ' ' + str(self.filas)
        salida = []
        salida.append('P1\n' + dimension_img + '\n') # imagen en blanco y negro
        salida.append('P3\n' + dimension_img + '\n255\n') # imagen en RGB
        # colores
        colores_rgb = {'black':   '  0  0   0',  'red':   '255  0    0', 'green': '  0 255   0',
                       'blue':    '  0  0 255', 'yellow': '255 255   0', 'cyan':  '  0 255 255',
                       'magenta': '255  0 255', 'white':  '255 255 255'}
        color_activador = random.choice(colores_rgb.keys())
        color_inhibidor = random.choice(colores_rgb.keys())
        while color_activador == color_inhibidor:
            color_inhibidor = random.choice(colores_rgb.keys())
        # dibujar imágenes
        for i in xrange(self.filas):
            linea = ''
            linea_rgb = ''
            for j in xrange(self.columnas):
                pixel = colores_rgb[color_inhibidor]
                if self.automata[i][j] == '1':
                    pixel = colores_rgb[color_activador]
                linea_rgb += pixel + (' '*4)
                linea += self.automata[i][j] + ' '
            salida[1] += linea_rgb.rstrip() + ('\n' if i < self.filas - 1 else '')
            salida[0] += linea.rstrip() + ('\n' if i < self.filas - 1 else '')
        # generar archivos
        tiempo = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
        c_inh =  str(self.w)[2:]
        c_inh = (c_inh + '0') if len(c_inh) == 1 else c_inh
        posfijo_archivo = 'w{0}_r{1}-{2}_{3}x{3}_{4}'.format(c_inh, self.radio_int, self.radio_ext, self.filas, tiempo)
        # imagen en blanco y negro
        aut_bn = open('img/ac_act-inh_' + posfijo_archivo + '.pbm', 'w+')
        aut_bn.write(salida[0])
        aut_bn.flush()
        # imagen en RGB
        if rgb:
            aut_rgb = open('img/ac_act-inh_' + posfijo_archivo + '.ppm', 'w+') 
            aut_rgb.write(salida[1])
            aut_rgb.flush()
        
def main():
    constante_inhibicion = float(random.randint(30, 50)) / 100
    radio_int, radio_ext = 3, 6
    casillas = 200
    iteraciones = 10
    if len(sys.argv) > 1:
        constante_inhibicion = float(sys.argv[1]) / 100
    if len(sys.argv) > 3:
        radio_int, radio_ext = int(sys.argv[2]), int(sys.argv[3])
    if len(sys.argv) > 4:
        casillas = int(sys.argv[4])
    if len(sys.argv) > 5:
        iteraciones = int(sys.argv[5])
        
    ActivadorInhibidor(constante_inhibicion, radio_int, radio_ext, casillas, iteraciones)
            
if __name__ == '__main__':
    main()
