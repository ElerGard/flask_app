from app import app
from flask import render_template, request
from utils import get_db_connection
from models.search_model import get_proizvoditel, card


@app.route('/search', methods=['get', 'post'])
def search():
    conn = get_db_connection()
    df_proizvoditel = get_proizvoditel(conn)

    if request.form.get('clear'):
        proizvoditels = []
    else:
        proizvoditels = [int(item) for item in request.form.getlist('firma_id')]

    df_card = card(conn, proizvoditels)

    html = render_template(
        'search.html',
        proizvoditel=df_proizvoditel,
        card=df_card,
        proizvoditels=proizvoditels,
        len=len
    )
    return html
