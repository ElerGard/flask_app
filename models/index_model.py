import pandas as pd
import random
    
def get_zakazchik(conn):
    return pd.read_sql('Select * from zakazchiki', conn)

def get_zakaz_zakazchika(conn, zakazchkic_id):
    return pd.read_sql(
        '''
            Select 
                t.technika_name as Техника,
                z.data_poluchenia as ДатаПолучения,
                w.worker_FIO as Работник,
                i.data_priezda as ДатаПриезда,
                i.data_vypolneniya as ДатаИсполнения,
                z.nomer_zakaza_id
            from zakazy z
            join technika t on t.technika_id = z.zakazchik_technika_id
            join ispolnenie i on i.nomer_zakaza_id = z.nomer_zakaza_id
            join workers w on w.worker_id = i.worker_id
            where zakazchik_id = :id
            union all
            Select 
                t.technika_name as Техника,
                z.data_poluchenia as ДатаПолучения,
                NULL as Работник,
                i.data_priezda as ДатаПриезда,
                i.data_vypolneniya as ДатаИсполнения,
                z.nomer_zakaza_id
            from zakazy z
            join technika t on t.technika_id = z.zakazchik_technika_id
            join ispolnenie i on i.nomer_zakaza_id = z.nomer_zakaza_id
            where zakazchik_id = :id and i.worker_id is NULL
            order by ДатаПолучения
        ''', 
    conn, params={"id": zakazchkic_id})

def get_new_zakazchik(conn, fio, tel, adr):
    """
    Функция для обработки данных о новом читателе
    """
    cur = conn.cursor()

    cur.execute(
        '''
            insert into zakazchiki(zakazchik_FIO, zakazchik_telephone, zakazchik_address) 
            values (:fio, :tel, :adr)
        ''', {"fio": fio, "tel": tel, "adr": adr})

    conn.commit()

    return cur.lastrowid


def new_zakaz(conn, zakaz_id, zakazchik_id):
    """
    Функция для обработки данных о взятой книге
    """
    cur = conn.cursor()

    cur.executescript(f'''
        insert into zakazy(data_poluchenia, zakazchik_technika_id, zakazchik_id, summa, number_type_oplaty)
        VALUES 
        (date('now'), {zakaz_id},{zakazchik_id}, {random.randrange(1000, 5000, 200)}, 1);
        
        insert into ispolnenie(nomer_zakaza_id) values ((select last_insert_rowid()));
    ''')

    return conn.commit()

def job(conn, zakaz_id) :
    cur = conn.cursor()

    worker_id = pd.read_sql(f'''
        SELECT w.worker_id FROM workers w
        ORDER BY RANDOM()
        LIMIT 1
    ''', conn).values[0][0]

    cur.executescript(f'''
        UPDATE ispolnenie
        SET worker_id = {worker_id}
        WHERE nomer_zakaza_id = {zakaz_id}
    ''')

    return conn.commit()
