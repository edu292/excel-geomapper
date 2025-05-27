from folium.plugins import HeatMapWithTime, MarkerCluster
from jinja2 import Environment, FileSystemLoader
import pandas as pd
import sqlite3
import folium
import os


def generate_heatmap():
    with sqlite3.connect('geoloc.db') as conn:
        df = pd.read_sql_query("""SELECT 
                                    strftime('%Y-%m-%d', date) as day,
                                    strftime('%Y-%m', date) as month,
                                    info,
                                    lat,
                                    long
                                FROM geoloc
                                ORDER BY day, info
                               """, conn)
    m = folium.Map(location=[df['lat'].mean(), df['long'].mean()], zoom_start=7)
    MarkerCluster().add_to(m)

    coordenadas_por_mes = {}
    mark_cluster = MarkerCluster().add_to(m)
    markers_by_month = {}
    for month, group in df.groupby('month'):
        markers_by_month[month] = []
        coordenadas_por_mes[month] = group[['lat', 'long']].values.tolist()
        if len(group) > 1:
            previous_date = group.iloc[1]['day']
            previous_info = group.iloc[1]['info']
        else:
            previous_date = ''
            previous_info = ''
        for _, row in group.iterrows():
            if row['day'] != previous_date or row['info'] != previous_info:
                marker = {'location': row[['lat', 'long']].values.tolist(),
                          'popup': f"Date: {row['day']}<br>Info: {row['info']}"}
                previous_date = row['day']
                previous_info = row['info']
            else:
                marker = {'location': row[['lat', 'long']].values.tolist()}
            markers_by_month[month].append(marker)

    coordenadas_por_mes['Total'] = df[['lat', 'long']].values.tolist()
    HeatMapWithTime(list(coordenadas_por_mes.values()), index=list(coordenadas_por_mes.keys()), radius=20).add_to(m)

    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('map_markers_template.js')

    rendered_js = template.render(
        cluster_var=mark_cluster.get_name(),
        markers_by_month=markers_by_month,
        map_var=m.get_name()
    )

    custom_js = f"<script>\n{rendered_js}\n</script>"
    m.get_root().html.add_child(folium.Element(custom_js))

    m.save("heatMap.html")


def generate_preview(df):
    m = folium.Map(
        location=[df['lat'].mean(), df['long'].mean()],
        zoom_start=5)

    for idx, row in df.iterrows():
        popup_html = f"Address: {row['address']}<br>Info: {row['info']}"
        folium.Marker(
            location=[row['lat'], row['long']],
            popup=popup_html,
            tooltip="Click to select",
            icon=folium.Icon(icon='info-sign')
        ).add_to(m)

    return m