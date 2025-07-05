import web
import sqlite3
import re
import os

# Configuración de URLs
urls = (
    '/', 'Index',
    '/index', 'Index',
    '/insertar', 'Insertar',
    '/detalle/(\d+)', 'Detalle',
    '/editar/(\d+)', 'Editar',
    '/borrar/(\d+)', 'Borrar'
)

# Configuración de templates
render = web.template.render('templates/', base='layout')

# Función para inicializar la base de datos
def init_db():
    try:
        conn = sqlite3.connect('personas.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS personas (
                id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")
        return False

# Función para validar email
def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

# Función para obtener conexión a la base de datos
def get_db_connection():
    try:
        conn = sqlite3.connect('personas.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Error al conectar con la base de datos: {e}")

class Index:
    def GET(self):
        try:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM personas ORDER BY id_persona')
                personas = cursor.fetchall()
                
                if not personas:
                    mensaje = "La base de datos está vacía. No hay registros para mostrar."
                    return render.index(personas=[], mensaje=mensaje)
                
                return render.index(personas=personas, mensaje=None)
            except sqlite3.Error as e:
                mensaje = f"Error al conectar con la tabla Personas: {e}"
                return render.index(personas=[], mensaje=mensaje)
            finally:
                conn.close()
        except Exception as e:
            mensaje = str(e)
            return render.index(personas=[], mensaje=mensaje)

class Insertar:
    def GET(self):
        return render.insertar(error=None)
    
    def POST(self):
        datos = web.input()
        nombre = datos.get('nombre', '').strip()
        email = datos.get('email', '').strip()
        
        # Validaciones
        if not nombre or not email:
            return render.insertar(error="No se permiten registros vacíos. Por favor, complete todos los campos.")
        
        if not validar_email(email):
            return render.insertar(error="El formato del email es incorrecto. Por favor, ingrese un email válido.")
        
        try:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO personas (nombre, email) VALUES (?, ?)', (nombre, email))
                conn.commit()
                raise web.seeother('/index')
            except sqlite3.Error as e:
                return render.insertar(error=f"Error de sintaxis en las consultas con la base de datos: {e}")
            finally:
                conn.close()
        except Exception as e:
            return render.insertar(error=str(e))

class Detalle:
    def GET(self, id_persona):
        try:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM personas WHERE id_persona = ?', (id_persona,))
                persona = cursor.fetchone()
                
                if not persona:
                    mensaje = "Persona no encontrada."
                    return render.detalle(persona=None, mensaje=mensaje)
                
                return render.detalle(persona=persona, mensaje=None)
            except sqlite3.Error as e:
                mensaje = f"Error de sintaxis en las consultas con la base de datos: {e}"
                return render.detalle(persona=None, mensaje=mensaje)
            finally:
                conn.close()
        except Exception as e:
            mensaje = str(e)
            return render.detalle(persona=None, mensaje=mensaje)

class Editar:
    def GET(self, id_persona):
        try:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM personas WHERE id_persona = ?', (id_persona,))
                persona = cursor.fetchone()
                
                if not persona:
                    mensaje = "Persona no encontrada."
                    return render.editar(persona=None, mensaje=mensaje, error=None)
                
                return render.editar(persona=persona, mensaje=None, error=None)
            except sqlite3.Error as e:
                mensaje = f"Error de sintaxis en las consultas con la base de datos: {e}"
                return render.editar(persona=None, mensaje=mensaje, error=None)
            finally:
                conn.close()
        except Exception as e:
            mensaje = str(e)
            return render.editar(persona=None, mensaje=mensaje, error=None)
    
    def POST(self, id_persona):
        datos = web.input()
        nombre = datos.get('nombre', '').strip()
        email = datos.get('email', '').strip()
        
        # Validaciones
        if not nombre or not email:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM personas WHERE id_persona = ?', (id_persona,))
                persona = cursor.fetchone()
                conn.close()
                return render.editar(persona=persona, mensaje=None, error="No se permiten registros vacíos. Por favor, complete todos los campos.")
            except:
                return render.editar(persona=None, mensaje=None, error="Error al recuperar los datos.")
        
        if not validar_email(email):
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM personas WHERE id_persona = ?', (id_persona,))
                persona = cursor.fetchone()
                conn.close()
                return render.editar(persona=persona, mensaje=None, error="El formato del email es incorrecto. Por favor, ingrese un email válido.")
            except:
                return render.editar(persona=None, mensaje=None, error="Error al recuperar los datos.")
        
        try:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('UPDATE personas SET nombre = ?, email = ? WHERE id_persona = ?', 
                             (nombre, email, id_persona))
                conn.commit()
                raise web.seeother('/index')
            except sqlite3.Error as e:
                cursor.execute('SELECT * FROM personas WHERE id_persona = ?', (id_persona,))
                persona = cursor.fetchone()
                return render.editar(persona=persona, mensaje=None, error=f"Error de sintaxis en las consultas con la base de datos: {e}")
            finally:
                conn.close()
        except Exception as e:
            return render.editar(persona=None, mensaje=str(e), error=None)

class Borrar:
    def GET(self, id_persona):
        try:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM personas WHERE id_persona = ?', (id_persona,))
                persona = cursor.fetchone()
                
                if not persona:
                    mensaje = "Persona no encontrada."
                    return render.borrar(persona=None, mensaje=mensaje)
                
                return render.borrar(persona=persona, mensaje=None)
            except sqlite3.Error as e:
                mensaje = f"Error de sintaxis en las consultas con la base de datos: {e}"
                return render.borrar(persona=None, mensaje=mensaje)
            finally:
                conn.close()
        except Exception as e:
            mensaje = str(e)
            return render.borrar(persona=None, mensaje=mensaje)
    
    def POST(self, id_persona):
        try:
            conn = get_db_connection()
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM personas WHERE id_persona = ?', (id_persona,))
                conn.commit()
                raise web.seeother('/index')
            except sqlite3.Error as e:
                cursor.execute('SELECT * FROM personas WHERE id_persona = ?', (id_persona,))
                persona = cursor.fetchone()
                return render.borrar(persona=persona, mensaje=f"Error de sintaxis en las consultas con la base de datos: {e}")
            finally:
                conn.close()
        except Exception as e:
            return render.borrar(persona=None, mensaje=str(e))

if __name__ == "__main__":
    # Crear directorio de templates si no existe
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Inicializar la base de datos
    if init_db():
        print("Base de datos inicializada correctamente.")
    else:
        print("Error al inicializar la base de datos.")
    
    # Habilitar modo debug para ver errores
    web.config.debug = True
    
    app = web.application(urls, globals())
    app.run()