from app import app
from flask import render_template, request, session
from utils import get_db_connection
from models.worker_model import get_workers, get_zakaz_zakazchika, complete, get_new_worker

@app.route('/workers', methods=['get'])
def workers():
    conn = get_db_connection()
    
    if request.values.get('worker'):
        worker_id = int(request.values.get('worker'))
        session['worker_id'] = worker_id
    elif request.values.get('worker_FIO'):
        worker_FIO = request.values.get('worker_FIO')
        worker_dolzhnost = request.values.get('worker_dolzhnost')
        session['worker_id'] = get_new_worker(conn, worker_FIO, worker_dolzhnost)
    elif request.values.get('complete'):
        job_id = int(request.values.get('complete'))
        complete(conn, job_id)
    else:
        session['worker_id'] = 1
        
    df_workers = get_workers(conn)
    df_zakazi = get_zakaz_zakazchika(conn, session['worker_id'])
        
    html = render_template(
        'workers.html',
        worker_id=session['worker_id'],
        workers=df_workers,
        zakazi=df_zakazi,
        len=len
    )
    return html
