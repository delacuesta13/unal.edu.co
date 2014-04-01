# -*- coding: iso-8859-1 -*-

import re
from Tkinter import *
import ttk, tkMessageBox
from lindenmeyer import Lindenmeyer

class FrontEnd(object):
    def __init__(self, parent):
        self.parent = parent
        
        self.l_systems = {}
        
        self.cargar_sistemas()
        self.inicializar_UI()
        self.limpiar_formulario()
        
    def cargar_sistemas(self):
        with open('sistemas.csv') as sistemas:
            for i, sistema in enumerate(sistemas):
                if i == 0:
                    continue
                sistema = sistema.rstrip('\n')
                fila = sistema.split(',')
                sistema_key = fila.pop(0)
                self.l_systems[sistema_key] = fila
    
    def inicializar_UI(self):
        self.parent.title('Lindemeyer Systems')
        
        self.frame = ttk.Frame(self.parent, padding="15 10 15 10")
        self.frame.grid(column=0, row=0)
        
        self.sistemas = StringVar()
        self.axioma = StringVar()
        self.regla_1 = StringVar()
        self.regla_2 = StringVar()
        self.regla_3 = StringVar()
        self.angulo = StringVar()
        self.iteraciones = StringVar()
        self.distancia = StringVar()
        self.rotacion_inicial = StringVar()
        self.posicion_inicial = StringVar()
        
        self.sistemas.trace('w', self.on_system_change)
        ttk.Label(self.frame, text="Sistema").grid(column=1, row=1)
        self.form_sistemas = ttk.Combobox(self.frame, width=29, textvariable=self.sistemas, values=self.l_systems.keys()).grid(column=2, row=1)
        # axioma
        ttk.Label(self.frame, text="Axioma").grid(column=1, row=2, pady=5)
        form_axioma = ttk.Entry(self.frame, width=30, textvariable=self.axioma).grid(column=2, row=2, padx=0)
        # regla 1
        ttk.Label(self.frame, text="Regla 1").grid(column=1, row=3, pady=5)
        form_regla_1 = ttk.Entry(self.frame, width=30, textvariable=self.regla_1).grid(column=2, row=3)
        # regla 2
        ttk.Label(self.frame, text="Regla 2").grid(column=1, row=4, pady=5)
        form_regla_2 = ttk.Entry(self.frame, width=30, textvariable=self.regla_2).grid(column=2, row=4)
        # regla 3
        ttk.Label(self.frame, text="Regla 3").grid(column=1, row=5, pady=5)
        form_regla_3 = ttk.Entry(self.frame, width=30, textvariable=self.regla_3).grid(column=2, row=5)
        # Ángulo
        ttk.Label(self.frame, text="Ángulo").grid(column=1, row=6, pady=5)
        form_angulo = Spinbox(self.frame, width=10, from_=0, to=360, textvariable=self.angulo).grid(column=2, row=6)
        # iteraciones
        ttk.Label(self.frame, text="Iteraciones").grid(column=1, row=7, pady=5)
        form_iteraciones = Spinbox(self.frame, width=10, from_=0, to=20, textvariable=self.iteraciones).grid(column=2, row=7)
        # rotación inicial
        ttk.Label(self.frame, text="Rotación inicial").grid(column=1, row=8, pady=5)
        form_rotacion_inicial = Spinbox(self.frame, width=10, from_=-380, to=360, textvariable=self.rotacion_inicial).grid(column=2, row=8)
        # distancia
        ttk.Label(self.frame, text="Distancia").grid(column=1, row=9, pady=5)
        form_distancia = Spinbox(self.frame, width=10, from_=0, to=1000, textvariable=self.distancia).grid(column=2, row=9)
        # posición inicial
        ttk.Label(self.frame, text="Posición inicial (x,y)").grid(column=1, row=10, pady=5)
        form_posicion_inicial = ttk.Entry(self.frame, width=11, textvariable=self.posicion_inicial).grid(column=2, row=10)
        
        ttk.Button(self.frame, text="Limpiar formulario", command=self.limpiar_formulario).grid(column=1, row=11, pady=10)
        ttk.Button(self.frame, text="Dibujar sistema", command=self.validar_datos).grid(column=2, row=11)
        
    def on_system_change(self, index, value, op):
        sistema = self.sistemas.get().strip().replace(' ', '')
        if len(sistema) > 0:
            self.limpiar_formulario(False)
            fila = self.l_systems[sistema]
            self.axioma.set(fila[1])
            reglas = fila[2].split('/')
            for i, regla in enumerate(reglas):
                if i == 0:
                    self.regla_1.set(regla)
                elif i == 1:
                    self.regla_2.set(regla)
                else:
                    self.regla_3.set(regla)
            self.angulo.set(fila[3])
            self.iteraciones.set(fila[4])
            self.distancia.set(fila[5])
            self.rotacion_inicial.set(fila[6])
            self.posicion_inicial.set(fila[7].replace('/',','))
    
    def limpiar_formulario(self, limpiar_sistema=True):
        if limpiar_sistema:
            self.sistemas.set('')
        self.axioma.set('')
        self.regla_1.set('')
        self.regla_2.set('')
        self.regla_3.set('')
        self.angulo.set('0')
        self.iteraciones.set('0')
        self.distancia.set('5')
        self.rotacion_inicial.set('0')
        self.posicion_inicial.set('0,0')
    
    def validar_datos(self):
        # regex
        rx_axioma = re.compile('^[A-Za-z\[\]\+\-]+$')
        rx_regla = re.compile('^[A-Za-z]{1}\=[A-Za-z\+\-\[\]]+$')
        rx_numero = re.compile('^\-?[0-9]+$')
        rx_pos_inic = re.compile('^\-?[0-9]+\,\-?[0-9]+$')
        
        s_axioma = self.axioma.get().strip().replace(' ', '')
        s_reglas = [self.regla_1.get().strip().replace(' ', ''),
                    self.regla_2.get().strip().replace(' ', ''),
                    self.regla_3.get().strip().replace(' ', '')]
        s_angulo = self.angulo.get().strip().replace(' ', '')
        s_iteraciones = self.iteraciones.get().strip().replace(' ', '')
        s_distancia = self.distancia.get().strip().replace(' ', '')
        s_rotacion_inicial = self.rotacion_inicial.get().strip().replace(' ', '')
        s_posicion_inicial = self.posicion_inicial.get().strip().replace(' ', '')
        
        errores = []
        
        if not rx_axioma.match(s_axioma):
            errores.append('No se ha ingresado un axioma válido.')
        reglas = {}
        reglas_validas = 0
        for i, regla in enumerate(s_reglas):
            if len(regla) > 0 and rx_regla.match(regla):
                temp = regla.split('=')
                reglas[temp[0]] = temp[1]
                reglas_validas += 1
            elif len(regla) > 0:
                errores.append('Regla {} no es válida.'.format(i+1))
        else:
            if reglas_validas == 0:
                errores.append('Debe ingresarse una o más reglas válidas para transformar.')
        if not rx_numero.match(s_angulo):
            errores.append('El ángulo ingresado no es válido.')
        if not rx_numero.match(s_iteraciones) or int(s_iteraciones) < 0:
            errores.append('El número de iteraciones no es válido.')
        if not rx_numero.match(s_distancia) or int(s_distancia) <= 0:
            errores.append('La distancia no es válida.')
        if not rx_numero.match(s_rotacion_inicial):
            errores.append('El grado de rotación no es válido.')
        if not rx_pos_inic.match(s_posicion_inicial):
            errores.append('Las coordenadas iniciales no son válidas.')
            
        if len(errores) > 0:
            s_error = 'Por favor corregir los siguientes errores encontrados.\n'
            for i, error in enumerate(errores):
                s_error += '\n{}. {}'.format(i+1, error)
            tkMessageBox.showwarning(title='Errores encontrados', icon='warning', 
                                      message=s_error)
        else:
            posiciones = s_posicion_inicial.split(',')
            l_system = Lindenmeyer(s_axioma, reglas, int(s_angulo), 
                                   int(s_iteraciones), int(s_distancia),
                                   int(s_rotacion_inicial), 
                                   int(posiciones[0]), int(posiciones[1]))
            l_system.dibujar_sistema(True)

def main():
    root = Tk()
    root.resizable(FALSE,FALSE)
    
    interfaz = FrontEnd(root)
    
    x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
    y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
    root.geometry("+%d+%d" % (50, y))
    
    root.mainloop()
        
if __name__ == '__main__':
    main()
