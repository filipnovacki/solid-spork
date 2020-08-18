from flask import Flask, render_template, flash, redirect, request

from dictionary.filler import render
from forms import InputDataForm, EnterDictionaryForm
import ZODB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

"""
This is homepage function
"""


@app.route('/')
def hello_world():
    return render_template("app.html")


@app.route('/input', methods=['GET', 'POST'])
def add_to_dictionary():
    form = InputDataForm()

    # returns false if get request
    if form.validate_on_submit():
        from dbapi import add_words
        flash('Adding data to dictionary {}'.format(form.dict_name.data))

        try:
            return redirect('/')
        except:
            pass
        finally:
            add_words(form.input_text.data, form.dict_name.data)

        # return redirect('/')
    return render_template('input_data.html', title='Add to dictionary',
                           form=form)


@app.route('/print_dict', methods=['POST', 'GET'])
def print_dict():
    form = EnterDictionaryForm()
    from dbapi import list_words
    print(list(list_words('1234')))

    if request.method == "POST":
        import dictionary.filler as df
        out = df.sectionise(
            list(
                list_words(form.d_name.data)
            )
        )
        print(render(out))
        return redirect('/')

    # if request.args.get('dict') is not None:
    #     dict_name = request.args.get('dict')
    #     flash('Printing ' + dict_name + '...')
    #     return render_template('/print_dict', dicts=list_words('1234'))
        # start printing process

    # nothing is selected for printing
    return render_template("print_dict.html", dicts=list(list_words('battery')), form=form)
