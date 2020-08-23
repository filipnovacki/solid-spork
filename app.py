from flask import Flask, render_template, flash, redirect, request, send_file

from dbapi import get_dicts
from forms import InputDataForm
from graph_drawer import draw_occ_graph, draw_wordlen_graph

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/')
def home():
    if request.args.get('new') == "yes":
        import dbapi
        dbapi.start_db()

    from markdown2 import Markdown
    md = Markdown()
    with open('README.md') as readme:
        txt = readme.read()
        html = md.convert(txt)


    return render_template("index.html", html=html)


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
    from dbapi import get_words, get_dicts_len

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

    return render_template("print_dict.html", dicts=get_dicts_len())


@app.route('/statistics')
def statistics():
    dicts = (get_dicts())
    graphs = []
    for dictionary in dicts:
        graphs.append((draw_occ_graph(dictionary), draw_wordlen_graph(dictionary)))
    import time
    return render_template("statistics.html", images=[(g[0].decode('utf8'), g[1].decode('utf8')) for g in graphs],
                           time=str(int(time.time())))

@app.route('/rm', methods=['GET'])
def del_dictionary():
    from dbapi import remove_dict
    if request.method == "GET" and request.args.get('dict') is not None:
        if remove_dict(request.args.get('dict')):
            flash('Dictionary ' + request.args.get('dict')+ ' removed from database')

    return redirect('/print_dict')
