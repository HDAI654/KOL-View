import sqlite3

class PR:
    def Style():
        with open("Assets/Databases/style.css", 'r') as c:
            return str(c.read())

    def Select(db, fields, table, where):
        con = sqlite3.connect(db)
        cur = con.cursor()
        data = list(cur.execute(f"SELECT {fields} FROM {table} WHERE {where}").fetchall())
        return data
    
    def Delete(db, table, where):
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(f"DELETE FROM {table} WHERE {where}")
        con.commit()
        con.close()
        return True
    
    def Insert(db, table, fields, values):
        con = sqlite3.connect(db)
        cur = con.cursor()
        cur.execute(f"INSERT INTO {table} ({fields}) VALUES ({values})")
        con.commit()
        con.close()
        return True
    
    def Update(db, table, set_fields, where):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"UPDATE {table} SET {set_fields} WHERE {where}")
        conn.commit()
        conn.close()
        return True
    
    def SQL_Table_to_custom_data(db_address, table_name, table_custom_name=None):
        table_name = table_name
        if table_custom_name is None:
            table_name = table_custom_name
        conn = sqlite3.connect(db_address)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        
        table = {
            "Table_name": table_name,
            "Columns": [],
            "Rows_data": [],
        }
        
        # get column names
        fields = []
        cursor.execute("SELECT * FROM {} LIMIT 0".format(table_name))
        column_names = [description[0] for description in cursor.description]
        # get column types
        for column_name in column_names:
            # get column type
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns_info = cursor.fetchall()
            col_type = str(columns_info[column_names.index(column_name)][2]).upper()
            col_pk = columns_info[column_names.index(column_name)][5]
            col_notnull = int(columns_info[column_names.index(column_name)][3])
            if col_notnull == 1:
                col_notnull = 1
            else:
                col_notnull = 0
            """print(column_name)
            print(col_type)
            print('---------')"""
            
            if col_pk == 1:
                col_type = "PRIMARY"   
            elif col_type in ["INTEGER", "REAL", "NUMERIC", "INT", "FLOAT", "DOUBLE", "SMALLINT", "BIGINT", "DECIMAL", "TINYINT", "BLOB", "BOOLEAN"]:
                col_type = "INTEGER"
            elif col_type in ["TEXT", "VARCHAR", "CHAR", "NVARCHAR", "NCHAR", "CLOB", "TEXT", "STRING"]:
                col_type = "STRING" 
            elif col_type in ["DATE"]:
                col_type = "DATE" 
            elif col_type in ["EMAIL"]:
                col_type = "EMAIL" 
            else:
                col_type = "FREE"
            fields.append([str(column_name), str(col_type), int(col_notnull)])
            
        table["Columns"] = fields
        
        # get rows data
        rows_data = []
        for row in data:
            rows_data.append(list(row))
        table['Rows_data'] = rows_data
        
        conn.close()
        return table
    
    def Get_Fields_of_a_table(db, table):
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table} LIMIT 1")
        fields_name = [str(field[0]) for field in cur.description]
        cur.close()
        conn.close()
        return fields_name
    
    def Filter(search_text, filter_text):
        lst = len(search_text)
        if str(search_text).strip() == str(filter_text)[0:int(lst)].strip() :
            return True
        else:
            return False
    
    