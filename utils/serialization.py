def converter(data: dict) -> str:
    table_name = data['table_name']
    fields = data['fields']

    sql = f'CREATE TABLE {table_name} (db_id INTEGER PRIMARY KEY, '
    for item in fields:
        sql += f"{item['column_name']} {item['column_type']}, "

    return sql[:-2].join(' )').strip()
