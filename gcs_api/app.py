import psycopg2
import pandas as pd

from flask import Flask, jsonify, request

app = Flask(__name__)

def connection_factory():
    return psycopg2.connect(**{
        "dbname": "gcs",
        "user": "docker",
        "password": "docker",
        "host": "127.0.0.1",
        "port": 25432
    })


@app.route('/api/images/landsat/rangesearch')
def rangesearch_landsat():
    timerange = request.args.get('time').split('/')
    bbox = request.args.get('bbox').split(',')
    platform = request.args.get('platform')
    sensor = request.args.get('sensor')

    if request.args.get('sensor'):
        sensor = f"AND sensor_id = '{sensor}'"
    else:
        sensor = ""

    # OBS: Ordem do ST_MakeEnvelope trocada por causa da inserção no banco
    query = pd.read_sql(
        f"""
            SELECT 
                scene_id, spacecraft_id, sensor_id, sensing_time, base_url
            FROM 
                landsat_index
            WHERE
                ST_Intersects(
                    ST_MakeEnvelope(west_lon, north_lat, east_lon, south_lat, 4326),
                    ST_MakeEnvelope({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}, 4326)
                ) AND sensing_time >= '{timerange[0]}' AND sensing_time <= '{timerange[1]}'
                AND spacecraft_id = '{platform}' {sensor};
        """, con=connection_factory())

    query['sensing_time'] = pd.to_datetime(query['sensing_time']).dt.strftime('%Y-%m-%d')
    return jsonify(list(query.T.to_dict().values()))


@app.route('/api/images/sentinel/rangesearch')
def rangesearch_sentinel():
    timerange = request.args.get('time').split('/')
    bbox = request.args.get('bbox').split(',')

    query = pd.read_sql(
        f"""
            SELECT 
                granule_id, product_id, mgrs_tile, sensing_time, base_url
            FROM 
                sentinel_index
            WHERE
                ST_Intersects(
                    ST_MakeEnvelope(west_lon, north_lat, east_lon, south_lat, 4326),
                    ST_MakeEnvelope({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]}, 4326)
                ) AND sensing_time >= '{timerange[0]}' AND sensing_time <= '{timerange[1]}';
        """, con=connection_factory())

    query['sensing_time'] = pd.to_datetime(query['sensing_time']).dt.strftime('%Y-%m-%d')
    return jsonify(list(query.T.to_dict().values()))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
