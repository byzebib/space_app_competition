#!/usr/bin/env python
# coding: utf-8

# In[1]:


from ipyleaflet import Map, basemaps, basemap_to_tiles, Heatmap, TileLayer
from ipywidgets import AppLayout
from ipywidgets import HTML, Layout, Dropdown, Output, Textarea, VBox, Label
import bqplot as bq
import numpy as np
from pandas import date_range


# In[2]:


OWM_API_KEY = '631e152dc7fad36960df657774e3cc9e'


# In[24]:


m = Map(center=(35, 20), zoom=4, basemap=basemaps.Esri.WorldImagery)
display(m)


# In[25]:


maps = {'NASA' : basemaps.NASAGIBS.ModisTerraBands367CR,
        'Esri' : basemaps.Esri.DeLorme}


# In[26]:


header = HTML("<h1>Prediction Model: Mediterrean Sea Weather (Fictional model)</h1>", layout=Layout(height='auto'))
header.style.text_align='center'
basemap_selector = Dropdown( options = list(maps.keys()),
                            layout=Layout(width='auto'))

heatmap_selector = Dropdown(options=('Temperature', 'Precipitation'),
                            layout=Layout(width='auto'))


# In[27]:


basemap_selector.value = 'NASA'
m.layout.height='600px'


# In[28]:


security_1 = np.cumsum(np.random.randn(150)) + 100.

dates = date_range(start='06-20-2020', periods=150)

dt_x = bq.DateScale()
sc_y = bq.LinearScale()

time_series = bq.Lines(x=dates, y=security_1, scales={'x': dt_x, 'y': sc_y})
ax_x = bq.Axis(scale=dt_x)
ax_y = bq.Axis(scale=sc_y, orientation='vertical')

fig = bq.Figure(marks=[time_series], axes=[ax_x, ax_y],
                fig_margin=dict(top=0, bottom=80, left=30, right=20))


# In[29]:


m.layout.width='auto'
m.layout.height='auto'
fig.layout.width='auto'
fig.layout.height='auto'


# In[30]:


out = HTML(
    value='',
    layout=Layout(width='auto', height='auto')
)


# In[31]:


AppLayout(center=m, 
          header=header,
          left_sidebar=VBox([Label("Basemap:"),
                             basemap_selector,
                             Label("Overlay:"),
                             heatmap_selector]),
          right_sidebar=fig,
          footer=out,
          pane_widths=['80px', 1, 1],
          pane_heights=['80px', 4, 1],
          height='600px',
          grid_gap="30px")


# In[11]:


row=[]


# In[12]:


X, Y = np.mgrid[-90:90:10j, -180:180:20j]


# In[13]:


X = X.flatten()
Y = Y.flatten()


# In[14]:


temps = np.random.randn(200, 150)*0.5


# In[15]:


from datetime import datetime


# In[16]:


import random


# In[17]:


def add_log(msg):
    max_rows = 3
    rows.append(msg)
    if len(rows) > max_rows:
        rows.pop(0)
    return '<h4>Activity log</h4><ul>{}</ul>'.format('<li>'.join([''] + rows))

def generate_temp_series(x, y):
    if heatmap_selector.value == 'Precipitation':
        temp = np.cumsum(np.random.randn(150)) + 100.
    elif heatmap_selector.value == 'Temperature':
        dist = np.sqrt((X - x)**2 + (Y-y)**2) / 100
        dist = dist.max() - dist
        dist[dist > np.percentile(dist, 5)] = 0
        temp = np.cumsum(np.dot(dist, temps)+0.05) + 20 - np.abs(x) / 2
    time_series.y = temp
    
def handle_interaction(**kwargs):
    if kwargs['type'] == 'click':
        generate_temp_series(*kwargs['coordinates'])
        msg = '%s Selected coordinates: %s, Temp: %d C Precipitation: %d mm\n' % (
            datetime.now(), kwargs['coordinates'], random.randint(-20, 20), random.randint(0, 100))
        out.value = add_log(msg)

m.on_interaction(handle_interaction) 

def on_map_selected(change):
    m.layers = [basemap_to_tiles(maps[basemap_selector.value]), weather_maps[heatmap_selector.value]]
    
basemap_selector.observe(on_map_selected, names='value')
heatmap_selector.observe(on_map_selected, names='value')


# In[18]:


temp = TileLayer(min_zoom=1, max_zoom=18, url='https://tile.openweathermap.org/map/temp_new/{z}/{x}/{y}.png?appid='+OWM_API_KEY, name='owm', attribute='me')
precipitation = TileLayer(min_zoom=1, max_zoom=18, url='https://tile.openweathermap.org/map/precipitation_new/{z}/{x}/{y}.png?appid='+OWM_API_KEY, name='owm', attribute='me')


# In[19]:


weather_maps = {'Temperature' : temp,
                'Precipitation' : precipitation}


# In[20]:


m.add_layer(weather_maps[heatmap_selector.value])


# In[ ]:





# In[ ]:




