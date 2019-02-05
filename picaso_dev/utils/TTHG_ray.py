import numpy as np
from bokeh.plotting import *
from bokeh.palettes import Spectral10, Viridis3
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import column, widgetbox,row
from bokeh.models import CustomJS, Slider,Div

from bokeh.resources import CDN
from bokeh.embed import autoload_static


def phasefun(g, azimuths):
    return (1.0-g**2)/np.sqrt(1+ g**2 - 2.0*g * np.cos(azimuths))**3.0


fig = Figure(y_range=[-4,4] ,x_range=[-2,20], width = 500, height = 200,
    y_axis_label='Light from here',x_axis_label='Back Scattering <-----> Forward Scattering')
g = 0.6
azimuths = np.linspace(0, 2 * np.pi, 10000)
#ranges = np.array([2, 4, 6, 8])
for g in list(np.linspace(0,0.9,10))+[0]:
    gf = g
    gb = -g/2
    f = 1-gb**2

    phase_noray = f*phasefun(gf,azimuths) + (1-f)*phasefun(gb,azimuths) #+ 0.5
    phase_ray = f*phasefun(gf,azimuths) + (1-f)*phasefun(gb,azimuths) + 0.5

    xx_noray = phase_noray*np.cos(azimuths)
    yy_noray = phase_noray*np.sin(azimuths)
    if g ==0:
        x_noray = xx_noray
        y_noray = yy_noray
    xx_ray = phase_ray*np.cos(azimuths)
    yy_ray = phase_ray*np.sin(azimuths)
    if g ==0:
        x_ray = xx_ray
        y_ray = yy_ray

    fig.line(xx_ray,yy_ray, line_width =3, alpha=0.3, color='grey')



source = ColumnDataSource(data=dict(x_ray=x_ray, y_ray=y_ray,x_noray=x_noray, y_noray=y_noray, az = azimuths))

fig.line('x_ray','y_ray', line_width =5, alpha=0.8, color='pink',source=source,legend='TTHG w/ Rayleigh')
fig.line('x_noray','y_noray', line_width =5, alpha=0.8, color=Viridis3[1],source=source,legend='TTHG')

callback = CustomJS(args=dict(source=source), code="""
    function phasefun(g,az){
        return (1.0-Math.pow(g,2))/Math.pow(Math.sqrt(1.0+ Math.pow(g,2) - 2.0 *g * Math.cos(az)),3.0);
    }

    var data = source.data;
    var g = g.value;
    var x_noray = data['x_noray'];
    var y_noray = data['y_noray'];
    var x_ray = data['x_ray'];
    var y_ray = data['y_ray'];
    var az = data['az'];
    var phase_noray = 0 ;
    var phase_ray = 0 ;
    var gf = g;
    var gb = -1*g/2;
    var f = 1 - Math.pow(gb,2);

    for (var i = 0; i < x_ray.length; i++) {
        phase_ray = f*phasefun(gf,az[i]) + (1-f)*phasefun(gb,az[i]) + 0.5;
        x_ray[i] = phase_ray*Math.cos(az[i]);
        y_ray[i] = phase_ray*Math.sin(az[i]);
        phase_noray = f*phasefun(gf,az[i]) + (1-f)*phasefun(gb,az[i]);
        x_noray[i] = phase_noray*Math.cos(az[i]);
        y_noray[i] = phase_noray*Math.sin(az[i]);
    }
    source.change.emit();
""")

g_slider = Slider(start=0, end=1, value=0, step=.01,
                     callback=callback)

callback.args["g"] = g_slider

div = Div(text="""<big><b>gf:</b></big>""")

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

fig.legend.label_text_font_size = '16px'
fig.legend.background_fill_color = "white"
fig.legend.background_fill_alpha = 0


output_file("sample.html", title="Sample example")

#show(layout)

js, tag = autoload_static(layout, CDN, "js/TTHG.js")
js_file = open("/Users/natashabatalha/Documents/natashabatalha.github.io/picaso/js/TTHG.js",'w')
js_file.write(js)
print(tag)
js_file.close()