import os
import psycopg2
import psycopg2.extras
import ipaddress
import re
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'cheie_secreta_proiect_ubd'

def get_db_connection():
    conn_string = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(conn_string)
    return conn

# --- LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        if user:
            session['user_id'] = user['user_id']
            session['role'] = user['role']
            session['name'] = user['first_name']
            return redirect('/')
        else:
            return render_template('login.html', error="Date incorecte!")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# --- DASHBOARD ---
@app.route('/')
def index():
    if 'user_id' not in session: return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    selected_location = request.args.get('location')

    sql_query = """
                SELECT a.*, l.room_name, u.first_name, u.last_name
                FROM assets a
                         LEFT JOIN locations l ON a.location_id = l.location_id
                         LEFT JOIN users u ON a.assigned_user_id = u.user_id
                WHERE 1=1
                """
    query_params = []

    if session['role'] != 'admin':
        sql_query += " AND a.assigned_user_id = %s"
        query_params.append(session['user_id'])

    if selected_location and selected_location != 'All':
        sql_query += " AND a.location_id = %s"
        query_params.append(selected_location)

    sql_query += " ORDER BY a.host_name;"

    cur.execute(sql_query, query_params)
    assets = cur.fetchall()

    cur.execute("SELECT location_id, room_name FROM locations ORDER BY room_name")
    locations = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('assets.html', assets=assets, locations=locations,
                           selected_location=selected_location,
                           user_role=session['role'],
                           current_user_id=session['user_id'])

# --- ADD ASSET (Actualizat cu GARANTIE) ---
@app.route('/add_asset', methods=('GET', 'POST'))
def add_asset():
    if 'user_id' not in session: return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    error_msg = None

    cur.execute("SELECT location_id, room_name FROM locations")
    locations = cur.fetchall()
    cur.execute("SELECT user_id, first_name, last_name FROM users")
    users = cur.fetchall()

    if request.method == 'POST':
        # 1. Preluare Date
        host_name = request.form['host_name'].strip().upper()
        serial_number = request.form['serial_number'].strip().upper()
        ip_addr = request.form['ip_address'].strip()
        status = request.form['status']
        location_id = request.form['location_id']
        user_id = request.form.get('user_id') if session['role'] == 'admin' else session['user_id']

        # Date Calendaristice (NOU)
        purchase_date = request.form['purchase_date']
        warranty_date = request.form['warranty_date']

        # Daca garantia e goala, o setam pe None (NULL in baza de date)
        if not warranty_date:
            warranty_date = None

        # 2. Validari
        if not re.match(r'^[A-Z0-9-]+$', host_name):
            error_msg = "Host Name invalid! Folosiți doar litere, cifre și cratimă."
        elif not re.match(r'^[A-Z0-9-]+$', serial_number):
            error_msg = "Serial Number invalid! Folosiți doar litere, cifre și cratimă."
        elif ip_addr:
            try:
                ipaddress.ip_address(ip_addr)
            except ValueError:
                error_msg = "Adresă IP invalidă!"

        # 3. Inserare
        if not error_msg:
            try:
                cur.execute("""INSERT INTO assets (host_name, serial_number, ip_address, status, location_id, assigned_user_id, purchase_date, warranty_end_date)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                            (host_name, serial_number, ip_addr, status, location_id, user_id, purchase_date, warranty_date))
                conn.commit()
                cur.close()
                conn.close()
                return redirect('/')
            except psycopg2.errors.UniqueViolation:
                conn.rollback()
                error_msg = "DUPLICAT: Host Name sau Serial Number există deja!"
            except Exception as e:
                conn.rollback()
                error_msg = f"Eroare DB: {e}"

    cur.close()
    conn.close()
    return render_template('add_asset.html', locations=locations, users=users,
                           user_role=session['role'], current_user_id=session['user_id'], error=error_msg)

# --- DELETE ASSET ---
@app.route('/delete_asset/<serial_number>', methods=['POST'])
def delete_asset(serial_number):
    if 'user_id' not in session: return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT assigned_user_id FROM assets WHERE serial_number = %s", (serial_number,))
    asset = cur.fetchone()

    if not asset: return "Nu exista", 404

    if session['role'] == 'admin' or asset['assigned_user_id'] == session['user_id']:
        cur.execute("DELETE FROM assets WHERE serial_number = %s", (serial_number,))
        conn.commit()
    else:
        return "Interzis!", 403

    cur.close()
    conn.close()
    return redirect('/')

# --- DETALII ---
@app.route('/asset/<serial_number>')
def asset_detail(serial_number):
    if 'user_id' not in session: return redirect('/login')

    page = request.args.get('page', 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM assets WHERE serial_number = %s", (serial_number,))
    asset = cur.fetchone()

    if not asset: return "Nu exista", 404

    cur.execute("""SELECT ac.asset_component_id, c.component_type, c.manufacturer, c.model_number, c.details
                   FROM components c JOIN asset_components ac ON c.component_id = ac.component_id
                   WHERE ac.asset_id = %s""", (asset['asset_id'],))
    current_components = cur.fetchall()

    cur.execute("SELECT * FROM components ORDER BY component_type LIMIT %s OFFSET %s", (per_page, offset))
    paginated_components = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM components")
    total_pages = (cur.fetchone()[0] + per_page - 1) // per_page

    cur.close()
    conn.close()

    return render_template('asset_detail.html', asset=asset, components=current_components,
                           all_components=paginated_components, page=page, total_pages=total_pages,
                           user_role=session['role'], current_user_id=session['user_id'])

# --- LINK COMPONENT ---
@app.route('/link_component', methods=['POST'])
def link_component():
    if 'user_id' not in session: return redirect('/login')
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT assigned_user_id FROM assets WHERE asset_id = %s", (request.form['asset_id'],))
    asset_owner = cur.fetchone()['assigned_user_id']

    if session['role'] == 'admin' or asset_owner == session['user_id']:
        try:
            cur.execute("INSERT INTO asset_components (asset_id, component_id) VALUES (%s, %s)",
                        (request.form['asset_id'], request.form['component_id']))
            conn.commit()
        except: conn.rollback()

    conn.close()
    return redirect(url_for('asset_detail', serial_number=request.form['serial_number']))

# --- UNLINK COMPONENT ---
@app.route('/unlink_component', methods=['POST'])
def unlink_component():
    if 'user_id' not in session: return redirect('/login')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM asset_components WHERE asset_component_id = %s", (request.form['asset_component_id'],))
        conn.commit()
    except: conn.rollback()
    finally: conn.close()
    return redirect(url_for('asset_detail', serial_number=request.form['serial_number']))