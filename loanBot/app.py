import sqlite3
from flask import Flask, request, g, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# LOAN_DATABASE = 'loans_toy.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/loans.db'
db = SQLAlchemy(app)

LOAN_MARGIN = 0.02

app.config.from_object(__name__)

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
    thresh = data['threshold']
    invest_amount = data['loan_amount']
    purpose = data['purpose']

    fields = ['id', 'funded_amount', 'profit_loss', 'int_rate', 'grade', 'title', 'purpose', 'desc', 'state']
    loans = Loan.query.filter(
        Loan.funded_amount <= invest_amount,
        Loan.prob > thresh - LOAN_MARGIN,
        Loan.prob < thresh + LOAN_MARGIN
        )
    if purpose != 'any':
        loans = loans.filter(
        Loan.purpose == purpose
        )
    loans = loans.limit(50)
    loan_info = [
        { fld: getattr(loan, fld) for fld in fields}
        for loan in loans
    ]

    return jsonify(loan_data=loan_info)


@app.route('/', methods=('GET','POST'))
@app.route('/loan', methods=('GET','POST'))
def main_page():
    data = request.json
    return render_template("base.html")

def main(host="0.0.0.0", port=9000, debug=True):
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main()
