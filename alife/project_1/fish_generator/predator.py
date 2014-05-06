# -*- coding: iso-8859-1 -*-

import math, datetime, png
from activador_inhibidor import ActivadorInhibidor

class GenerarDepredador(object):
    def __init__(self, ancho=400, alto=400):
        self.matriz = [] # matriz con la que se dibujará
        self.ancho, self.alto = ancho, alto    
        #self.eje_mayor = 144
        #self.eje_menor = 81   
        
        self.poblar_matriz()
        self.generar_pez()
        self.dibujar_pez()
        
    def poblar_matriz(self):
        """Poblar la matriz."""
        for i in xrange(self.ancho):
            fila = []
            for j in xrange(self.alto):
                fila.append('agua')
            self.matriz.append(fila)
            
    def generar_pez(self):
        """Método principal para dibujar un pez con figuras geométricas."""
        # calcular las coordenadas de la mitad (ejes X e Y) de la matriz
        mitad_x = int(round(float(self.ancho) / 2, 0))
        mitad_y = int(round(float(self.alto) / 2, 0)) - 30
        
        # dibujar el cuerpo del tiburon como elipse
        eje_mayor = 144
        eje_menor = 55
        self.dibujar_elipse(mitad_x, mitad_y, eje_mayor, eje_menor)
        
        # dibujar boca
        self.dibujar_elipse(mitad_x, mitad_y-135, 30, 6, 'agua')
        
        # dibujar ojo
        self.dibujar_circulo(mitad_x-35, mitad_y-100, 16, 'ojo')
        self.dibujar_circulo(mitad_x-35, mitad_y-100, 4, 'vista')
        
        # dibujar tronco (cerca a cola)
        alto_tronco, ancho_tronco = 10, 45
        col_sig = mitad_x + (eje_mayor - 55)
        for i in xrange(ancho_tronco):
            self.poblar_eje_y(mitad_x, col_sig, alto_tronco)
            col_sig += 1
            
        # dibujar cola básica
        ancho_cola = 70
        col_sig = col_sig - 20
        for i in xrange(ancho_cola):
            self.poblar_eje_y(mitad_x, col_sig, ancho_cola - (ancho_cola - i))
            col_sig += 1
            
        # 'partir' cola
        ancho_cola = 40
        col_sig = col_sig - 35
        for i in xrange(ancho_cola):
            self.poblar_eje_y(mitad_x, col_sig, ancho_cola - (ancho_cola - i), 'agua')
            col_sig += 1
            
        # dibujar aleta
        alto_aleta = 70
        fil_ant = mitad_y - (eje_menor - 40)
        for i in xrange(alto_aleta):
            self.poblar_eje_x(fil_ant, mitad_y+50, alto_aleta - i, '1', 'izq')
            fil_ant -= 1
            
        # aleta
        alto_aleta = 40
        fil_sig = mitad_y + (eje_menor + 20)
        for i in xrange(alto_aleta):
            self.poblar_eje_x(fil_sig, mitad_y-20, alto_aleta - i, '1', 'izq')
            fil_sig += 1
        
        # 'aleticas' antes de cola
        alto_aleta = 30
        fil_ant = mitad_y - (eje_menor - 60)
        fil_sig = mitad_y + (eje_menor)
        for i in xrange(alto_aleta):
            self.poblar_eje_x(fil_ant, mitad_y+120, alto_aleta - i, '1', 'izq')
            self.poblar_eje_x(fil_sig, mitad_y+120, alto_aleta - i, '1', 'izq')
            fil_ant -= 1
            fil_sig += 1
        
    def dibujar_elipse(self, fil, col, eje_mayor, eje_menor, caracter='1'):
        """Dibujar un forma geométrica de elipse.
        
        Las coordenadas (0,0) del punto central representan la celda -> matriz[fil,col].
        El eje mayor representa al eje X.
        """
        col_ant = col - 1 # representa los puntos en -X
        col_sig = col + 1 # representa los puntos en X
        for i in xrange(-1, eje_mayor, 1):
            raiz_cuadrada = math.pow(eje_menor, 2)*(1-(math.pow(i+1, 2)/math.pow(eje_mayor, 2)))
            y = int(round(math.sqrt(raiz_cuadrada), 0))
            # cuando i == -1 -> x == 0
            if i == -1:
                self.poblar_eje_y(fil, col, y, caracter)                
            else:
                self.poblar_eje_y(fil, col_ant, y, caracter)
                self.poblar_eje_y(fil, col_sig, y, caracter)
                col_ant -= 1
                col_sig += 1
    
    def dibujar_circulo(self, fil, col, radio, caracter='1'):
        """Dibujar un forma geométrica de círculo.
        
        Las coordenadas (0,0) del punto central representan la celda -> matriz[fil,col].
        El eje mayor representa al eje X.
        """
        col_ant = col - 1 # representa los puntos en -X
        col_sig = col + 1 # representa los puntos en X
        for i in xrange(-1, radio, 1):
            raiz_cuadrada = math.pow(radio, 2) - math.pow(i+1, 2)
            y = int(round(math.sqrt(raiz_cuadrada), 0))
            # cuando i == -1 -> x == 0
            if i == -1:
                self.poblar_eje_y(fil, col, y, caracter)                
            else:
                self.poblar_eje_y(fil, col_ant, y, caracter)
                self.poblar_eje_y(fil, col_sig, y, caracter)
                col_ant -= 1
                col_sig += 1
            
    def poblar_eje_y(self, fil, col, radio, caracter = '1'):
        """Poblar con un caracter definido, el eje Y e -Y para una celda -> matriz[fil][col].""" 
        fil_ant, fil_sig = fil - 1, fil + 1
        self.matriz[fil][col] = caracter
        for i in xrange(radio):
            self.matriz[fil_ant][col] = caracter
            self.matriz[fil_sig][col] = caracter
            fil_ant -= 1
            fil_sig += 1
    
    def poblar_eje_x(self, fil, col, radio, caracter='1', lados='ambos'):
        col_ant, col_sig = col - 1, col + 1
        self.matriz[fil][col] = caracter
        for i in xrange(radio):
            if lados == 'ambos' or lados == 'izq':
                self.matriz[fil][col_ant] = caracter
            if lados == 'ambos' or lados == 'der':
                self.matriz[fil][col_sig] = caracter
            col_ant -= 1
            col_sig += 1
        
    def dibujar_pez(self):
        # generar Turing morph
        turing_morph = ActivadorInhibidor(0.41, 3, 6, self.ancho, 10)
        patron_colores = turing_morph.colorear_automata()
        """
        Recortar el espacio de la matriz, tanto en lo ancho como en lo alto,
        para sólo dibujar la figura del pez.
        """
        s = 'P3\n{} {}\n255\n'.format(self.ancho, self.alto)
        for i in xrange(self.ancho):
            linea = ''
            for j in xrange(self.alto):
                if self.matriz[i][j] == 'agua':
                    linea += '255 255 255'
                elif self.matriz[i][j] == '1':
                    # verificar si la celda hace parte del borde
                    if self.dibujar_borde(i, j, 'agua'):
                        linea += '0 0 0'
                    else:
                        linea += patron_colores[i][j]
                elif self.matriz[i][j] == 'ojo':
                    if self.dibujar_borde(i, j, 'agua') or self.dibujar_borde(i, j, '1'):
                        linea += '0 0 0'
                    else:
                        linea += '255 255 255'
                elif self.matriz[i][j] == 'vista':
                    linea += '0 0 0'
                elif self.matriz[i][j] == 'boca':
                    linea += '255 255 255'
                linea += ' ' * 3
            s += linea.rstrip() + ('\n' if i < self.ancho - 1 else '')
        tiempo = datetime.datetime.today().strftime('%Y%m%d-%H%M%S')
        pez_salida = open('img/predator_{}.ppm'.format(tiempo), 'w+')
        pez_salida.write(s)
        pez_salida.flush()
    
    def dibujar_borde(self, fil, col, caracter='0'):
        """Dibujar el borde de la figura del pez."""
        borde = False
        if self.matriz[fil-1][col]==caracter or self.matriz[fil+1][col]==caracter:
            borde = True
        elif self.matriz[fil][col-1]==caracter or self.matriz[fil][col+1]==caracter:
            borde = True
        return borde

if __name__ == '__main__':
    GenerarDepredador()
