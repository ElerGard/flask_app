import pandas as pd

def get_workers(conn):
    return pd.read_sql('Select * from workers', conn)

def get_new_worker(conn, worker_FIO, worker_dolzhnost):

    cur = conn.cursor()

    cur.execute(
        f'''
            insert into workers(worker_FIO, worker_dolzhnost) 
            values(:fio, :dolsh)
        ''', {"fio": worker_FIO, "dolsh": worker_dolzhnost})

    conn.commit()

    return cur.lastrowid

def get_zakaz_zakazchika(conn, worker_id):
    return pd.read_sql(
        '''
            Select 
                t.technika_name as Техника,
                z.data_poluchenia as ДатаПолучения,
                z2.zakazchik_FIO as Заказчик,
                i.data_priezda as ДатаПриезда,
                i.data_vypolneniya as ДатаИсполнения,
                z.nomer_zakaza_id
            from zakazy z
            join technika t on t.technika_id = z.zakazchik_technika_id
            join ispolnenie i on i.nomer_zakaza_id = z.nomer_zakaza_id
            join zakazchiki z2 on z.zakazchik_id = z2.zakazchik_id
            where i.worker_id = :id
            order by ДатаПолучения
        ''', 
    conn, params={"id": worker_id})
    
def complete(conn, zakaz_id) :
    cur = conn.cursor()

    cur.executescript(f'''
        UPDATE ispolnenie
        SET data_priezda = date('now'), data_vypolneniya = date('now')
        WHERE nomer_zakaza_id = {zakaz_id}
    ''')

    return conn.commit()


