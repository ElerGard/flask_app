from app import app
from flask import render_template


@app.route('/new_worker', methods=['get'])
def new_worker():
    html = render_template(
        'new_worker.html',
    )
    return html