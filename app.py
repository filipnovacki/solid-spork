from flask import Flask, render_template, flash, redirect, request, send_file
from forms import InputDataForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/')
def home():
    return render_template("app.html")


@app.route('/input', methods=['GET', 'POST'])
def add_to_dictionary():
    form = InputDataForm()

    if form.validate_on_submit():
        from dbapi import add_words
        flash('Adding data to dictionary {}'.format(form.dict_name.data))

        try:
            return redirect('/')
        except:
            pass
        finally:
            add_words(form.input_text.data, form.dict_name.data)

    return render_template('input_data.html', title='Add to dictionary',
                           form=form)


@app.route('/print_dict', methods=['POST', 'GET'])
def print_dict():
    from dbapi import get_words, get_dicts

    if request.method == "GET" and request.args.get('dict') is not None:
        import dictionary.filler as df
        df.render(
            df.sectionise(
                list(
                    get_words(request.args.get('dict'))
                )
            )
        )
        return send_file('dict.pdf', as_attachment=True)

    return render_template("print_dict.html", dicts=get_dicts())
