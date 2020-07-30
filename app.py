from flask import Flask, render_template, flash, redirect, request
from forms import InputDataForm
from dbapi import open_conn, add_dictionary, get_dictionaries
from bookkeep import Dictionary
import ZODB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

"""
This is homepage function
"""
@app.route('/')
def hello_world():
    return render_template("app.html", dicts = get_dictionaries())


"""
Page for word input into dictionaries
"""
@app.route('/input', methods=['GET', 'POST'])
def add_to_dictionary():
    form = InputDataForm()

    # returns false if get request
    if form.validate_on_submit():
        flash('Adding data to dictionary {}'.format(form.dict_name.data))

        dict = Dictionary(form.dict_name.data)
        dict.add_words(form.input_text.data)

        add_dictionary(dict)

        return redirect('/')
    return render_template('input_data.html', title='Add to dictionary',
                           form=form)


"""
Page for dictionaries printing
"""
@app.route('/print_dict')
def print_dict():

    # if files are selected for printing
    if request.args.get('dict') is not None:
        dict_name = request.args.get('dict')
        flash('Printing ' + dict_name + '...')
        return redirect('/print_dict')
        # start printing process

    # nothing is selected for printing
    return render_template("print_dict.html", dicts = get_dictionaries())
