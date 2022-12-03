import re
from datetime import datetime
from flask import Flask
from flask import render_template as rt


app = Flask(__name__)
@app.route("/")
def home():
    return rt("home.html")
@app.route('/hello/<name>')
def hello_there(name = None):
    return rt("hello_there.html", name=name, date=datetime.now())

@app.route('/api/data')
def get_data():
    return app.send_static_file("data.json")
@app.route("/about/")
def about():
    return rt("about.html")
@app.route("/contact/")
def contact():
    return rt("contact.html") 

from flask_plots import Plots
import matplotlib
from matplotlib.figure import Figure
from flask import render_template_string
plots=Plots(app)
@app.route('/plot2takeover')
def bar():
    countries = ["Argentina", "Brazil", "columbia", "Chile"]
    peoples = [14, 40,16,24]
    fig = Figure()
    ax = fig.subplots()
    ax = plots.bar(fig, countries, peoples)
    ax.set_title("Set the bar high chart")
    data = plots.get_data(fig)
    return render_template_string(
        """
        {% from 'plots/utils.html' import render_img %}
        {{ render_img(data=data, alt_img='my_img')}}
        """,
        data=data
        )
    
from sympy.integrals.transforms import inverse_laplace_transform
from sympy.physics.control.control_plots import ramp_response_plot as rrp
from sympy.physics.control.control_plots import step_response_plot as srp

from sympy.physics.control.lti import TransferFunction as TF
from sympy.abc import s
import numpy as np    
@app.route('/damperPI')
def transfer():
    
    f_t = np.linspace(0.0001, 124.545, num=5)
    Ki = 30;
    Kp = np.linspace(18.5, 273, num=5)
    i = f_t.size

    for l in range(i-1):
        X_s=TF(f_t[l], 1-s,s)
        H_s = TF(Kp[l]*s+30, s, s)
        Theta_s=TF(f_t[l]*(Kp[l]*s+30)/(s-s**2), 1+(f_t[l]*(Kp[l]*s+30)/(s-s**2)), s)
        #pzp(Theta_s)
        #print(Theta_s.is_stable())
        #print(Theta_s)
        rrp(Theta_s)
        
        Error_s = TF(1, 1+(f_t[l]*(Kp[l]*s+30)/(s-s**2)),s)
        #print(Error_s)
        rrp(Error_s)
        l+1
    fig2=Figure()
    data=Plots.get_data(fig2)
    return render_template_string(
        """{% from 'plots/utils.html' import render_img %}
        {{ render_img(data=data, alt_img='my_img')}}
        """,
        data=data
        )
    

    
