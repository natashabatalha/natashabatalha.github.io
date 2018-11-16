import numpy as np
from bokeh.plotting import *
from bokeh.palettes import Spectral10, Viridis3,Colorblind8
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import column, widgetbox
from bokeh.models import CustomJS, Slider,Div

from bokeh.resources import CDN
from bokeh.embed import autoload_static



def phasefun(g, azimuths):
    return (1.0-g**2)/np.sqrt(1+ g**2 - 2.0*g * np.cos(azimuths))**3.0


fig = Figure(width = 600, height = 300,y_range=[-4,4] ,x_range=[-4,20], #x_range=[0,np.pi],y_range=[1e-1,1e3],y_axis_type='log', #
    y_axis_label='Light from here')
fige = Figure(width = 600, height = 200 ,x_range=[0,np.pi], y_axis_type='log',y_range=[1e-4,1e5], #x_range=[0,np.pi],y_range=[1e-1,1e3],y_axis_type='log', #
    y_axis_label='Error')
g = 0.6
azimuths = np.linspace(0, 2 * np.pi, 10000)
#ranges = np.array([2, 4, 6, 8])
for g in list(np.linspace(0,0.9,10))+[0]:
    gf = g
    gb = -g/2
    f = 1-gb**2

    phase = f*phasefun(gf,azimuths) + (1-f)*phasefun(gb,azimuths)

    xx = phase*np.cos(azimuths)#azimuths#
    yy = phase*np.sin(azimuths)#phase#

    if g ==0:
        x = xx
        y = yy

    #fig.line(xx,yy, line_width =3, alpha=0.3, color='grey')
##RAYLEIGH############################################################
phase = 0.75*(1 + np.cos(azimuths)**2.0)
xr = phase*np.cos(azimuths)#azimuths#
yr = phase*np.sin(azimuths)
fig.line(xr,yr, line_width =6, alpha=0.5, color=Colorblind8[6],legend='Rayleigh')
#######################################################################

##N=1 LEGENDRE######################################################
phase =1 + 3.0 * g * np.cos(azimuths)
x1 = phase*np.cos(azimuths)#azimuths#
y1 = phase*np.sin(azimuths)
#fig.line(x1,y1, line_width =3, alpha=0.5, color='green') #below
#######################################################################

##N=2 LEGENDRE######################################################
g2 = 0.5
phase =1 + 3.0 * g * np.cos(azimuths) + 0.5*g2*(3.0*np.cos(azimuths)**2.0 - 1.0)
x2 = phase*np.cos(azimuths)#azimuths#
y2 = phase*np.sin(azimuths)
#fig.line(x2,y2, line_width =3, alpha=0.5, color='red')#below


##N=2 LEGENDRE DELTA######################################################
g2 = 0.5
g = g/(1+g)
phase =1 + 3.0 * g * np.cos(azimuths) + 0.5*g2*(3.0*np.cos(azimuths)**2.0 - 1.0)
x3 = phase*np.cos(azimuths)#azimuths#
y3 = phase*np.sin(azimuths)
#fig.line(x2,y2, line_width =3, alpha=0.5, color='red')#below
#######################################################################
ey1 = abs(y-y1)/y
ey2 = abs(y-y2)/y
ey3 = abs(y-y3)/y

source = ColumnDataSource(data=dict(x=x, y=y, az = azimuths, x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, ey1=ey1,ey2=ey2,ey3=ey3))
#polar
fig.line('x','y', line_width =6, alpha=0.5, color=Colorblind8[-1],source=source,legend='TTGH')
fig.line('x1','y1', line_width =6, alpha=0.5, color=Colorblind8[0],source=source,legend='Legendre,N=1')
fig.line('x2','y2', line_width =6, alpha=0.5, color=Colorblind8[3],source=source,legend='Legendre,N=2')
fig.line('x3','y3', line_width =6, alpha=0.5, color=Colorblind8[5],source=source,legend='Legendre, N=2, d-Scale')

#error
fige.line('az','ey1', line_width =6, alpha=0.5, color=Colorblind8[0],source=source)
fige.line('az','ey2', line_width =6, alpha=0.5, color=Colorblind8[3],source=source)
fige.line('az','ey3', line_width =6, alpha=0.5, color=Colorblind8[5],source=source)

callback = CustomJS(args=dict(source=source), code="""
    function phasefun(g,az){
        return (1.0-Math.pow(g,2))/Math.pow(Math.sqrt(1.0+ Math.pow(g,2) - 2.0 *g * Math.cos(az)),3.0);
    }
    var data = source.data;
    var g = g.value;

    var x = data['x'];
    var y = data['y'];
    var x1 = data['x1'];
    var y1 = data['y1'];
    var x2 = data['x2'];
    var y2 = data['y2'];
    var x3 = data['x3'];
    var y3 = data['y3'];
    var az = data['az'];

    var ey1 = data['ey1'];
    var ey2 = data['ey2'];
    var ey3 = data['ey3'];

    var phase = 0 ;
    var gf = g;
    var gb = -1*g/2;
    var f = 1 - Math.pow(gb,2);

    for (var i = 0; i < x.length; i++) {
        phase = f*phasefun(gf,az[i]) + (1-f)*phasefun(gb,az[i]);
        x[i] = phase*Math.cos(az[i]);
        y[i] = phase*Math.sin(az[i]);
        phase = 1 + 3.0 * g *Math.cos(az[i]);
        x1[i] = phase*Math.cos(az[i]);
        y1[i] = phase*Math.sin(az[i]);
        ey1[i] = Math.abs(ey1[i] - y[i])/y[i];
        phase = 1 + 3.0 * g * Math.cos(az[i]) + 0.5*0.5*(3.0*Math.cos(az[i])**2.0 - 1.0);
        x2[i] = phase*Math.cos(az[i]);
        y2[i] = phase*Math.sin(az[i]);
        ey2[i] = Math.abs(ey2[i] - y[i])/y[i];
        phase = 1 + 3.0 * g/(1+g) * Math.cos(az[i]) + 0.5*0.5*(3.0*Math.cos(az[i])**2.0 - 1.0);
        x3[i] = phase*Math.cos(az[i]);
        y3[i] = phase*Math.sin(az[i]);
        ey3[i] = Math.abs(ey3[i] - y[i])/y[i];
    }
    source.change.emit();
""")

g_slider = Slider(start=0, end=1, value=0, step=.1,
                     callback=callback)

callback.args["g"] = g_slider

div = Div(text="""<big><b>Assymetry Factor, <em>g</em></b></big>""")

layout = column(
     widgetbox(div,g_slider),
    fig,fige
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
fig.legend.label_text_font_size = '20px'
fig.border_fill_color = 'white'
fig.border_fill_alpha = 0.5
fig.legend.background_fill_color = "white"
fig.legend.background_fill_alpha = 0

fige.background_fill_alpha = 0.5 
fige.background_fill_color = 'white'
fige.grid.grid_line_alpha = 0 
#fige.yaxis.major_label_text_alpha = 0
fige.xaxis.major_label_text_alpha = 0 
fige.yaxis.major_tick_line_alpha = 0 
fige.xaxis.major_tick_line_alpha = 0 
fige.yaxis.minor_tick_line_alpha = 0 
fige.xaxis.minor_tick_line_alpha = 0 
fige.yaxis.axis_line_alpha  =0
fige.xaxis.axis_line_alpha  =0
fige.yaxis.axis_label_text_font_size = '20px'
fige.xaxis.axis_label_text_font_size = '20px'
fige.border_fill_color = 'white'
fige.border_fill_alpha = 0.5


output_file("sample.html", title="Sample example")

show(layout)

js, tag = autoload_static(layout, CDN, "js/multi_phase.js")
js_file = open("/Users/natashabatalha/Documents/picaso_derivations/js/multi_phase.js",'w')
js_file.write(js)
print(tag)
js_file.close()