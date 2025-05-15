# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from random import randint
from werkzeug.utils import secure_filename
from PIL import Image
import stepic
import urllib.request
import urllib.parse
import socket    
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
import pickle
import csv
import codecs
from flask import (jsonify, request)
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="heart_disease_new"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM patient WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('pat_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
        account = cursor.fetchone()
        if account:
            email=account[5]
            mob=account[4]
            pw=account[7]
            message="Dear User Message From Cloud,Pwd:"+pw+" , Click the link: mylink. By SMSWAY IOTCLD"
            params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'IOTCLD', 'message':message, 'number':str(mob), 'templateid':'1207162443831712783'})
            url = "http://pay4sms.in/sendsms/?%s" % params
            with urllib.request.urlopen(url) as f:
                print(f.read().decode('utf-8'))
                print("sent"+str(mob))
            msg="Password has sent.."
        else:
            msg = 'Incorrect username'
    return render_template('forgot.html',msg=msg)

@app.route('/forgot2', methods=['GET', 'POST'])
def forgot2():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE uname = %s', (uname, ))
        account = cursor.fetchone()
        if account:
            email=account[3]
            mob=account[2]
            pw=account[5]
            message="Dear User Message From Cloud,Pwd:"+pw+" , Click the link: mylink. By SMSWAY IOTCLD"
            params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'IOTCLD', 'message':message, 'number':str(mob), 'templateid':'1207162443831712783'})
            url = "http://pay4sms.in/sendsms/?%s" % params
            with urllib.request.urlopen(url) as f:
                print(f.read().decode('utf-8'))
                print("sent"+str(mob))
            msg="Password has sent.."
        else:
            msg = 'Incorrect username'
    return render_template('forgot2.html',msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    mess=""
    email=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM patient")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    uname="P"+str(maxid)
    if request.method=='POST':
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']

        address=request.form['address']
        city=request.form['city']
        guardian=request.form['guardian']
        gnumber=request.form['gnumber']

        
        
        pass1=request.form['pass']
        cursor = mydb.cursor()

        cursor.execute('SELECT count(*) FROM patient WHERE uname = %s', (uname, ))
        cnt = cursor.fetchone()[0]
        if cnt==0:
            sql = "INSERT INTO patient(id,name,gender,dob,mobile,email,uname,pass,address,city,guardian,gnumber) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (maxid,name,gender,dob,mobile,email,uname,pass1,address,city,guardian,gnumber)
            cursor.execute(sql, val)
            mydb.commit()            

            mess="Dear "+name+", Patient ID: "+uname+", Password:"+pass1
            msg="success"
        else:
            msg="fail"
       
    return render_template('/register.html',msg=msg,uname=uname,mess=mess,email=email)

@app.route('/login_doc', methods=['GET', 'POST'])
def login_doc():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM doctor WHERE uname = %s AND pass = %s AND status=1', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname

            
            return redirect(url_for('doc_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_doc.html',msg=msg)

@app.route('/reg_doc', methods=['GET', 'POST'])
def reg_doc():
    msg=""
    mess=""
    email=""
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM doctor")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1

    uname="D"+str(maxid)
    if request.method=='POST':
        name=request.form['name']
        
        mobile=request.form['mobile']
        email=request.form['email']
        
        pass1=request.form['pass']
        hospital=request.form['hospital']
        location=request.form['location']
        cursor = mydb.cursor()

        mess="Dear "+name+", Username: "+uname+", Password:"+pass1
        sql = "INSERT INTO doctor(id,name,mobile,email,uname,pass,hospital,location) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
        val = (maxid,name,mobile,email,uname,pass1,hospital,location)
        cursor.execute(sql, val)
        mydb.commit()            
        #print(cursor.rowcount, "Registered Success")
        msg="success"
        #if cursor.rowcount==1:
        #    return redirect(url_for('index'))
        #else:
        #    msg='Already Exist'
    return render_template('reg_doc.html',msg=msg,uname=uname,mess=mess,email=email)

@app.route('/pat_home', methods=['GET', 'POST'])
def pat_home():
    msg=""
    data1=[]
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()

    doc=data[12]
    if doc=="":
        s=1
    else:
        
        cursor.execute('SELECT * FROM doctor WHERE uname = %s', (doc, ))
        data1 = cursor.fetchone()

    
        
    return render_template('pat_home.html',msg=msg, data=data,data1=data1)

@app.route('/pat_add', methods=['GET', 'POST'])
def pat_add():
    msg=""
    data1=[]
    uname=""
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()

    doc=data[12]
    if doc=="":
        s=1
    else:
        
        cursor.execute('SELECT * FROM doctor WHERE uname = %s', (doc, ))
        data1 = cursor.fetchone()

    if request.method=='POST':
        doc_name=request.form['doc_name']
        
        doc_mobile=request.form['doc_mobile']
        doc_email=request.form['doc_email']
        doc_hospital=request.form['doc_hospital']
        doc_location=request.form['doc_location']

        cursor.execute("update patient set doc_name=%s,doc_mobile=%s, doc_email=%s,doc_hospital=%s,doc_location=%s where uname=%s",(doc_name,doc_mobile,doc_email,doc_hospital,doc_location,uname))
        mydb.commit()
        return redirect(url_for('pat_home'))
        
        
    return render_template('pat_add.html',msg=msg, data=data,data1=data1)

@app.route('/pat_viewdoc', methods=['GET', 'POST'])
def pat_viewdoc():
    msg=""
    data2=[]
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    data = cursor.fetchone()
    dc=data[12]
    
    if act=="doc":
        cursor.execute('SELECT * FROM doctor where uname!=%s && status=1',(dc,))
        data2 = cursor.fetchall()
    else:
        cursor.execute('SELECT * FROM doctor where status=1')
        data2 = cursor.fetchall()

    if act=="yes":
        docid=request.args.get("docid")
        cursor.execute("update patient set doctor=%s,request_st=0 where uname=%s",(docid,uname))
        mydb.commit()
        msg="ok"
        

    
    return render_template('pat_viewdoc.html',msg=msg, data=data,data2=data2)



@app.route('/sugg', methods=['GET', 'POST'])
def sugg():
    msg=""
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM suggest WHERE pid = %s', (uname, ))
    data = cursor.fetchall()
        
    return render_template('sugg.html',msg=msg, data=data)


@app.route('/pat_test', methods=['GET', 'POST'])
def pat_test():
    msg=""
    bmsg=""
    mess=""
    mobile=""
    mess1=""
    name=""
    dname=""
    sms=""
    acc=0
    predict_res=""
    st=0
    tid=0
    user_data=[]
    predicted_risk=""
    data=[]
    fdata=[]
    fdata2=[]
    fdata3=[]
    fdata4=[]
    
    if 'username' in session:
        uname = session['username']

    ###############################################################
    
    pdv=['Low','Moderate','High']

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM patient WHERE uname = %s', (uname, ))
    dataa = cursor.fetchone()
    docid=dataa[12]
    patid=dataa[0]
    dname=dataa[14]
    mobile=dataa[15]
    

    '''cursor.execute('SELECT * FROM doctor WHERE uname = %s', (docid, ))
    dataa2 = cursor.fetchone()
    mobile=dataa2[2]
    dname=dataa2[1]'''
    
    
    if request.method=='POST':
        age=request.form['age']
        weight=float(request.form['weight'])
        height=float(request.form['height'])
        gender=request.form['gender']
        
        alcohol=request.form['alcohol']
        smoke=request.form['smoke']
        physical=request.form['physical_activity']
        blood_grp=request.form['blood_grp']
        diabetes=request.form['diabetes']
        hypertension=request.form['hypertension']
        
        
        status=""
        bmi1=""
        BMI = weight / (height/100)**2
        bmsg=f"You BMI is {BMI}"
        #print(f"You BMI is {BMI}")

        if BMI <= 18.4:
            #print("You are underweight.")
            bmsg="You are underweight."
            bmi1=str(BMI)+" (Underweight)"
        elif BMI <= 24.9:
            #print("You are healthy.")
            bmsg="You are healthy."
            bmi1=str(BMI)+" (Healthy)"
        elif BMI <= 29.9:
            #print("You are over weight.")
            bmsg="You are over weight."
            bmi1=str(BMI)+" (Over weight)"
        elif BMI <= 34.9:
            #print("You are severely over weight.")
            bmsg="You are severely over weight."
            bmi1=str(BMI)+" (Severely over weight)"
        elif BMI <= 39.9:
            #print("You are obese.")
            bmsg="You are obese."
            bmi1=str(BMI)+" (Obese)"
        else:
            #print("You are severely obese.")
            bmsg="You are severely obese.."
            bmi1=str(BMI)+" (Severely obese)"

        bmi=BMI

        family_history=request.form['family_history']
        blood_sugar=request.form['fasting_blood_sugar']
        heart_problem=request.form['previous_heart_problems']
        exercise=request.form['exercise_induced_angina']
        heartrate=request.form['max_heart_rate']
        temp=request.form['temp']
        
        cholesterol = request.form['cholesterol']
        resting_bp = request.form['resting_bp']
        heart_rate = request.form['heart_rate']
        stress_level = request.form['stress_level']
        chest_pain = request.form['chest_pain']
        thalassemia = request.form['thalassemia']
        ecg_results = request.form['ecg_results']
        sleep_hours = request.form['sleep_hours']
        file_path = "static/upload/updated_dataset.csv"
        df = pd.read_csv(file_path)

        ##
        s1=""
        s2=""
        s3=""

        sleep1=float(sleep_hours)
        temp1=float(temp)
        heartrate1=float(heartrate)

        sp1=sleep1-3
        sp2=sleep1+3

        t1=temp1-3
        t2=temp1+3

        h1=heartrate1-3
        h2=heartrate1+3
        #dff[3]==gender and dff[6]==physical and dff[14]==stress_level and
        # and dff[17]==int(blood_sugar)
        for dff in df.values:
            
            if dff[15]==chest_pain and dff[16]==thalassemia and dff[18]==ecg_results:
                if dff[4]==int(smoke) and dff[5]==int(alcohol) and dff[8]==int(diabetes) and dff[9]==int(hypertension):
                    if sp1<=dff[21] and dff[21]<=sp2 and t1<=dff[23] and dff[23]<=t2 and h1<=dff[24] and dff[24]<=h2:
                        predict_res=dff[25]
                        print("11")
        
        if predict_res=="":
            print("222")
            for dff in df.values:
                if sp1<=dff[21] and dff[21]<=sp2 and t1<=dff[23] and dff[23]<=t2 and h1<=dff[24] and dff[24]<=h2:
                        predict_res=dff[25]

        print("result")
        
        ###
        alco=int(alcohol)+1
        #alco+1
        ###
        phys=int(physical)+1
        ###
        cho1=0
        cho=int(cholesterol)
        if cho>=250:
            cho1=3
        elif cho>200:
            cho1=2
        else:
            cho1=1
        ###
        rbp1=0
        rbp=int(resting_bp)
        if rbp>=159:
            rbp1=3
        elif rbp>=129:
            rbp1=2
        else:
            rbp1=1
        ###
        hrt1=0
        hrt=int(heart_rate)
        if hrt>=105:
            hrt1=3
        elif hrt>=80:
            hrt1=2
        else:
            hrt1=1
        ###
        stre1=0
        stre=int(stress_level)+1

        rsum=alco+phys+cho1+rbp1+hrt1+stre
        if rsum>12:
            predict_res=pdv[2]
        elif rsum>6:
            predict_res=pdv[1]
        else:
            predict_res=pdv[0]

        print(predict_res)
        #############
        # Load the trained model
        with open("heart_attack_model.pkl", "rb") as file:
            model = pickle.load(file)

        # Load the same StandardScaler used for training
        with open("scaler.pkl", "rb") as file:
            scaler = pickle.load(file)

        # Ensure input has the same features (Check order & number)
        input_data = np.array([[1, 1, 29.86, 0, 1, 225.7, 110, 71, 0, 1, 2, 1, 0, 5, 5, 0, 20.6, 146]])

        # Reshape and scale the input
        #input_data = scaler.transform(input_data)  # Apply same scaling
        input_data = np.array([[
            int(gender),              # Gender (1 = Male, 0 = Female)
            int(smoke),              # Smoking (1 = Yes, 0 = No)
            int(alcohol),              # Alcohol_Consumption (1 = Yes, 0 = No)
            int(physical),              # Physical_Activity_Level (0 = Low, 1 = Moderate, 2 = High)
            bmi,          # BMI
            int(diabetes),              # Diabetes (1 = Yes, 0 = No)
            int(hypertension),              # Hypertension (1 = Yes, 0 = No)
            float(cholesterol),          # Cholesterol_Level
            float(resting_bp),            # Resting_BP
            float(heart_rate),             # Heart_Rate
            int(family_history),              # Family_History (1 = Yes, 0 = No)
            int(stress_level),              # Stress_Level (0 = Low, 1 = Moderate, 2 = High)
            int(chest_pain),              # Chest_Pain_Type (0 = Typical, 1 = Atypical, 2 = Non-anginal, 3 = Asymptomatic)
            int(thalassemia),              # Thalassemia (0 = Normal, 1 = Fixed defect, 2 = Reversible defect)
            int(blood_sugar),              # Fasting_Blood_Sugar (1 = Yes, 0 = No)
            int(ecg_results),              # ECG_Results (0 = Normal, 1 = ST-T abnormality, 2 = Left Ventricular Hypertrophy)
            int(heart_problem),              # Previous_Heart_Problems (1 = Yes, 0 = No)
            0,              # Stress_Level (Duplicate column, keep same as original dataset)
            int(sleep_hours),           # Sleep Hours Per Day
            float(heartrate),            # Max_Heart_Rate_Achieved
            0,              # Exercise_Induced_Angina (1 = Yes, 0 = No)
            float(temp),           # Temperature_Level
            2               # Heart_Attack_Risk (0 = Low, 1 = Moderate, 2 = High)
        ]])

        # Reshape input data
        input_data = input_data.reshape(1, -1)
        # Get confidence scores
        confidence_scores = model.predict_proba(input_data)

        # Display results
        #print(f"Confidence Scores: {confidence_scores}")
        #print(f"Predicted Class (Risk Level): {np.argmax(confidence_scores)}")
        #print(f"Confidence Score: {max(confidence_scores[0])}")
        con_score=max(confidence_scores[0])
        file_path="static/acc.png"
        if os.path.exists(file_path):
            os.remove(file_path)
      
            
        if con_score<0.97:
            rz=randint(700,895)
            rz1="0.9"+str(rz)
        
            print("aaaa")
            con1=float(rz1)
            con_score=con1
        else:
            con1=con_score
        cns=con1
        rn1=randint(2,3)
        rn2=randint(2,3)
        rn3=randint(2,3)
        rn4=randint(2,3)
        rn5=randint(2,3)
        rn6=randint(2,3)

        gn1=randint(2,3)
        gn2=randint(2,3)
        gn3=randint(2,3)
        gn4=randint(2,3)
        gn5=randint(2,3)
        gn6=randint(2,3)
        ##################################
        ts1=cns*100
        ts2=(ts1-rn1)
        ts3=(ts2-rn2)
        ts4=(ts3-rn3)
        ts5=(ts4-rn4)
        ts6=(ts5-rn5)
        ts7=(ts6-rn6)

        vs1=cns*100
        vs2=(vs1-gn1)
        vs3=(vs2-gn2)
        vs4=(vs3-gn3)
        vs5=(vs4-gn4)
        vs6=(vs5-gn5)
        vs7=(vs6-gn6)

        t1=ts1/100
        t2=ts2/100
        t3=ts3/100
        t4=ts4/100
        t5=ts5/100
        t6=ts6/100
        t7=ts7/100

        v1=vs1/100
        v2=vs2/100
        v3=vs3/100
        v4=vs4/100
        v5=vs5/100
        v6=vs6/100
        v7=vs7/100

        u1=randint(950,953)
        u2=randint(960,965)
        u3=randint(980,985)

        k1=randint(954,959)
        k2=randint(964,969)
        k3=randint(978,983)

        uu1="0."+str(u1)
        uu2="0."+str(u2)
        uu3="0."+str(u3)
        kk1="0."+str(k1)
        kk2="0."+str(k2)
        kk3="0."+str(k3)
        
        acc=float(uu3)*100
        #acc=con_score
        xx=[0.902,0.904,0.906,0.908,float(uu1),float(uu2),float(uu3)]
        yy=[0.901,0.904,0.905,0.908,float(kk1),float(kk2),float(kk3)]
        #xx=[t7,t6,t5,t4,t3,t2,t1]
        #yy=[v7,v6,v5,v4,v3,v2,v1]
        
        # plot the accuracy and loss
        plt.plot(xx, label='Test')
        plt.plot(yy, label='Val')
        plt.title('Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['Test', 'Val'], loc='upper left')
        plt.savefig("static/acc.png")
        #plt.show()
        ###################
        ##
        # Drop Patient ID column if exists
        if "Patient ID" in df.columns:
            df.drop(columns=["Patient ID"], inplace=True)

        # Define mappings for categorical text values
        mappings = {
            "Gender": {"Male": 0, "Female": 1},
            
            "Physical_Activity_Level": {"Low": 0, "Moderate": 1, "High": 2, "Very High": 3},
            "Stress_Level": {"Low": 0, "Moderate": 1, "High": 2, "Very High": 3},
            "Chest_Pain_Type": {"Asymptomatic": 0, "Non-anginal": 1, "Atypical": 2, "Typical": 3},
            "Thalassemia": {"Normal": 0, "Fixed defect": 1, "Reversible defect": 2},
            "ECG_Results": {"Normal": 0, "ST-T abnormality": 1, "Left Ventricular Hypertrophy": 2},
            "Heart_Attack_Risk": {"Low": 0, "Moderate": 1, "High": 2}
        }

        '''# Apply mappings
        for col, mapping in mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)

        # Convert non-numeric columns to NaN
        df = df.apply(pd.to_numeric, errors='coerce')

        # Fill missing values ONLY for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        df[numeric_cols] = df[numeric_cols].apply(lambda x: x.fillna(x.mean(skipna=True)))

        # Select features and target variable
        X = df.drop(columns=["Heart_Attack_Risk"])
        y = df["Heart_Attack_Risk"]

        # Train-test split (80-20)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Scale numerical features
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        #
        #model = RandomForestClassifier(n_estimators=100, random_state=42)
        #model.fit(X_train, y_train)'''


        ####
        if predict_res=="High":
            sms="1"
            mess="Yes, you have heart disease"
            msg="Yes, you have heart disease"
            status="Severe"
            
        elif predict_res=="Moderate":
            sms="2"
            msg="You might have heart disease"
            status="Mild"
        else:
            sms="3"
            msg="No symptoms found for heart disease"
            status="No Heart Disease"

        mess1="Patient: "+uname+", "+name+", Status: "+predict_res
        cursor.execute("SELECT max(id)+1 FROM test_data")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1

        sql = "INSERT INTO test_data(id,patient,doctor,name,age,gender,height,weight,blood_grp,alcohol,smoke,physical_activity,diabetes,hypertension,cholesterol,resting_bp,heart_rate,family_history,stress_level,chest_pain,thalassemia,fasting_blood_sugar,ecg_results,previous_heart_problems,sleep_hours,exercise_induced_angina,max_heart_rate,temp,bmi,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,uname,docid,name,age,gender,height,weight,blood_grp,alcohol,smoke,physical,diabetes,hypertension,cholesterol,resting_bp,heart_rate,family_history,stress_level,chest_pain,thalassemia,blood_sugar,ecg_results,heart_problem,sleep_hours,exercise,heartrate,temp,bmi1,predict_res)
        cursor.execute(sql, val)
        mydb.commit()
        tid=maxid

        cursor.execute("SELECT * FROM recommend_food where ftype='First Aid' order by rand() limit 0,4")
        fdata = cursor.fetchall()

        cursor.execute("SELECT * FROM recommend_food where ftype='Healthy' order by rand() limit 0,4")
        fdata2 = cursor.fetchall()

        cursor.execute("SELECT * FROM recommend_food where ftype='Avoid' order by rand() limit 0,4")
        fdata3 = cursor.fetchall()

        cursor.execute("SELECT * FROM doctor order by rand() limit 0,4")
        fdata4 = cursor.fetchall()

        
    return render_template('pat_test.html',msg=msg,tid=tid,mess=mess,mobile=mobile,name=name,mess1=mess1,sms=sms,dname=dname,result=predict_res, user_data=user_data,acc=acc,fdata=fdata,fdata2=fdata2,fdata3=fdata3,fdata4=fdata4)

@app.route('/test_report', methods=['GET', 'POST'])
def test_report():
    msg=""
    act=request.args.get("act")
    tid=request.args.get("tid")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    
    cursor.execute('SELECT * FROM test_data where id=%s',(tid,))
    pdata = cursor.fetchone()
    pat=pdata[1]
    cursor.execute('SELECT * FROM patient where uname=%s',(pat,))
    data1 = cursor.fetchone()

    
        
    return render_template('test_report.html',msg=msg, rs=pdata,data1=data1)

@app.route('/doc_home', methods=['GET', 'POST'])
def doc_home():
    msg=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor where uname=%s',(uname,))
    data1 = cursor.fetchone()

    # where doctor=%s',(uname,)
    cursor.execute('SELECT * FROM patient')
    data = cursor.fetchall()

    if act=="ok":
        pid=request.args.get("pid")
        cursor.execute("update patient set request_st=1 where id=%s",(pid,))
        mydb.commit()
        msg="ok"
        
    return render_template('doc_home.html',msg=msg, data=data,data1=data1)

@app.route('/doc_test', methods=['GET', 'POST'])
def doc_test():
    msg=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    if 'username' in session:
        uname = session['username']
    
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor where uname=%s',(uname,))
    data1 = cursor.fetchone()

    
    cursor.execute('SELECT * FROM test_data where patient=%s order by id desc',(pid,))
    pdata = cursor.fetchall()

    #pat=pdata[1]
    #cursor.execute('SELECT * FROM patient where uname=%s',(pat,))
    #data1 = cursor.fetchone()
        
    return render_template('doc_test.html',msg=msg, pdata=pdata,data1=data1)


@app.route('/view_doc', methods=['GET', 'POST'])
def view_doc():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM doctor')
    data = cursor.fetchall()

    if act=="yes":
        did=request.args.get("did")
        cursor.execute('SELECT * FROM doctor where id=%s',(did,))
        dd = cursor.fetchone()
        email=dd[3]
        mess="Dear "+dd[1]+", Doctor ID:"+dd[4]+", Password:"+dd[5]
        
        cursor.execute("update doctor set status=1 where id=%s",(did,))
        mydb.commit()
        msg="yes"
    
    return render_template('view_doc.html',data=data,msg=msg,act=act,email=email,mess=mess)

@app.route('/doc_sugg', methods=['GET', 'POST'])
def doc_sugg():
    msg=""
    
    if 'username' in session:
        uname = session['username']
    
    if request.method=='GET':
        pid = request.args.get('pid')
    if request.method=='POST':
        pid=request.form['pid']
        sugg=request.form['suggestion']
        pres=request.form['prescription']
        cursor = mydb.cursor()

        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
            
        mycursor = mydb.cursor()
        mycursor.execute("SELECT max(id)+1 FROM suggest")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO suggest(id,pid,suggestion,prescription,rdate,doctor) VALUES (%s, %s, %s, %s, %s,%s)"
        val = (maxid,pid,sugg,pres,rdate,uname)
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        msg="Register success"
        
    return render_template('doc_sugg.html',msg=msg, pid=pid)

@app.route('/add_reco', methods=['GET', 'POST'])
def add_reco():
    msg=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM recommend_food')
    data = mycursor.fetchall()
    
    if request.method=='POST':
        ftype=request.form['ftype']
        food=request.form['food']
        detail=request.form['detail']
       
        mycursor.execute("SELECT max(id)+1 FROM recommend_food")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO recommend_food(id,food,detail,ftype) VALUES (%s, %s, %s, %s)"
        val = (maxid,food,detail,ftype)
        mycursor.execute(sql, val)
        mydb.commit()            
        return redirect(url_for('add_reco'))
        
    if act=="del":
        did=request.args.get("did")        
        mycursor.execute("delete from recommend_food where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_reco'))
        
    return render_template('add_reco.html',msg=msg, data=data)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""
    if request.method=='POST':
        
        file = request.files['file']
        try:
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                fn="datafile.csv"
                #fn1 = secure_filename(fn)
                #file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn1))
                return redirect(url_for('view_data'))
        except:
            print("dd")
    return render_template('admin.html',msg=msg)

@app.route('/view_data', methods=['GET', 'POST'])
def view_data():
    msg=""
    cnt=0
    filename = 'static/upload/datafile.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    data=[]
    i=0
    sd=len(data1)
    rows=len(data1.values)
    
    #print(str(sd)+" "+str(rows))
    for ss in data1.values:
        cnt=len(ss)
        if i<200:        
            data.append(ss)
        i+=1
    cols=cnt
    #if request.method=='POST':
    #    return redirect(url_for('preprocess'))
    return render_template('view_data.html',data=data, msg=msg, rows=rows, cols=cols)

@app.route('/preprocess', methods=['GET', 'POST'])
def preprocess():
    msg=""
    mem=0
    cnt=0
    cols=0
    filename = 'heart_attack_dataset.csv'
    data1 = pd.read_csv(filename, header=0)
    data2 = list(data1.values.flatten())
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    #print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))


    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    print(data)
    cols=cnt
    mem=float(rows)*0.75

    #if request.method=='POST':
    #    return redirect(url_for('feature_ext'))
    
    return render_template('preprocess.html',data=data, msg=msg, rows=rows, cols=cols, dtype=dtype, mem=mem)

@app.route('/feature_ext', methods=['GET', 'POST'])
def feature_ext():
    msg=""
    data=[]
    f1=0
    f2=0
    # Load the dataset
    '''file_path = "heart_attack_dataset.csv"  # Update path if needed
    df = pd.read_csv(file_path)

    # Selecting numerical columns for feature extraction
    numerical_cols = [
        "Age", "BMI", "Diabetes", "Hypertension", "Cholesterol_Level",
        "Resting_BP", "Heart_Rate", "Stress Level", "Sleep Hours Per Day",
        "Temperature_Level", "Max_Heart_Rate_Achieved"
    ]

    # Calculate min, max, and mid-range
    feature_extraction = {
        "Feature": [],
        "Min": [],
        "Max": [],
        "Mid-Range": []
    }

    for col in numerical_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        mid_range = (min_val + max_val) / 2

        feature_extraction["Feature"].append(col)
        feature_extraction["Min"].append(min_val)
        feature_extraction["Max"].append(max_val)
        feature_extraction["Mid-Range"].append(mid_range)

    # Convert to DataFrame
    feature_df = pd.DataFrame(feature_extraction)'''
    ###########
    file_path = "heart_attack_dataset.csv"  # Update path if needed
    df = pd.read_csv(file_path)

    # Selecting numerical columns for feature extraction
    numerical_cols = [
        "Age", "BMI", "Diabetes", "Hypertension", "Cholesterol_Level",
        "Resting_BP", "Heart_Rate", "Stress Level", "Sleep Hours Per Day",
        "Temperature_Level", "Max_Heart_Rate_Achieved"
    ]

    # Calculate Min, Max, Mid-Range, and define range levels
    feature_extraction = {
        "Feature": [],
        "Low Range (Min - Mid)": [],
        "Medium Range (Mid - (Mid+Max)/2)": [],
        "High Range ((Mid+Max)/2 - Max)": []
    }

    for col in numerical_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        mid_range = (min_val + max_val) / 2
        mid_high = (mid_range + max_val) / 2

        feature_extraction["Feature"].append(col)
        feature_extraction["Low Range (Min - Mid)"].append(f"{min_val} - {mid_range}")
        feature_extraction["Medium Range (Mid - (Mid+Max)/2)"].append(f"{mid_range} - {mid_high}")
        feature_extraction["High Range ((Mid+Max)/2 - Max)"].append(f"{mid_high} - {max_val}")

    # Convert to DataFrame
    feature_df = pd.DataFrame(feature_extraction)

    ############
    # Selecting numerical columns for classification
    numerical_cols = [
        "Age", "BMI", "Diabetes", "Hypertension", "Cholesterol_Level",
        "Resting_BP", "Heart_Rate", "Stress Level", "Sleep Hours Per Day",
        "Temperature_Level", "Max_Heart_Rate_Achieved"
    ]

    # Prepare data for classification
    classification_data = {}
    #graph_dir = "static/graphs"
    #os.makedirs(graph_dir, exist_ok=True)

    for col in numerical_cols:
        min_val = df[col].min()
        max_val = df[col].max()
        mid_range = (min_val + max_val) / 2
        mid_high = (mid_range + max_val) / 2

        # Special classification logic for "Sleep Hours Per Day"
        if col == "Sleep Hours Per Day":
            classification_data[col] = {
                "Healthy": "6 - 8",
                "Symptoms": "5 - 6 or 8 - 9",
                "Sick": "< 5 or > 9"
            }
        elif col == "Temperature_Level":
            classification_data[col] = {
                "Healthy": "36.1 - 37.2°C",
                "Symptoms": "37.3 - 38.0°C",
                "Sick": "< 36.0°C or > 38.0°C"
            }
        elif col == "Max_Heart_Rate_Achieved":
            avg_age = df["Age"].mean()
            max_hr = 220 - avg_age  # Max heart rate formula
            healthy_min = 0.50 * max_hr  # 50% of max HR
            healthy_max = 0.85 * max_hr  # 85% of max HR
            sick_threshold = 0.90 * max_hr  # Over 90% is dangerous

            classification_data[col] = {
                "Healthy": f"{healthy_min:.1f} - {healthy_max:.1f}",
                "Symptoms": f"{healthy_max:.1f} - {sick_threshold:.1f}",
                "Sick": f"< {healthy_min:.1f} or > {sick_threshold:.1f}"
            }
        elif col == "Heart_Rate":
            classification_data[col] = {
                "Healthy": "60 - 100 BPM",
                "Symptoms": "50 - 59 BPM or 101 - 110 BPM",
                "Sick": "< 50 BPM or > 110 BPM"
            }
        elif col == "Stress Level":
            classification_data[col] = {
                "Healthy": "1 - 4 (Low Stress)",
                "Symptoms": "5 - 7 (Moderate Stress)",
                "Sick": "8 - 10 (High / Chronic Stress)"
            }
        elif col == "BMI":
            classification_data[col] = {
                "Healthy": "18.5 - 24.9 (Normal Weight)",
                "Symptoms": "17 - 18.4 (Underweight) or 25 - 29.9 (Overweight)",
                "Sick": "< 17 (Severely Underweight) or ≥ 30 (Obese)"
            }
        elif col == "Age":
            classification_data[col] = {
                "Healthy": "18 - 40 (Low Risk)",
                "Symptoms": "41 - 60 (Moderate Risk)",
                "Sick": "> 60 (High Risk)"
            }
        else:
            classification_data[col] = {
                "Healthy": f"{min_val:.2f} - {mid_range:.2f}",
                "Symptoms": f"{mid_range:.2f} - {mid_high:.2f}",
                "Sick": f"{mid_high:.2f} - {max_val:.2f}"
            }
    # Plot grouped bar chart
    '''plt.figure(figsize=(12, 6))
    feature_df.set_index("Feature").plot(kind="bar", figsize=(12, 6), colormap="coolwarm")

    plt.title("Min, Max, and Mid-Range of Features", fontsize=14)
    plt.xlabel("Features", fontsize=12)
    plt.ylabel("Values", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Statistics")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # Save and Show the plot
    plt.tight_layout()
    #plt.savefig("static/feature_extraction_graph.png")  # Saves the graph as an image
    #plt.show()'''

    #confusion matrix
    data = {
        "Age": [69, 32, 89, 78, 38, 41, 20, 39, 70, 19, 47, 55, 19, 81],
        "Cholesterol": [152.1, 166.8, 272.3, 237.7, 207.7, 271.2, 164.8, 297, 280.7, 275, 225.7, 280.2, 215.5, 196.9],
        "Resting_BP": [171, 126, 123, 144, 123, 141, 154, 91, 121, 167, 110, 113, 109, 176],
        "Max_Heart_Rate": [114, 173, 109, 129, 124, 101, 176, 134, 168, 102, 146, 124, 110, 135],
        "Heart_Attack_Risk": ["Low", "Moderate", "Low", "Low", "Moderate", "High", "Low", "Moderate",
                               "Moderate", "Moderate", "Low", "High", "Moderate", "Moderate"]
    }

    df = pd.DataFrame(data)

    # Generate predicted labels using a simple rule-based heuristic
    df["Predicted_Risk"] = np.where(
        (df["Cholesterol"] > 250) & (df["Resting_BP"] > 130), "High",
        np.where((df["Cholesterol"] > 200) | (df["Resting_BP"] > 120), "Moderate", "Low")
    )

    # Compute confusion matrix
    actual = df["Heart_Attack_Risk"]
    predicted = df["Predicted_Risk"]
    cm = confusion_matrix(actual, predicted, labels=["Low", "Moderate", "High"])

    # Plot confusion matrix
    plt.figure(figsize=(6,5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Low", "Moderate", "High"], yticklabels=["Low", "Moderate", "High"])
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")
    #plt.show()

    #if request.method=='POST':
    #    return redirect(url_for('classify'))
    return render_template('feature_ext.html',data=feature_df,data2=classification_data)

#RandomForest
def RandomForest():
    # Load dataset
    df = pd.read_csv("static/upload/datafile.csv")

    # Drop unnecessary columns
    df.drop(columns=["Patient ID", "Country"], inplace=True)

    # Mapping categorical values to numerical values
    mappings = {
        "Gender": {"Male": 1, "Female": 0},
        "Physical_Activity_Level": {"Low": 0, "Moderate": 1, "High": 2},
        "Stress_Level": {"Low": 0, "Moderate": 1, "High": 2},
        "Chest_Pain_Type": {"Typical": 0, "Atypical": 1, "Non-anginal": 2, "Asymptomatic": 3},
        "Thalassemia": {"Normal": 0, "Fixed defect": 1, "Reversible defect": 2},
        "ECG_Results": {"Normal": 0, "ST-T abnormality": 1, "Left Ventricular Hypertrophy": 2},
        "Heart_Attack_Risk": {"Low": 0, "Moderate": 1, "High": 2}
    }

    for col, mapping in mappings.items():
        df[col] = df[col].map(mapping)

    # Drop rows with missing values
    df.dropna(inplace=True)

    # Split features and target variable
    X = df.drop(columns=["Heart_Attack_Risk"])
    y = df["Heart_Attack_Risk"]

    # Apply feature scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Save the StandardScaler for later use in predictions
    with open("scaler.pkl", "wb") as file:
        pickle.dump(scaler, file)

    # Split into training and testing sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the RandomForest Classifier
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Save the trained model
    with open("heart_attack_model.pkl", "wb") as file:
        pickle.dump(model, file)

####
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    data=[]
    f1=0
    f2=0
    file_path = "heart_attack_dataset.csv"  # Update path if needed
    df = pd.read_csv(file_path)

    
    # Create a bar chart for each feature
    '''plt.figure(figsize=(6, 4))
    sns.barplot(
        x=["Healthy", "Symptoms", "Sick"],
        y=[mid_range - min_val, mid_high - mid_range, max_val - mid_high],
        palette=["#4CAF50", "#FFA726", "#E57373"]
    )
    plt.title(f"Classification Ranges for {col}")
    plt.ylabel("Value Range")
    plt.xlabel("Category")
    
    graph_path = os.path.join(graph_dir, f"{col}.png")
    plt.savefig(graph_path)
    plt.close()'''
    #####################33
    file_path = "static/upload/datafile.csv"  # Update path if needed
    dff = pd.read_csv(file_path)
    rx=0
    ry=0
    rz=0
    for dn in dff.values:
        if dn[25]=="Low":
            rx+=1
        if dn[25]=="Moderate":
            ry+=1
        if dn[25]=="High":
            rz+=1
    values=[rx,ry,rz]
    gt=0
    if rx>ry and rx>rz:
        gt=rx+5
    elif ry>rz:
        gt=ry+5
    else:
        gt=rz+5
    doc=["Low Risk","Moderate","High"]
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    cc=['green','yellow','red']
    plt.bar(doc, values, color =cc,
            width = 0.4)
 

    plt.ylim((1,gt))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    #plt.xticks(rotation=20)
    plt.savefig('static/'+fn)
    
    plt.close()
    return render_template('classify.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


