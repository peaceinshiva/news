from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import pandas as pd
import smtplib

app = Flask(__name__)

UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['GET', 'POST'])
def data():
    if (request.method == "POST"):
        file1 = request.files['myfile']
        file2 = request.files['template']
    
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file1.filename)))
        file2.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file2.filename)))
    
           
        if file1.filename.endswith(".csv") and file2.filename.endswith(".txt"):
            data =pd.read_csv(f"static/{file1.filename}",delimiter=',')
            for i in data.index:
                na=data['Name'][i]
                em=data['Email'][i]
                co=data['Course'][i]
                
            m = open(f"static/{file2.filename}", "r")
            mal =(f"Thanks {na} for Enrolled of {co}")
            mal=m.read()
            server=smtplib.SMTP_SSL('smtp.gmail.com',465)
            server.login("shivatechnogroup@gmail.com","fmpwrRDNBsQ59.X")
            server.sendmail("shivatechnogroup@gmail.com",em,mal.format(na,co))
        else:
            return render_template('upload.html', submit='Your file is not valid')
        
    return render_template('upload.html', submit='Successful submited your file')


if __name__ == '__main__':
    app.run()