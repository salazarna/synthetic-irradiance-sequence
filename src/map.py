import folium
from folium import plugins

def draw_map(download:bool=False):
    # Map canvas
    MAP = folium.Map(location=[4.60, -74.06],
                    zoom_start=2.5,
                    tiles='Open Street Map',
                    control_scale=True)

    # Bogotá
    folium.Marker(location=[4.60, -74.06],
                    popup=folium.Popup(f'<b>Bogotá</b>', min_width=250, max_width=250),
                    tooltip=f'<b>Bogotá</b>',
                    icon=folium.Icon(icon='asterisk', prefix='fa', color='blue')).add_to(MAP)

    folium.Marker(location=[3.5, -78],
                icon=folium.DivIcon(html=('<div style="font-size: 13pt"><b>Bogotá</b></div>'))).add_to(MAP)

    # Oregon
    folium.Marker(location=[45.52, -122.67],
                    popup=folium.Popup(f'<b>Oregon</b>', min_width=250, max_width=250),
                    tooltip=f'<b>Oregon</b>',
                    icon=folium.Icon(icon='asterisk', prefix='fa', color='green')).add_to(MAP)

    folium.Marker(location=[45, -127],
                icon=folium.DivIcon(html=('<div style="font-size: 13pt"><b>Oregon</b></div>'))).add_to(MAP)

    # Tucson
    folium.Marker(location=[32.16, -110.99],
                    popup=folium.Popup(f'<b>Tucson</b>', min_width=250, max_width=250),
                    tooltip=f'<b>Tucson</b>',
                    icon=folium.Icon(icon='asterisk', prefix='fa', color='purple')).add_to(MAP)

    folium.Marker(location=[31.5, -115],
                icon=folium.DivIcon(html=('<div style="font-size: 13pt"><b>Tucson</b></div>'))).add_to(MAP)

    # Seville
    folium.Marker(location=[37.37, -5.98],
                    popup=folium.Popup(f'<b>Seville</b>', min_width=250, max_width=250),
                    tooltip=f'<b>Seville</b>',
                    icon=folium.Icon(icon='asterisk', prefix='fa', color='red')).add_to(MAP)

    folium.Marker(location=[38, -17],
                icon=folium.DivIcon(html=('<div style="font-size: 13pt"><b>Seville</b></div>'))).add_to(MAP)

    # Adelaide
    folium.Marker(location=[-34.92, 138.61],
                    popup=folium.Popup(f'<b>Adelaide</b>', min_width=250, max_width=250),
                    tooltip=f'<b>Adelaide</b>',
                    icon=folium.Icon(icon='asterisk', prefix='fa', color='orange')).add_to(MAP)

    folium.Marker(location=[-36, 133],
                icon=folium.DivIcon(html=('<div style="font-size: 13pt"><b>Adelaide</b></div>'))).add_to(MAP)

    # Zoom
    plugins.ScrollZoomToggler().add_to(MAP)

    # Full window
    plugins.Fullscreen(position='topright').add_to(MAP)

    # Layers
    folium.LayerControl(position='topright').add_to(MAP)

    # Download
    if download == True:
        MAP.save(f'../figs/map.html')

    return MAP