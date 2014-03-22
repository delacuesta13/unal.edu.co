# -*- coding: iso-8859-1 -*-

import sys, datetime, math

def generar_fechas(f_min, f_max):
    """Generar un CSV con las fechas entre el rango definido."""
    fechas = [f_min.split("/"), f_max.split("/")]
    fecha_min = datetime.date(int(fechas[0][0]), int(fechas[0][1]), int(fechas[0][2]))
    fecha_max = datetime.date(int(fechas[1][0]), int(fechas[1][1]), int(fechas[1][2]))    
    fecha_iterador = fecha_min
       
    salida = []
    # agregar cabecera del archivo
    salida.append('date, date_description,day,day_week,month,calendar_month,quarter,semester,year')
    
    while fecha_iterador <= fecha_max:
        linea = fecha_iterador.strftime("%Y/%m/%d,%B %d %Y,%d,%A,%m,%B,")
        linea += "%d," % int(math.ceil((float(fecha_iterador.month) / 12) * 4))
        linea += "%d," % int(math.ceil((float(fecha_iterador.month) / 12) * 2))
        linea += "%d" % fecha_iterador.year
        
        salida.append(linea)
        
        # incremento la fecha en un día
        fecha_iterador += datetime.timedelta(days=1)
    
    # escribir archivo de salida
    a_salida = "fechas.{:d}{:02d}{:d}_{:d}{:02d}{:d}.csv".format(
        fecha_min.year, fecha_min.month, fecha_min.day,
        fecha_max.year, fecha_max.month, fecha_max.day
        )
    archivo_salida = open(a_salida, 'w+')
    for s in salida:
        archivo_salida.write(s + '\n')
    archivo_salida.flush()

if __name__ == '__main__':
    generar_fechas(sys.argv[1], sys.argv[2])
    # generar_fechas("2013/07/31", "2013/08/31")
    
