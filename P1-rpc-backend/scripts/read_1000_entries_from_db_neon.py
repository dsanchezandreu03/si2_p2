import os
import time
import psycopg2


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
   raise RuntimeError("Falta DATABASE_URL en el entorno. Exporta DATABASE_URL antes de ejecutar.")


if "sslmode=" not in DATABASE_URL:
   sep = "&" if "?" in DATABASE_URL else "?"
   DATABASE_URL = DATABASE_URL + f"{sep}sslmode=require"


try:
   conn = psycopg2.connect(DATABASE_URL)
   cursor = conn.cursor()


   cursor.execute("SELECT numero FROM public.tarjeta LIMIT 1000")
   rows = cursor.fetchall()


   search_query = 'SELECT * FROM public.tarjeta WHERE "numero" = %s'


   start_time = time.time()


   for (numero,) in rows:
       cursor.execute(search_query, (numero,))
       cursor.fetchone()


   end_time = time.time()
   print(f"Tiempo invertido en buscar las 1000 entradas una a una: {end_time - start_time:.6f} segundos")


except Exception as e:
   print(f"Error: {e}")


finally:
   try:
       cursor.close()
   except:
       pass
   try:
       conn.close()
   except:
       pass
