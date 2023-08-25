from flask import Flask 

app = Flask(__name__)

@app.route('/excelFile')
def getExcelFile():
    return {'file': 'test'}