from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import sqlite3
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def getPCstr(playcount):
    s = str(playcount)
    if len(s[:-3]) > 3:
        if len(s[:-6]) == 1:
            return str(float(s[:-5]) / 10) + 'm'
        return s[:-6] + 'm'
    return s[:-3] + 'k'

@app.route('/get_data')
def get_data():
    input_list_json = request.args.get('inputList')

    if input_list_json is None:
        return jsonify({"error": "Input list parameter is missing"}), 400  # Return a 400 Bad Request status

    # Convert the JSON string back to a Python list
    input_list = json.loads(input_list_json)
    
    
    print("Accessed /get_data endpoint")
    connection = sqlite3.connect('osuMaps.db')  
    cursor = connection.cursor()

    for i in range(len(input_list)):
        if input_list[i] == '':
            input_list[i] = '999999999'
            if i % 2 == 0:
                input_list[i] = '0'
        elif 14 <= i <= 17:
            if input_list[i] != 2:
                input_list[i] = bool(input_list[i] - 1)
           
    print(input_list)
    
    query = f"""
        SELECT osuMaps.*, osuScores.*
        FROM osuMaps
        JOIN osuScores ON osuMaps.ID = osuScores.ID
        WHERE osuScores.pp >= {input_list[0]} AND osuScores.pp <= {input_list[1]}
        AND osuMaps.AR >= {input_list[2]} AND osuMaps.AR <= {input_list[3]}
        AND osuMaps.OD >= {input_list[4]} AND osuMaps.OD <= {input_list[5]}
        AND osuMaps.CS >= {input_list[6]} AND osuMaps.CS <= {input_list[7]}
        AND osuMaps.SR >= {input_list[8]} AND osuMaps.SR <= {input_list[9]}
        AND osuMaps.DrainTime >= {input_list[10]} AND osuMaps.DrainTime <= {input_list[11]}
        AND osuScores.max_combo >= {input_list[12]} AND osuScores.max_combo <= {input_list[13]}
        AND (
            (osuScores.HD = {input_list[14]})
            OR
            ({input_list[14]} = 2)
        )
        AND (
            (osuScores.HR = {input_list[15]})
            OR
            ({input_list[15]} = 2)
        )
        AND (
            (osuScores.DT = {input_list[16]})
            OR
            ({input_list[16]} = 2)
        )
        AND (
            (osuScores.FL = {input_list[17]})
            OR
            ({input_list[17]} = 2)
        )
        AND osuMaps.BPM >= {input_list[18]} AND osuMaps.BPM <= {input_list[19]}
        AND osuScores.accuracy >= {input_list[20]} AND osuScores.accuracy <= {input_list[21]}
        AND CAST(osuMaps.MapsetPlaycount AS INTEGER) >= {input_list[22]} 
        AND CAST(osuMaps.MapsetPlaycount AS INTEGER) <= {input_list[23]}
        ORDER BY DateRanked DESC;
    """
    cursor.execute(query)

    rows = cursor.fetchall()   
    data = [{'URL': row[2], 'Player': row[22], 'Playcount': getPCstr(row[16]), 'mapsetID': row[18], 'accuracy': row[20],
             'artist': row[1], 'title': row[0], 'diff': row[3], 'count': len(rows)} for row in rows] 
   
    connection.close()

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
