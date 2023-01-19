import pandas as pd

def get_proizvoditel(conn):
    return pd.read_sql(
        '''
            Select p.firma_id, p.proizvoditel_name, count(t.firma_id) 
            from technika t
            join proizvoditeli p on t.firma_id = p.firma_id
            group by t.firma_id
            ''', 
    conn)

def convert(list):
    # Converting integer list to string list
    s = [str(i) for i in list]

    # Join list items using join()
    res = ",".join(s)

    return res

def card(conn, proizvoditel):
    proizvoditel = convert(proizvoditel)

    return pd.read_sql(f'''
        select 
            t.technika_name as Название,
            p.proizvoditel_name as Производитель, 
            t.technika_model as Модель,
            t.technika_id as ID
        from technika t 
        join proizvoditeli p on t.firma_id = p.firma_id
        group by t.technika_id
        having (t.firma_id in ({proizvoditel}) OR ({not proizvoditel}))
    ''', conn)
