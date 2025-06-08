from flask import Flask, jsonify, render_template, request
import json
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    print("GET / called")
    return render_template('index.html')

@app.route('/data')
def get_data():
    print("GET /data called")
    return jsonify({"message": "Hello from /data!"})

@app.route('/search')
def search():
    print("GET /search called")

    input_list = request.args.get('inputList')
    if input_list is None:
        return jsonify({"error": "Missing inputList"}), 400
    
    input_list = json.loads(input_list)

    for i in range(len(input_list)):
        if input_list[i] == '':
            input_list[i] = '999999999'
            if i % 2 == 0:
                input_list[i] = '0'
        # why am I so retarded
        elif 20 <= i <= 23:
            if input_list[i] == 2:
                input_list[i] = 1
            elif input_list[i] == 1:
                input_list[i] = 2

        # idk just whatever
        if input_list[16] == "":
            input_list[16] = 0

    print(input_list)
    
    connection = sqlite3.connect('osuMaps.db')
    cursor = connection.cursor()

    print("Accessed /get_data endpoint")        

    query = f"""
        SELECT osuMaps.*, osuScores.*
        FROM osuMaps
        JOIN osuScores ON osuMaps.DiffID = osuScores.ID
        WHERE osuScores.pp >= {input_list[0]} AND osuScores.pp <= {input_list[1]}
        AND osuMaps.AR >= {input_list[2]} AND osuMaps.AR <= {input_list[3]}
        AND osuMaps.OD >= {input_list[4]} AND osuMaps.OD <= {input_list[5]}
        AND osuMaps.CS >= {input_list[6]} AND osuMaps.CS <= {input_list[7]}
        AND osuMaps.SR >= {input_list[8]} AND osuMaps.SR <= {input_list[9]}
        AND osuMaps.DrainTime >= {input_list[10]} AND osuMaps.DrainTime <= {input_list[11]}
        AND osuScores.max_combo >= {input_list[12]} AND osuScores.max_combo <= {input_list[13]}
        AND osuMaps.BPM >= {input_list[14]} AND osuMaps.BPM <= {input_list[15]}
        AND (osuScores.accuracy >= {input_list[16]} AND osuScores.accuracy <= {input_list[17]})
        AND CAST(osuMaps.MapsetPlaycount AS INTEGER) >= {input_list[18]} 
        AND CAST(osuMaps.MapsetPlaycount AS INTEGER) <= {input_list[19]}
        AND (
            (osuScores.HD = {input_list[20]})
            OR
            ({input_list[20]} = 2)
        )
        AND (
            (osuScores.HR = {input_list[21]})
            OR
            ({input_list[21]} = 2)
        )
        AND (
            (osuScores.DT = {input_list[22]})
            OR
            ({input_list[22]} = 2)
        )
        AND (
            (osuScores.FL = {input_list[23]})
            OR
            ({input_list[23]} = 2)
        )
        ORDER BY DateRanked DESC;
    """

    cursor.execute(query)
    rows = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    connection.close()
    # print(results[:10])
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
