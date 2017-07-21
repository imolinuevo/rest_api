# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from splunkdj.decorators.render import render_to

@render_to('prueba:home.html')
@login_required

def home(request):

    query_1 = """
        | inputlookup traffic_violations.csv
        | rename "Date Of Stop" as fecha "Time Of Stop" as time
        | eval fecha = fecha." ".time
        | eval fecha_epoch = strptime(fecha,"%d/%m/%Y %H:%M:%S")
        $filtro_fecha$
        | rename "Make" as coche
        $filtro_coche$
        | rename "Alcohol" as alcohol 
        | where alcohol="Yes"
        | stats count by coche
        | rename coche as "Marca de coche" count as "Positivos en Alcohol"
    """

    query_2 = """
        | inputlookup traffic_violations.csv
        | rename "Make" as coche
        $filtro_coche$
        | rename "Year" as year
        | where year>1900 AND year<2018
        $filtro_anyo$
        | stats count by year
        | rename year as "Año" count as "Num de Infracciones"
    """

    query_2_map = """
        | inputlookup traffic_violations.csv
        | rename "Make" as coche
        $filtro_coche$
        | rename "Year" as year "Latitude" as lat "Longitude" as lon
        | where year>1900 AND year<2018
        $filtro_anyo$
        | geostats count by year
    """


    context = {
        "query_1":query_1,
        "query_2":query_2,
        "query_2_map":query_2_map,

    }
    
    context = { q: ' '.join( context[q].replace("\n"," ").replace("\t"," ").split()) for q in context }

    return context