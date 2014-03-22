# -*- coding: iso-8859-1 -*-

import os, os.path, re

def listar_competiciones(project_data_dir):
    """Lista los directorios de competiciones ubicados en los datos del proyecto."""
    # expresión regular de la competición
    rx_competicion = re.compile('^[a-z0-9]+\.([a-z0-9]+\.)?[0-9]{2,4}(_[0-9]{2,4})?$')
    # listar el directorio de datos del proyecto
    p_dir = project_data_dir.strip().rstrip('/')
    listar_dir = os.listdir(p_dir)
    
    competiciones_dir = []
    for d in listar_dir:
        d = d.strip().lower()
        if rx_competicion.match(d) and os.path.isdir(p_dir + '/' + d):
            competiciones_dir.append(d)
    
    return competiciones_dir

