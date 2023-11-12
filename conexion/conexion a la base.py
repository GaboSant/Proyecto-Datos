import psycopg2 as pg

try:
    conexion = pg.connect(
        host = "localhost",         # Nombre del host (normalmente es localhost)
        database = "postgres",      # nombre de la base donde se guardan los datos
        user = "postgres",          # Nombre del usuario que maneja el servidor (normalmente es postgres)
        password = "123456789",     # Contraseña del servidor
        port = "5432")
    cur = conexion.cursor()
    
    print("tabla ciudad:")
    cur.execute("select * from ciudad")
    rows = cur.fetchall()
    i = 0
    while i != 20:
        print(rows[i])
        i += 1
        
    print("")
        
    print("tabla recurso:")
    cur.execute("select * from recurso")
    rows = cur.fetchall()
    i = 0
    while i != 20:
        print(rows[i])
        i += 1
    
    print("")
    
    print("tabla tiene:")
    cur.execute("select * from tiene")
    rows = cur.fetchall()
    i = 0
    while i != 20:
        print(rows[i])
        i += 1
        
    print("")
    
    print("tabla proyecto:")
    cur.execute("select * from proyecto")
    rows = cur.fetchall()
    for row in rows:
        print(row)
        
    print("")
    
    print("tabla explota:")
    cur.execute("select * from explota")
    rows = cur.fetchall()
    i = 0
    while i != 20:
        print(rows[i])
        i += 1
    
except Exception as ex:
    print(ex)
    
finally:
    if cur is not None:
        cur.close()
    if conexion is not None:
        conexion.close()