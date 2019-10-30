"""PSLA - Perforce Server Log Analyzer
"""

from flask import Flask, request, redirect, url_for, render_template, flash, Response
from flask_wtf.csrf import CSRFProtect
from werkzeug import secure_filename

import logging
import pandas as pd
import sqlite3
import traceback
from datetime import datetime
import glob
import textwrap

from altair import Chart, X, Y, Axis

# Modules from our psla app
from config import Config
from app import app
from app.forms import UploadForm, AnalyzeLog, QueryLog, ChartLog
from log2sql import Log2sql
import app.queries as queries
import os

# Default chart dimensions
WIDTH = 600
HEIGHT = 300

UPLOAD_FOLDER = os.getenv('PSLA_LOGS', '/logs')     # Default is inside docker container
ALLOWED_EXTENSIONS = set(['txt'])

app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
csrf = CSRFProtect(app)


def allowed_file(filename):
    return True
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

class MyOptions():
    "Options class with defaults for Log2sql"
    def __init__(self, logfile, sql=False, verbosity=logging.INFO, outlog=None):
        self.dbname = None
        self.logfile = logfile
        self.sql = sql
        self.no_sql = not sql
        self.verbosity = verbosity
        self.interval = 10
        self.outlog = outlog
        self.output = None
        self.interval = None
        self.reset = True

@app.route('/')
def index():
    """Front page for application"""
    return render_template('index.html')

@app.route('/uploadLog', methods=['GET', 'POST'])
def uploadLog():
    "Upload log file"
    form = UploadForm()
    app.logger.debug("uploadLog: %s" % form.errors)
    app.logger.debug('------ {0}'.format(request.form))
    if form.is_submitted():
        app.logger.debug(form.errors)

    if form.validate():
        app.logger.debug(form.errors)
    app.logger.debug(form.errors)

    if form.validate_on_submit():
        db_folder = app.config['UPLOAD_FOLDER']
        filename = secure_filename(form.uploadFile.data.filename)
        file_path = os.path.join(db_folder, filename)
        form.uploadFile.data.save(file_path)

        os.chdir(db_folder)
        optionsSQL = MyOptions([file_path], sql=True, outlog='log.out')
        log2sql = Log2sql(optionsSQL)
        log2sql.processLogs()

        return redirect(url_for('analyzeLog'))
    return render_template('uploadLog.html', title='Upload Log', form=form)

@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x < 100:
            # print x
            # x = x + 10
            # time.sleep(0.2)
            yield "data:" + str(x) + "\n\n"
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/analyzeLog', methods=['GET', 'POST'])
def analyzeLog():
    "Access previously uploaded log"
    db_folder = app.config['UPLOAD_FOLDER']
    logFiles = glob.glob('%s/*.db' % db_folder)

    form = AnalyzeLog()
    form.logFile.choices = [(f, f) for f in logFiles]

    if not form.validate_on_submit():
        return render_template('analyzeLog.html', tables=[], charts=[], dbName=None, form=form)

    dbname = os.path.join(form.logFile.data)
    if not os.path.exists(dbname):
        flash('Database does not exist', 'error')
        return render_template('error.html', title='Database error')

    app.dbname = dbname

    try:
        conn = sqlite3.connect(dbname)
    except Exception as e:
        app.logger.error(traceback.format_exc())
        flash('Error: %s' % (str(e)), 'error')
        return render_template('error.html', title='Error in database reporting')

    tables = []
    for q in queries.queries:
        if not 'sql' in q or not q['sql']:
            continue
        app.logger.debug("running table query: %s - %s" % (q['title'], q['sql']))
        start = datetime.now()
        try:
            df = pd.read_sql_query(q['sql'], conn)
            table = df.to_html()
        except Exception as e:
            table = "<h3>ERROR: %s</h3>" % str(e)
        end = datetime.now()
        delta = end - start
        tables.append({'data': table,
                       'title': q['title'],
                       'explanation': q['explanation'],
                       'sql': q['sql'],
                       'time_taken': str(delta)})
    return render_template('analyzeLog.html', tables=tables, dbName=dbname, form=form)

@app.route('/queryLog', methods=['GET', 'POST'])
def queryLog():
    "Run queries on selected log"

    db_folder = app.config['UPLOAD_FOLDER']
    logFiles = glob.glob('%s/*.db' % db_folder)

    form = QueryLog()
    form.logFile.choices = [(f, f) for f in logFiles]
    form.queryOptions.choices = [('--Please select SQL', '<select>')]
    for q in queries.queries:
        sql = textwrap.dedent(q['sql']).lstrip()
        form.queryOptions.choices.append((sql, q['title']))
    try:
        dbname = app.dbname
        if os.path.exists(dbname):
            form.logFile.data = dbname
    except:
        pass
    if not form.validate_on_submit():
        return render_template('queryLog.html', data={}, dbName=None, form=form)

    dbname = os.path.join(form.logFile.data)
    if not os.path.exists(dbname):
        flash('Database does not exist', 'error')
        return render_template('error.html', title='Database error')

    try:
        conn = sqlite3.connect(dbname)
    except Exception as e:
        app.logger.error(traceback.format_exc())
        flash('Error: %s' % (str(e)), 'error')
        return render_template('error.html', title='Error in database reporting')

    sqlQuery = form.sqlQuery.data
    app.logger.debug("running interactive query: %s" % (sqlQuery))
    start = datetime.now()
    try:
        df = pd.read_sql_query(sqlQuery, conn)
        table = df.to_html()
    except Exception as e:
        table = "<h3>ERROR: %s</h3>" % str(e)
    end = datetime.now()
    delta = end - start
    data = ({'data': table,
             'sql': sqlQuery,
             'time_taken': str(delta)})
    return render_template('queryLog.html', data=data, dbName=dbname, form=form)

@app.route('/schema', methods=['GET'])
def schema():
    return render_template('schema.html')

@app.route('/chartLog', methods=['GET', 'POST'])
def chartLog():
    "Display chart for selected log"

    db_folder = app.config['UPLOAD_FOLDER']
    logFiles = glob.glob('%s/*.db' % db_folder)

    form = ChartLog()
    form.logFile.choices = [(f, f) for f in logFiles]
    form.chartId.choices = [(q['id'], q['id']) for q in queries.graphs]
    try:
        dbname = app.dbname
        if os.path.exists(dbname):
            form.logFile.data = dbname
    except:
        pass

    if not form.validate_on_submit():
        return render_template('chartLog.html', chart={}, dbName=None, form=form)

    dbname = os.path.join(form.logFile.data)
    if not os.path.exists(dbname):
        flash('Database does not exist', 'error')
        return render_template('error.html', title='Database error')

    try:
        conn = sqlite3.connect(dbname)
    except Exception as e:
        app.logger.error(traceback.format_exc())
        flash('Error: %s' % (str(e)), 'error')
        return render_template('error.html', title='Error in database reporting')

    chartId = form.chartId.data
    charts = [q for q in queries.graphs if q['id'] == chartId]
    if not charts:
        flash("Error: logic error couldn't find chartId", 'error')
        return render_template('error.html', title='Error in in configuration of chart reports')

    q = charts[0]
    app.logger.debug("running chart query: %s - %s" % (q['title'], q['sql']))
    start = datetime.now()
    try:
        df = pd.read_sql_query(q['sql'], conn)
    except Exception as e:
        flash('Error: %s' % (str(e)), 'error')
        return render_template('error.html', title='Error in database reporting')

    end = datetime.now()
    delta = end - start
    if q['graph_type'] == 'line':
        chart = Chart(data=df, height=HEIGHT, width=WIDTH).mark_line().encode(
            X(q['x']['field'], axis=Axis(title=q['x']['title'], labelOverlap='greedy')),
            Y(q['y']['field'], axis=Axis(title=q['y']['title']))
        )
    else:
        chart = Chart(data=df, height=HEIGHT, width=WIDTH).mark_bar().encode(
            X(q['x']['field'], axis=Axis(title=q['x']['title'], labelOverlap='greedy')),
            Y(q['y']['field'], axis=Axis(title=q['y']['title']))
        )
    data = {'id': "chart",
           'data': chart.to_json(),
           'title': q['title'],
           'explanation': q['explanation'],
           'sql': q['sql'],
           'time_taken': str(delta)}
    return render_template('chartLog.html', chart=data, dbName=dbname, form=form)