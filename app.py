import datetime
import os

from flask import Flask, render_template, redirect, url_for
from forms import ItemForm
from models import Items
from database import db_session

app = Flask(__name__)
app.secret_key = os.environ['APP_SECRET_KEY']

@app.route("/", methods=('GET', 'POST'))
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Items(name=form.name.data, quantity=form.quantity.data, description=form.description.data, date_added=datetime.datetime.now())
        db_session.add(item)
        db_session.commit()
        return redirect(url_for('success'))
    return render_template('index.html', form=form)

@app.route("/success")
def success():
    all_records = []
    qry = db_session.query(Items)
    for row in qry.all():
        this_record = []
        this_record.append(row.name)
        this_record.append(row.quantity)
        this_record.append(row.description)
        this_record.append(str(row.date_added))
        all_records.append(this_record)
    return str(all_records)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
