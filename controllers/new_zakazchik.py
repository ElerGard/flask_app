from app import app
from flask import render_template


@app.route('/new_zakazchik', methods=['get'])
def new_zakazchik():
    html = render_template(
        'new_zakazchik.html',
    )
    return html