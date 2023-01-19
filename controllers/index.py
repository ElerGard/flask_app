from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.index_model import get_zakazchik, get_zakaz_zakazchika, get_new_zakazchik, new_zakaz, job


@app.route('/', methods=['get'])
def index():
    conn = get_db_connection()

    if request.values.get('zakazchik'):
        zakazchik_id = int(request.values.get('zakazchik'))
        session['zakazchik_id'] = zakazchik_id
    elif request.values.get('new_zakazchik'):
        new_zakazchik = request.values.get('new_zakazchik')
        new_za = request.values.get('new_za')
        new_zaka = request.values.get('new_zaka')
        session['zakazchik_id'] = get_new_zakazchik(conn, new_zakazchik, new_za, new_zaka)
    elif request.values.get('job'):
        job_id = int(request.values.get('job'))
        job(conn, job_id)
    elif request.values.get('take'):
        book_id = int(request.values.get('take'))
        new_zakaz(conn, book_id, session['zakazchik_id'])
    else:
        session['zakazchik_id'] = 1

    df_zakazchiki = get_zakazchik(conn)
    df_zakazi = get_zakaz_zakazchika(conn, session['zakazchik_id'])

    # выводим форму
    html = render_template(
        'index.html',
        zakazchik_id=session['zakazchik_id'],
        zakazchiki=df_zakazchiki,
        zakazi=df_zakazi,
        len=len
    )
    return html
