import sqlite3
from flask import Response
import json

from flask import Flask, request, g, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# LOAN_DATABASE = 'loans_toy.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/loans.db'
db = SQLAlchemy(app)

app.config.from_object(__name__)


# def connect_to_database():
#     return sqlite3.connect(app.config['LOAN_DATABASE'])
#
# def get_db():
#     db = getattr(g, 'db', None)
#     if db is None:
#         db = g.db = connect_to_database()
#     return db
#
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()
#
# def execute_query(query, args=()):
#     cur = get_db().execute(query,args)
#     rows = cur.fetchall()
#     cur.close()
#     return rows
#
# @app.route('/viewhead')
# def view_head():
#     rows = execute_query("""SELECT binary_profit_loss,profit_loss FROM loans LIMIT(10);""")
#     return '<br>'.join(str(row) for row in rows)

class Loan(db.Model):
    __tablename__ = 'loans'
    id = db.Column('index', db.Integer, primary_key=True)
    funded_amount = db.Column('funded_amnt', db.Float)
    profit_loss = db.Column('profit_loss', db.Float)
    funded_amount = db.Column('funded_amnt', db.Float)
    pred = db.Column('pred', db.Float)
    prob = db.Column('prob', db.Float)
    int_rate = db.Column('int_rate', db.Float)
    grade = db.Column('grade', db.Text)
    title = db.Column('title', db.Text)
    purpose = db.Column('purpose', db.Text)
    desc = db.Column('desc', db.Text)
    state = db.Column('addr_state', db.Text)
    profitable = db.Column('binary_profit_loss', db.Integer)




@app.route("/lend/", methods=["POST"])
def get_loans():
    """
    Accepts a POST request with the user's loan parameters, e.g. risk threshold, loan purpose, geo, etc.
    Makes an SQL query to the database and retrieves loans to be recommended.
    """
    data = request.json
    data_simp = data['example']
    print("THIS IS THE DATA: ", data_simp)
    thresh = data_simp[1]
    # thresh=0.5
    invest_amount = data_simp[0]
    # invest_amount = 10000
    # num_loans = data['num_loans']

    fields = ['id', 'funded_amount', 'profit_loss', 'int_rate', 'grade', 'title', 'purpose', 'desc', 'state']
    # fields = ['grade']

    loans = Loan.query.filter(
        Loan.funded_amount <= invest_amount,
        Loan.prob > thresh
        # Loan.profitable == 1
        ).limit(100)
    loan_info = [
        { fld: getattr(loan, fld) for fld in fields}
        for loan in loans
    ]
    print("THE LOANS~~~~   ",loan_info[0]['purpose'])
    # loan_info={"profit_loss":loans['profit_loss']}
    # print(jsonify(loan_info))
    return Response(json.dumps(loan_info),  mimetype='application/json')



@app.route('/', methods=('GET','POST'))
def main_page():
    data = request.json
    return render_template("base.html")

if __name__ == '__main__':
  app.run(debug=True)
