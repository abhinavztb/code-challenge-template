from flask import Flask, request, jsonify, g
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
import sqlite3
import math

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
    'title': 'Weather API',
    'uiversion': 3
}
swagger = Swagger(app)

DATABASE_PATH = '/Users/abhi/Documents/GitHub/code-challenge-template/answers/wx_data.db'

def get_db_connection():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row  # This allows to access columns by name
    return g.db

def close_db_connection(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db_connection)

class Weather(Resource):
    @swag_from('weather.yml')
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        station_id = request.args.get('station_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        query_parts = ["SELECT * FROM WeatherData"]
        query_filters = []
        params = []

        if station_id:
            query_filters.append("station_id = ?")
            params.append(station_id)
        if start_date:
            query_filters.append("record_date >= ?")
            params.append(start_date)
        if end_date:
            query_filters.append("record_date <= ?")
            params.append(end_date)

        if query_filters:
            query_parts.append("WHERE " + " AND ".join(query_filters))

        query_parts.append("LIMIT ? OFFSET ?")

        # Pagination
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        offset = (page - 1) * per_page
        params.extend([per_page, offset])

        cursor.execute(" ".join(query_parts), params)
        data = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) FROM WeatherData" + (" WHERE " + " AND ".join(query_filters) if query_filters else ""), params[:-2])
        total = cursor.fetchone()[0]

        conn.close()

        results = [{
            'station_id': row['station_id'],
            'record_date': row['record_date'],
            'max_temp': float(row['max_temp'])/10,
            'min_temp': float(row['min_temp'])/10,
            'precipitation': float(row['precipitation'])
        } for row in data]

        return jsonify({
            'data': results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': math.ceil(total / per_page)
        })

class WeatherStats(Resource):
    @swag_from('weather_stats.yml')
    def get(self):
        conn = get_db_connection()
        cursor = conn.cursor()

        station_id = request.args.get('station_id')
        year = request.args.get('year')

        query_parts = ["SELECT * FROM WeatherAnalysis"]
        query_filters = []
        params = []

        if station_id:
            query_filters.append("station_id = ?")
            params.append(station_id)
        if year:
            query_filters.append("year = ?")
            params.append(year)

        if query_filters:
            query_parts.append("WHERE " + " AND ".join(query_filters))

        cursor.execute(" ".join(query_parts), params)
        data = cursor.fetchall()
        conn.close()

        results = [{
            'station_id': row['station_id'],
            'year': row['year'],
            'avg_max_temp': row['avg_max_temp'],
            'avg_min_temp': row['avg_min_temp'],
            'total_precipitation': row['total_precipitation']
        } for row in data]

        return jsonify(results)

api.add_resource(Weather, '/api/weather')
api.add_resource(WeatherStats, '/api/weather/stats')

if __name__ == '__main__':
    app.run(debug=True)
