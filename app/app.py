import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template

# Initialize  Flask app
app = Flask(__name__)

# Function to obtain a connection to the db
def get_db_connection():
    # Reads the URL-ul of the db  from the docker env variabile set în docker-compose.yml
    conn_string = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(conn_string)
    return conn

# main route of the app  (Dashboard)
@app.route('/')
def index():
    conn = get_db_connection()
    # Opens a "cursor" to execute SQL interogations
    # 'cursor_factory' helps obtain results as dictionaries (easier to use in HTML)
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Main SQL interogation : exctracts all equipments and related details (location, user)
    # using JOIN to combine data from multiple tables
    cur.execute("""
                SELECT
                    a.host_name,
                    a.ip_address,
                    a.status,
                    a.serial_number,
                    l.room_name,
                    u.first_name,
                    u.last_name
                FROM assets a
                         LEFT JOIN locations l ON a.location_id = l.location_id
                         LEFT JOIN users u ON a.assigned_user_id = u.user_id
                ORDER BY a.host_name;
                """)

    # takes all results of the interogation
    assets = cur.fetchall()

    # closes the cursor and the connection
    cur.close()
    conn.close()

    # sends extracted data  ('assets') to the HTML file to display
    return render_template('assets.html', assets=assets)

#  route to see all details of one single equipment
@app.route('/asset/<serial_number>')
def asset_detail(serial_number):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # interogation for details
    cur.execute("SELECT * FROM assets WHERE serial_number = %s", (serial_number,))
    asset = cur.fetchone()

    # interogation for the components of that equipment
    cur.execute("""
                SELECT c.component_type, c.manufacturer, c.model_number, c.details
                FROM components c
                         JOIN asset_components ac ON c.component_id = ac.component_id
                WHERE ac.asset_id = %s
                """, (asset['asset_id'],))
    components = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('asset_detail.html', asset=asset, components=components)