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

    query = """
        SELECT osuMaps.*, osuScores.*
        FROM osuMaps
        JOIN osuScores ON osuMaps.DiffID = osuScores.ID
        WHERE osuScores.pp >= ? AND osuScores.pp <= ?
        AND osuMaps.AR >= ? AND osuMaps.AR <= ?
        AND osuMaps.OD >= ? AND osuMaps.OD <= ?
        AND osuMaps.CS >= ? AND osuMaps.CS <= ?
        AND osuMaps.SR >= ? AND osuMaps.SR <= ?
        AND osuMaps.DrainTime >= ? AND osuMaps.DrainTime <= ?
        AND osuScores.max_combo >= ? AND osuScores.max_combo <= ?
        AND osuMaps.BPM >= ? AND osuMaps.BPM <= ?
        AND (osuScores.accuracy >= ? AND osuScores.accuracy <= ?)
        AND CAST(osuMaps.MapsetPlaycount AS INTEGER) >= ? 
        AND CAST(osuMaps.MapsetPlaycount AS INTEGER) <= ?
        AND ((osuScores.HD = ?) OR (? = 2))
        AND ((osuScores.HR = ?) OR (? = 2))
        AND ((osuScores.DT = ?) OR (? = 2))
        AND ((osuScores.FL = ?) OR (? = 2))
        ORDER BY DateRanked DESC;
    """

    # Then pass the parameters
    params = (
        input_list[0], input_list[1],
        input_list[2], input_list[3],
        input_list[4], input_list[5],
        input_list[6], input_list[7],
        input_list[8], input_list[9],
        input_list[10], input_list[11],
        input_list[12], input_list[13],
        input_list[14], input_list[15],
        input_list[16], input_list[17],
        input_list[18], input_list[19],
        input_list[20], input_list[20],
        input_list[21], input_list[21],
        input_list[22], input_list[22],
        input_list[23], input_list[23]
    )

    cursor.execute(query)
    rows = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    connection.close()
    # print(results[:10])
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
