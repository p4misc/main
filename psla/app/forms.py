# -*- coding: utf-8 -*

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired
from wtforms import SelectField, SubmitField, TextAreaField

class UploadForm(FlaskForm):
    uploadFile = FileField(u'ログファイル', validators=[
        FileRequired(message=u"アップロードするログファイルを選択してください"),
        FileAllowed(['txt', 'gz', 'zip', 'log'], 'Log files only!')
    ])
    submit = SubmitField(u'アップロード開始')

class AnalyzeLog(FlaskForm):
    logFile = SelectField(u'ログファイル', validators = [DataRequired()])
    submit = SubmitField(u'分析開始')

class MySelectField(SelectField):
    def pre_validate(self, form):
        pass

class QueryLog(FlaskForm):
    logFile = SelectField(u'ログファイル', validators = [DataRequired()])
    queryOptions = MySelectField(u'定義済みのSQL文', coerce=str, validators = [DataRequired()])
    sqlQuery = TextAreaField(u"SQL文", default=u"ここにSQL文を入力してください",
                             validators = [DataRequired()])
    submit = SubmitField(u'クエリを実行')

class ChartLog(FlaskForm):
    logFile = SelectField(u'ログファイル', validators = [DataRequired()])
    chartId = SelectField(u'表示するグラフ', validators = [DataRequired()])
    submit = SubmitField(u'グラフを表示')
