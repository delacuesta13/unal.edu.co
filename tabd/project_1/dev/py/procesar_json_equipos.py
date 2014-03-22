# -*- coding: iso-8859-1 -*-

import sys, json

def procesar_json_equipos(a_entrada, **args):
    """Procesar un archivo JSON con equipos de una competición.
    
    Además, escribe un archivo de salida con una estructura de tabla.
    """
    a_json = open(a_entrada, 'r')    
    data_json = json.load(a_json)    
    a_json.close()
    
    salida = []
    # agregar cabecera del archivo
    salida.append('team_key,team_description,team_organization,country,association_description,confederation_description')
    
    for team in data_json['teams']:
        linea = "{},{},{},{},{},{}".format(team['key'].lower(), team['title'].encode('utf-8').title(),
                                                args['team_organization'].upper(), args['country'].upper(),
                                                args['association_description'].upper(), args['confederation_description'].upper())
        salida.append(linea)
        
    # escribir archivo de salida
    a_salida = data_json['event']['key'].encode('utf-8').replace('/', '_')
    archivo_salida = open(a_salida + ".teams.csv", 'w+')
    for s in salida:
        archivo_salida.write(s + '\n')
    archivo_salida.flush()
 
if __name__ == '__main__':
    procesar_json_equipos(a_entrada=sys.argv[1],
                          team_organization=sys.argv[2], country=sys.argv[3],
                          association_description=sys.argv[4], confederation_description=sys.argv[5])
        

