from flask import Flask, request, redirect
import psycopg2

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(host='db-dillan', port='5432', user='admin', password='adminpass', dbname='yavirac_db')

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS usuarios (id SERIAL PRIMARY KEY, nombre VARCHAR(100), correo VARCHAR(100));')
    conn.commit()
    cur.close()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        if nombre and correo:
            cur.execute('INSERT INTO usuarios (nombre, correo) VALUES (%s, %s);', (nombre, correo))
            conn.commit()
        cur.close()
        conn.close()
        return redirect('/')
    cur.execute('SELECT id, nombre, correo FROM usuarios ORDER BY id DESC;')
    filas = cur.fetchall()
    cur.close()
    conn.close()
    rows_html = ''.join([f'<tr><td>{f[0]}</td><td>{f[1]}</td><td>{f[2]}</td></tr>' for f in filas])
    return f'''<div style="font-family:Arial;max-width:600px;margin:40px auto;text-align:center"><h1>Flask + PostgreSQL en Docker</h1><h2>Estudiante: Dillan Alvarez</h2><h3 style="color:#0056b3">Yo estudio en Yavirac</h3><p style="color:green">Conectado a BD: <b>yavirac_db</b></p><form method="POST" style="margin:20px 0;padding:15px;border:1px solid #ccc;border-radius:8px"><input type="text" name="nombre" placeholder="Nombre completo" required style="padding:8px;margin:5px;width:220px"><input type="email" name="correo" placeholder="Correo electronico" required style="padding:8px;margin:5px;width:220px"><br><button type="submit" style="padding:10px 20px;margin-top:10px;background:#0056b3;color:white;border:none;border-radius:5px;cursor:pointer">Guardar en PostgreSQL</button></form><table border="1" cellpadding="8" cellspacing="0" style="width:100%;border-collapse:collapse"><tr style="background:#f2f2f2"><th>ID</th><th>Nombre</th><th>Correo</th></tr>{rows_html}</table></div>''', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
