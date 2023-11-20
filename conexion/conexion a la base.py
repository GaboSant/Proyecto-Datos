import psycopg2 as pg

def row_print(rows, n):            # funcion para imprimir n filas
    if len(rows) <= n:          # si el numero de filas es menor al que se desean mostrar, se imprime todas
        for row in rows:
            print(row)
    else:                          # si no, se imprimen el numero filas que se desean
        i = 0
        while i != n:
            print(rows[i])
            i += 1

try:
    conexion = pg.connect(
        host = "localhost",         # Nombre del host (normalmente es localhost)
        database = "postgres",      # nombre de la base donde se guardan los datos
        user = "postgres",          # Nombre del usuario que maneja el servidor (normalmente es postgres)
        password = "123456789",     # Contraseña del servidor
        port = "5432")
    cur = conexion.cursor()

    num_filas = 20                  # numero de filas que se desean mostrar
    
    print("tabla ciudad:")
    cur.execute("select * from ciudad")
    rows = cur.fetchall()
    row_print(rows, num_filas)
        
    print("")
        
    print("tabla recurso:")
    cur.execute("select * from recurso")
    rows = cur.fetchall()
    row_print(rows, num_filas)
    
    print("")
    
    print("tabla tiene:")
    cur.execute("select * from tiene")
    rows = cur.fetchall()
    row_print(rows, num_filas)
        
    print("")
    
    print("tabla proyecto:")
    cur.execute("select * from proyecto")
    rows = cur.fetchall()
    row_print(rows, num_filas)
        
    print("")
    
    print("tabla explota:")
    cur.execute("select * from explota")
    rows = cur.fetchall()
    row_print(rows, num_filas)
    
except Exception as ex:
    print(ex)
    
finally:
    if cur is not None:
        cur.close()
    if conexion is not None:
        conexion.close()
