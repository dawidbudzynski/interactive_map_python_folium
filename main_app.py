import folium
import pandas

data = pandas.read_csv('Volcanoes_USA.txt')
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])
volcano_info = []


def color_producer(elevation):
    if elevation < 1500:
        return 'green'
    elif 1500 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


my_map = folium.Map(location=[lat[0], lon[0]], zoom_start=4, tiles='Mapbox Bright')

fgv = folium.FeatureGroup(name='Volcanoes')

for lt, ln, el in zip(lat, lon, elev):
    fgv.add_child(
        folium.RegularPolygonMarker(location=[lt, ln], popup=folium.Popup(str(el) + ' m', parse_html=True),
                                    fill_color=color_producer(el), number_of_sides=6, radius=10, fill_opacity=0.7,
                                    color='gray'))

fgp = folium.FeatureGroup(name='Population')

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                             style_function=lambda x: {'fillColor': 'yellow' if x['properties']['POP2005'] < 20000000
                             else 'green' if 20000000 <= x['properties']['POP2005'] < 40000000
                             else 'blue'}))

my_map.add_child(fgp)
my_map.add_child(fgv)


my_map.add_child(folium.LayerControl())

my_map.save('index.html')
