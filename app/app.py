import os
import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Function to obtain a connection to the db
def get_db_connection():
    conn_string = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(conn_string)
    return conn

# 1. ROUTE: Dashboard (Home) with Filtering
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    selected_location = request.args.get('location')

    sql_query = """
                SELECT
                    a.host_name, a.ip_address, a.status, a.serial_number,
                    l.room_name, u.first_name, u.last_name
                FROM assets a
                         LEFT JOIN locations l ON a.location_id = l.location_id
                         LEFT JOIN users u ON a.assigned_user_id = u.user_id
                """

    query_params = []

    if selected_location and selected_location != 'All':
        sql_query += " WHERE a.location_id = %s"
        query_params.append(selected_location)

    sql_query += " ORDER BY a.host_name;"

    cur.execute(sql_query, query_params)
    assets = cur.fetchall()

    cur.execute("SELECT location_id, room_name FROM locations ORDER BY room_name")
    locations = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('assets.html', assets=assets, locations=locations, selected_location=selected_location)

# 2. ROUTE: Add New Asset (Create)
@app.route('/add_asset', methods=('GET', 'POST'))
def add_asset():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        host_name = request.form['host_name']
        serial_number = request.form['serial_number']
        ip_address = request.form['ip_address']
        status = request.form['status']
        location_id = request.form['location_id']
        user_id = request.form['user_id']

        try:
            cur.execute("""
                        INSERT INTO assets (host_name, serial_number, ip_address, status, location_id, assigned_user_id, purchase_date)
                        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_DATE)
                        """,
                        (host_name, serial_number, ip_address, status, location_id, user_id)
                        )
            conn.commit()
            cur.close()
            conn.close()
            return redirect('/')
        except Exception as e:
            conn.rollback()
            return f"Eroare la adaugare: {e}"

    cur.execute("SELECT location_id, room_name FROM locations")
    locations = cur.fetchall()

    cur.execute("SELECT user_id, first_name, last_name FROM users")
    users = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('add_asset.html', locations=locations, users=users)

# 3. ROUTE: Delete Asset
@app.route('/delete_asset/<serial_number>', methods=['POST'])
def delete_asset(serial_number):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM assets WHERE serial_number = %s", (serial_number,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect('/')
    except Exception as e:
        conn.rollback()
        return f"Eroare la stergere: {e}"

# 4. ROUTE: Asset Details & Component Management
@app.route('/asset/<serial_number>')
def asset_detail(serial_number):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # Get Asset Info
    cur.execute("SELECT * FROM assets WHERE serial_number = %s", (serial_number,))
    asset = cur.fetchone()

    if asset is None:
        cur.close()
        conn.close()
        return "Echipamentul nu a fost gasit", 404

    # Get Associated Components (Linked)
    cur.execute("""
                SELECT ac.asset_component_id, c.component_type, c.manufacturer, c.model_number, c.details
                FROM components c
                         JOIN asset_components ac ON c.component_id = ac.component_id
                WHERE ac.asset_id = %s
                ORDER BY c.component_type
                """, (asset['asset_id'],))
    current_components = cur.fetchall()

    # Get ALL Components (For dropdown menu)
    cur.execute("SELECT * FROM components ORDER BY component_type, manufacturer")
    all_components = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('asset_detail.html', asset=asset, components=current_components, all_components=all_components)

# 5. ROUTE: Link Component to Asset
@app.route('/link_component', methods=['POST'])
def link_component():
    asset_id = request.form['asset_id']
    component_id = request.form['component_id']
    serial_number = request.form['serial_number']

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("INSERT INTO asset_components (asset_id, component_id) VALUES (%s, %s)", (asset_id, component_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Eroare link: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('asset_detail', serial_number=serial_number))

# 6. ROUTE: Unlink (Remove) Component from Asset
@app.route('/unlink_component', methods=['POST'])
def unlink_component():
    asset_component_id = request.form['asset_component_id']
    serial_number = request.form['serial_number']

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM asset_components WHERE asset_component_id = %s", (asset_component_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Eroare unlink: {e}")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('asset_detail', serial_number=serial_number))