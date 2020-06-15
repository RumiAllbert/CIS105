from imageHanlder import checkImage, createImage
from form import SearchForm
from flask import Flask, render_template, url_for, flash, redirect, request, send_file, session
from forms import RegistrationForm, LoginForm
import os
import pyqrcode, getpass
from pyqrcode import QRCode
import pyqrcode
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/qrcodecreator")
def qrcode():
    return render_template('qrcodecreator.html')

@app.route("/converter", methods=['POST'])
def convert():
    qrvalue = request.form['test']
    QR = pyqrcode.create(qrvalue) 
    myfile = os.path.join(app.static_folder, "qr.png")
    QR.png(myfile, scale=10)
    return render_template('converter.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/covid", methods=['GET', 'POST'])
def covid():
    form = SearchForm()
    if form.validate_on_submit():
        if (not checkImage(form.state.data)):
            createImage(form.state.data)
        session['image'] = form.state.data + "_" + str(datetime.date.today())
        return redirect(url_for('result'))

    return render_template('search.html', form=form)

@app.route("/result")
def result():
    return render_template('result.html', imageSrc = "/getGraph")

@app.route("/getGraph")
def getGraph():
    filePath = "./image/" + session['image'] + ".png"
    return send_file(filePath, mimetype='image/png')




@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
