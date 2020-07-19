from flask import Flask, render_template, flash, redirect
from forms import InputDataForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/')
def hello_world():
    return render_template("app.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = InputDataForm()

    # returns false if get request
    if form.validate_on_submit():
        flash('Adding data to dictionary {}'.format(form.dict_name.data))
        return redirect('/')
    return render_template('input_data.html', title='Add to dictionary',
            form=form)

