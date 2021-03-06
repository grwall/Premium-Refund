#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 12 15:58:13 2020

@author: marcus
"""
from flask import Flask, request, render_template, jsonify
from flask_restful import Resource, Api
from datetime import datetime
import calculator as cal
import SQL
app = Flask(__name__)
api = Api(app)


def compute(request_date,prd_grp_fin,policy_id, issue_date=None, end_date=None, start_date=None, premium=None, commission=None):
   try:
       if (premium==None) or (issue_date==None) or (end_date==None) or (start_date==None) or (commission==None):
           issue_date, end_date, start_date, premium, commission = SQL.retrieve(policy_id)
       else:
           issue_date = datetime.strptime(issue_date,'%Y-%m-%d') 
           start_date = datetime.strptime(start_date,'%Y-%m-%d')  
           end_date = datetime.strptime(end_date,'%Y-%m-%d') 
           premium = float(premium)
           commission = float(commission)

       if request_date>end_date:
           msg='Sorry, your cancellation requested date is after the policy has expired! No Premium is refunded'
       elif request_date<issue_date:
           msg='You cannot request a refund prior to the policy is issued' 
       else:    
            earned = cal.function(issue_date,start_date,end_date,request_date,prd_grp_fin)
            Premium_refunded = round(premium*(1-earned),2)
            returned_commission = round(commission *(1-earned),2)
            
            if Premium_refunded == round(premium,2):
                refund_type = 'FULL REFUND'
            elif Premium_refunded == 0:
                refund_type = 'NO REFUND'
            else :
                refund_type = 'PARTIAL REFUND'
            
            msg = {'POLICY_ID'          : policy_id,
                   'ISSUE_DATE'         : issue_date,
                   'START_DATE'         : start_date,
                   'END_DATE'           : end_date,
                   'REQUEST_DATE'       : request_date,
                   'CAL_METHOD'         : prd_grp_fin,
                   'ORIGINAL_PREMIUM'   : premium,
                   'COMMISSION'         : commission,
                   'REFUND_PERCENT'     : (1-earned),
                   'PREMIUM_REFUND'     : Premium_refunded,
                   'RETURNED_COMMISSION': returned_commission, 
                   'REFUND_TYPE'        : refund_type,
                   'PROCESS_DATE'       : datetime.now()
                    }
            
   except:
       msg = SQL.retrieve(policy_id)  
   return msg
        

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate',methods=['POST'])
def calculate():
  
    policy_id = request.form['policy_id']
    premium = request.form['premium'] or None
    commission = request.form['commission'] or None
    issue_date = request.form['issue_date'] or None
    start_date = request.form['start_date'] or None
    end_date = request.form['end_date'] or None
    request_date = datetime.strptime(request.form['request_date'],'%Y-%m-%d')
    prd_grp_fin = request.form['prd_grp_fin']
            
    msg = compute(request_date,prd_grp_fin,policy_id, issue_date=issue_date, end_date=end_date, start_date=start_date, premium=premium, commission=commission)
    
    try:
        html =  render_template('index.html', premium_refund = 'Premium refunded : ${}'.format(msg['PREMIUM_REFUND']),
                               policy_id        = 'Policy id : %s' %(msg['POLICY_ID']),
                               original_premium = 'Original Premium : ${}'.format(msg['ORIGINAL_PREMIUM']),
                               commission = 'Commision : ${}'.format(msg['COMMISSION']),

                               refund_percent      = 'Percentage refund : {:.0%}'.format(msg['REFUND_PERCENT']),
                               returned_commission = 'Return commission : ${}'.format(msg['RETURNED_COMMISSION']),
                               refund_type         = 'Refund type : %s' %(msg['REFUND_TYPE']),
                               
                               issue_date       = 'Issue date: %s' %(msg['ISSUE_DATE']),
                               start_date       = 'Start date: %s' %(msg['START_DATE']),
                               end_date         = 'End date: %s' %(msg['END_DATE']),
                               request_date     = 'Request date: %s' %(msg['REQUEST_DATE']),
                               prd_grp_fin      = 'Calculation method : %s' %(msg['CAL_METHOD']),
                               process_date     = 'Process date: %s' %(msg['PROCESS_DATE']),
                               )
        SQL.injection(msg)
    except:
        html = render_template('index.html', error=msg)
    
    return html


class calculate_api(Resource):
    def post(self):
        data = request.get_json(force=True)
        policy_id = data['policy_id']
        premium = data['premium']
        commission = data['commission'] 
        issue_date = data['issue_date'] 
        start_date = data['start_date'] 
        end_date = data['end_date'] 
        request_date = datetime.strptime(data['request_date'],'%Y-%m-%d')
        prd_grp_fin = data['prd_grp_fin']
        
        msg = compute(request_date,prd_grp_fin,policy_id, issue_date=issue_date, end_date=end_date, start_date=start_date, premium=premium, commission=commission)
        SQL.injection(msg)
        
        return jsonify(msg)

api.add_resource(calculate_api, '/calculate_api')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False, port=5000)
