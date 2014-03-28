# -*- coding: iso-8859-1 -*-

import turtle

class Lindenmeyer(object):
    def __init__(self, axioma, reglas, angulo, iteraciones, 
                 distancia=5, rotacion_inicial=0, posx_inic=0, posy_inic=0):
        self.axioma = axioma
        self.reglas = reglas
        self.angulo = angulo
        self.iteraciones = iteraciones
        self.distancia = distancia
        self.rotacion_inicial = rotacion_inicial
        self.posx_inic = posx_inic
        self.posy_inic = posy_inic
        
        self.instrucciones = ''
        self.aplicar_reglas()

    def aplicar_reglas(self):
        transformaciones = []

        transformaciones.append(self.axioma)
        for i in xrange(1, self.iteraciones + 1):
            string = transformaciones[i - 1]
            t = ''
            for s in string:
                if s in self.reglas:
                    t += self.reglas[s]
                else:
                    t += s
            transformaciones.append(t)

        self.instrucciones = transformaciones[self.iteraciones]

    def dibujar_sistema(self):
        tortuga = turtle.Turtle()
        
        tortuga.up()
        tortuga.setpos(self.posx_inic, self.posy_inic)
        tortuga.left(self.rotacion_inicial)
        tortuga.down()
        tortuga.speed(10)
        
        ventana = turtle.Screen()
        
        estado_actual = []
        for inst in self.instrucciones:
            if inst == 'F':
                # dibujar hacia adelante
             tortuga.forward(self.distancia)
            elif inst == 'f':
                # mover hacia adelante sin dibujar
                tortuga.penup()
                tortuga.forward(self.distancia)
                tortuga.pendown()
            elif inst == '+':
                # rotar hacia la derecha
                tortuga.right(self.angulo)
            elif inst == '-':
                # rotar hacia la izquierda
                tortuga.left(self.angulo)
            elif inst == '[':
                # obtener la posición actual
                pos = {'x': tortuga.xcor(), 'y': tortuga.ycor()}
                # grados sentido contra-reloj
                direc = tortuga.heading()
                # guardar estado
                estado_actual.append({'pos': pos, 'dir': direc})
            elif inst == ']':
                ult_estado = estado_actual.pop()
                pos, direc = ult_estado['pos'], ult_estado['dir']
                tortuga.penup()
                tortuga.goto(pos['x'], pos['y'])
                tortuga.setheading(direc)
                tortuga.pendown()
                
        tortuga.hideturtle()          
