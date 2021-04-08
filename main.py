# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 15:12:48 2020

@author: Gerald
"""

# main.py

from app import app
from db_setup import init_db, db_session
from forms import ExperimentSearchForm
from flask import flash, render_template, request, redirect, send_file
from data import Data
from settings import Setting
from tables import Results, Settings

init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    """Renders the index.html template"""
    search = ExperimentSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)

# Calls the search function and returns the results in results.html
@app.route('/results')
def search_results(search):
    """Takes in a ModelSearchForm and queries the database using the search String from the ModelSearchForm
    Returns a results.html template containing a flask-table with the models that contains the search String"""
    results = []
    search_string = search.data['search']

    if search_string:
        if search.data['select'] == 'Experimental ID':
            qry = db_session.query(Data).filter(
                    Data.id.contains(search_string, autoescape=True))
            results = qry.all()
        elif search.data['select'] == 'Set temperature':
            qry = db_session.query(Data).filter(
                Data.set_temperature.contains(search_string, autoescape=True))
            results = qry.all()
        elif search.data['select'] == 'Data Values':
            qry = db_session.query(Data).filter(
                Data.data_values.contains(search_string, autoescape=True))
            results = qry.all()
        else:
            qry = db_session.query(Data)
            results = qry.all()
    else:
        qry = db_session.query(Data)
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        result = Results(results)
        result.border = True

        search = ExperimentSearchForm(request.form)
        counter = 'Number of experiments found: ' + str(len(results))
        return render_template('results.html', form=search, result=result, counter=counter)

# Links to the respective download urls for the models based on their id
@app.route('/download/<string:id>')
def download(id):
    """Sends the.zip files of the respective models when the download link is accessed"""
    path = "downloads/config/" + str(id) + ".zip"
    return send_file(path, as_attachment=True)

# Links to the respective settings for the models based on their id
@app.route('/settings/<string:id>')
def settings(id):
    """Returns a settings.html template that contains the settings of the respective model"""
    results = []
    qry = db_session.query(Setting).filter(Setting.id==id)
    results = qry.all()
    table = Settings(results)
    search = ExperimentSearchForm(request.form)
    return render_template('settings.html', form=search, table=table)

# Links to the respective genetic circuit diagrams based on their ids
@app.route('/display/<string:id>')
def display(id):
    """Returns the respective genetic circuit diagram of the selected model"""
    search=ExperimentSearchForm(request.form)
    num_id = int(''.join(filter(str.isdigit, str(id))))
    if num_id <= 13:
        return render_template('inducible.html', form=search)
    elif num_id <= 17:
        return render_template('constitutive.html', form=search)
    elif num_id <= 21:
        return render_template('constitutivevariedpromoter.html', form=search)
    elif num_id <= 23:
        return render_template('constitutivevariedrbs.html', form=search)
    elif num_id <= 27:
        return render_template('NOTgate.html', form=search)
    elif num_id <= 33:
        return render_template('ANDgate.html', form=search)
    elif num_id <= 44:
        return render_template('ORgate.html', form=search)
    else:
        return render_template('diagramerror.html', form=search)
        

if __name__ == '__main__':
    import os
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False
    app.run(threaded = True, port=5000)