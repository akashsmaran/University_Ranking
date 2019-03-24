from flask import Flask, redirect, url_for, request, render_template
import pandas as pd
import TIdatabase as ti
import numpy as np
import pandas as pd
import pickle

app = Flask(__name__)

@app.route('/success/<name>/',defaults={'country': None})
@app.route('/success//<country>', defaults={'name': None})
@app.route('/success/<name>/<country>')
def display(name, country):
    df = pd.read_csv("DataFinal.csv",delimiter=',')
    df1 = pd.read_csv("timesData.csv", delimiter=',')
    if(country==None):
        y = df.loc[df['Institution'] == name]
        y1 = df1.loc[df1['university_name'] == name]
        return render_template('query.html', tables=[y.to_html(classes='data', header="true")],tables1=[y1.to_html(classes='data', header="true")])
    elif(name==None):
        y = df.loc[df['Location'] == country]
        y1 = df1.loc[df1['country'] == country]
        return render_template('query.html', tables=[y.to_html(classes='data', header="true")],tables1=[y1.to_html(classes='data', header="true")])
    else:
        y = df.loc[df['Location'] == country]
        y = y.loc[y['Institution'] == name]
        y1 = df1.loc[df1['country'] == country]
        y1 = y1.loc[y1['university_name'] == name]
        return render_template('query.html', tables=[y.to_html(classes='data', header="true")],tables1=[y1.to_html(classes='data', header="true")])


@app.route('/login',methods = ['POST', 'GET'])
def search():
   if request.method == 'POST':
      name = request.form['nm']
      country = request.form['country']
      course = request.form.get('xyz')
      name = name.lower()
      country = country.lower()
      if(course=="def"):
          return redirect(url_for('display',name = name,country = country))
      elif(course=="CS" and name=="" and country==""):
          df = pd.read_csv("CS.csv",delimiter=',')
          return render_template('query1.html', tables=[df.to_html(classes='data', header="true")])
      elif(course=="CS" and name!=""):
          df = pd.read_csv("CS.csv",delimiter=',')
          y = df.loc[df['Institution'] == name]
          return render_template('query1.html', tables=[y.to_html(classes='data', header="true")])
      elif(course=="CS" and name=="" and country!=""):
          df = pd.read_csv("CS.csv",delimiter=',')
          y = df.loc[df['country'] == country]
          return render_template('query1.html', tables=[y.to_html(classes='data', header="true")])    
      elif(course=="Mech" and name!=""):
          df = pd.read_csv("Mech.csv",delimiter=',')
          y = df.loc[df['Institution'] == name]
          return render_template('query1.html', tables=[y.to_html(classes='data', header="true")])
      elif(course=="BIO" and name!=""):
          df = pd.read_csv("Biomed.csv",delimiter=',')
          y = df.loc[df['Institution'] == name]
          return render_template('query1.html', tables=[y.to_html(classes='data', header="true")])      
          
   else:
      name = request.args.get('nm')
      country = request.args.get('country')
      name = name.lower()
      country = country.lower()
      return redirect(url_for('display',name = name,country = country))
"""
@app.route('/filter',methods = ['POST', 'GET'])
def abcd():
   df = pd.read_csv("CS.csv",delimiter=',')
   course = request.form['course']
   course = course.lower()
   y = df.loc[df['Institution*'] == course]
   return render_template('query.html', tables=[y.to_html(classes='data', header="true")])
"""
@app.route('/calc',methods = ['POST', 'GET'])
def calculate():
   if request.method == 'POST':
      admissionstest = request.form['admissionstest']
      gpa = request.form['gpa']
      averageap = request.form['averageap']
      ap = request.form['ap']
      sat = request.form['sat']
      female = request.form['female']
      schooltype = request.form['schooltype']
      mina = request.form['min']
      early = request.form['early']
      out = request.form['out']
      alum = request.form['alum']
      inta = request.form['inta']
      sport = request.form['sport']
      filename = 'finalized_model.sav'
      loaded_model = pickle.load(open(filename, 'rb'))
      """
      candidate = [0.926899206,7,1.06733864,
             3,-0.187109979,0,1,
             0,0,1,0,0,
             0]
      """
      candidate = [admissionstest,ap,averageap,sat,gpa,schooltype,female,mina,inta,sport,early,alum,out]
      college_cols = ["acceptrate","size","public"]
      colleges = ti.College()
      preds = []
      for i, row in colleges.df.iterrows():
          Xp1 = candidate + list(row[college_cols])
          y_rf = loaded_model.predict_proba([Xp1])[0][1]
          p =  {'college':row.collegeID, 'prob':y_rf}
          preds.append(p)
    
      return render_template('show.html', your_list=preds)

if __name__ == '__main__':
   app.run(debug = True)