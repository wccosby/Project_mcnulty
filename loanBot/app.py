import sqlite3


from flask import Flask, request, g, jsonify, request, render_template
app = Flask(__name__)

LOAN_DATABASE = 'loans_toy.sqlite'

app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['LOAN_DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query,args)
    rows = cur.fetchall()
    cur.close()
    return rows

@app.route('/viewhead')
def view_head():
    rows = execute_query("""SELECT binary_profit_loss,profit_loss FROM loans LIMIT(10);""")
    return '<br>'.join(str(row) for row in rows)


@app.route('/')
def main_page():
    return render_template("base.html")

if __name__ == '__main__':
  app.run(debug=True)
