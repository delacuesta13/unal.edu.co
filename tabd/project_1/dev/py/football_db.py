# -*- coding: iso-8859-1 -*-

import os, subprocess, sys, datetime
from listar_competiciones import listar_competiciones 

def football_db(kettle_path, project_dir):
    """Ejecuta por shell el ETL."""
    # limpiar la cadena de la ruta del proyecto
    project_dir = project_dir.strip().rstrip('/')
    
    # obtener la lista de competiciones del directorio de datos
    lista_competiciones = listar_competiciones(project_dir + '/data')
        
    # ejecutar la ETL por cada competición
    for competicion in lista_competiciones:
        log_file = "football_db.{}.{}.log".format(competicion, 
                                                  datetime.datetime.today().strftime('%Y%m%d_%H%M'))
        command_line = "sh {0}/kitchen.sh -file='{1}/dev/kettle/football_db.kjb' ".format(kettle_path, project_dir)
        command_line += "-param:projectDirectory='{0}' -param:competitionDescription='{1}' ".format(project_dir, competicion)
        command_line += "-Level=Rowlevel > {0}/logs/{1}".format(project_dir, log_file)
        
        output = os.system(command_line)
        if output != 0:
            # hubo error ejecutando el ETL
            break
     
if __name__ == '__main__':
    kettle_path = '/opt/kettle'
    default_project_dir = '/var/unal/tabd/project_1'

    if len(sys.argv) == 1:
        football_db(kettle_path, default_project_dir) 
    else:
        football_db(kettle_path, sys.argv[1]) 
