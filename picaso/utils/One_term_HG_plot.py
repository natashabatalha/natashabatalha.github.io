import numpy as np
from bokeh.plotting import *
from bokeh.palettes import Spectral10, Viridis3
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import column, widgetbox
from bokeh.models import CustomJS, Slider,Div

from bokeh.resources import CDN
from bokeh.embed import autoload_static

fig = Figure(y_range=[-4,4] ,x_range=[-8,8], width = 550, height = 200,
	y_axis_label='Light from here',x_axis_label='Back Scattering <-----> Forward Scattering')
g = 0.6
azimuths = np.linspace(0, 2 * np.pi, 10000)
#ranges = np.array([2, 4, 6, 8])
for g in list(np.linspace(-0.9,0.9,10))+[0]:

	phase = (1.0-g**2)/np.sqrt(1+ g**2 - 2.0*g * np.cos(azimuths))**3.0

	xx = phase*np.cos(azimuths)
	yy = phase*np.sin(azimuths)
	if g ==0:
		x = xx
		y = yy

	fig.line(xx,yy, line_width =3, alpha=0.3, color='grey')

source = ColumnDataSource(data=dict(x=x, y=y, az = azimuths))

fig.line('x','y', line_width =5, alpha=0.8, color=Viridis3[1],source=source)

callback = CustomJS(args=dict(source=source), code="""
    var data = source.data;
    var g = g.value;

    var x = data['x'];
    var y = data['y'];
    var az = data['az'];

    var phase = 0 ;

    for (var i = 0; i < x.length; i++) {
    	phase = (1.0-Math.pow(g,2))/Math.pow(Math.sqrt(1.0+ Math.pow(g,2) - 2.0 *g * Math.cos(az[i])),3.0);
        x[i] = phase*Math.cos(az[i]);
        y[i] = phase*Math.sin(az[i]);
    }
    source.change.emit();
""")

g_slider = Slider(start=-1, end=1, value=0, step=.05,
                     callback=callback)

callback.args["g"] = g_slider

div = Div(text="""<big><b>OTHG,Asymmetry Parameter, <em>g</em></b></big>""")

layout = column(
	 widgetbox(div,g_slider),
    fig
)

fig.background_fill_alpha = 0.5 
fig.background_fill_color = 'white'
fig.grid.grid_line_alpha = 0 
fig.yaxis.major_label_text_alpha = 0
fig.xaxis.major_label_text_alpha = 0 
fig.yaxis.major_tick_line_alpha = 0 
fig.xaxis.major_tick_line_alpha = 0 
fig.yaxis.minor_tick_line_alpha = 0 
fig.xaxis.minor_tick_line_alpha = 0 
fig.yaxis.axis_line_alpha  =0
fig.xaxis.axis_line_alpha  =0
fig.yaxis.axis_label_text_font_size = '20px'
fig.xaxis.axis_label_text_font_size = '20px'
fig.border_fill_color = 'white'
fig.border_fill_alpha = 0.5
output_file("sample.html", title="Sample example")

show(layout)

js, tag = autoload_static(layout, CDN, "js/OTHG.js")
js_file = open("/Users/natashabatalha/Documents/picaso_derivations/js/OTHG.js",'w')
js_file.write(js)
print(tag)
js_file.close()