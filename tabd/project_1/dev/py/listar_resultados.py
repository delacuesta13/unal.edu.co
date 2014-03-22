# -*- coding: iso-8859-1 -*-

import sys, json, urllib2

def listar_resultados(competicion, ronda_min, ronda_max=-1):
    """Genera un archivo CSV con los resultados entre un rango para una competición."""
    salida = []
    # agregar cabecera del archivo
    salida.append('competition_key,date,home_team_key,away_team_key,match_round,full_time_home_team_goals,full_time_away_team_goals,full_time_result')
    
    ronda_min, ronda_max = int(ronda_min), int(ronda_max)
    if ronda_max == -1:
        ronda_max = ronda_min
    
    for i in xrange(ronda_min, ronda_max + 1):
        url_json = "http://footballdb.herokuapp.com/api/v1/event/{}/round/{}".format(competicion, i)
        consulta_json = urllib2.urlopen(url_json)
        data_json = json.load(consulta_json)
        
        competition_key = data_json['event']['key']
        match_round = data_json['round']['title'].replace("/", "-")
        
        for game in data_json['games']:
            try:
                home_goals = int(game['score1'])
                away_goals = int(game['score2'])
                if home_goals > away_goals:
                    full_time_result = 'h'
                elif home_goals < away_goals:
                    full_time_result = 'a'
                else:
                    full_time_result = 'd' 
                linea = "{},{},{},{},{},{},{},{}".format(competition_key.lower(), game['play_at'],
                                                                game['team1_key'].lower(), game['team2_key'].lower(), match_round.title(),
                                                                str(home_goals), str(away_goals), full_time_result.upper())
                salida.append(linea)
            except:
                pass
            
    # escribir archivo de salida
    a_salida = data_json['event']['key'].encode('utf-8').replace('/', '_') + "."
    if ronda_max - ronda_min > 0:
        a_salida += "rounds.{}_{}".format(ronda_min, ronda_max)
    else:
        a_salida += "round.{}".format(ronda_min)
        
    archivo_salida = open(a_salida + ".csv", 'w+')    
    for s in salida:
        archivo_salida.write(s + '\n')
    archivo_salida.flush()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        listar_resultados(sys.argv[1], sys.argv[2])
    else:
        listar_resultados(sys.argv[1], sys.argv[2], sys.argv[3])
