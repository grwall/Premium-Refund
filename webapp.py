#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:58:13 2020

@author: marcus
"""

from flask import Flask, request, render_template
from datetime import datetime
import calculator as cal

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate',methods=['POST'])
def calculate():
    '''
    For rendering results on HTML GUI
    '''
    premium = float(request.form['premium'])
    issue_date = datetime.strptime(request.form['issue_date'],'%Y-%m-%d')
    start_date = datetime.strptime(request.form['start_date'],'%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'],'%Y-%m-%d')
    request_date = datetime.strptime(request.form['request_date'],'%Y-%m-%d')
    
    earned = cal.function(issue_date,start_date,end_date,request_date)
    refund = round(premium *(1-earned),2)


    return render_template('index.html', refund_amount='Eligible Refund Amount $ {}'.format(refund))
    #return print(int_features)


if __name__ == "__main__":
    app.run(debug=True)