from flask import Flask, render_template, flash, redirect, request, send_file
from dbapi import add_words, get_words, get_dicts_len, remove_dict
from forms import InputDataForm
from graph_drawer import draw_occ_graph, draw_wordlen_graph
from markdown2 import Markdown
import dictionary.filler as df

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


@app.route('/')
def home():
    md = Markdown()
    with open('README.md') as readme:
        txt = readme.read()
        html = md.convert(txt)

    return render_template("index.html", html=html)


@app.route('/input', methods=['GET', 'POST'])
def add_to_dictionary():
    form = InputDataForm()

    if form.validate_on_submit():
        flash('Added data to dictionary {}'.format(form.dict_name.data))
        add_words(form.input_text.data, form.dict_name.data)
        return redirect('/input')

    return render_template('input_data.html', title='Add to dictionary',
                           form=form)


@app.route('/print_dict', methods=['POST', 'GET'])
def print_dict():
    if request.method == "GET" and request.args.get('dict') is not None:
        df.render(df.sectionise(list(get_words(request.args.get('dict')))))
        return send_file('dict.pdf', as_attachment=True)
    return render_template("print_dict.html", dicts=get_dicts_len())


@app.route('/statistics')
def statistics():
    from dbapi import get_dicts
    dicts = get_dicts()
    graphs = []
    for dictionary in dicts:
        graphs.append((draw_occ_graph(dictionary), draw_wordlen_graph(dictionary)))
    return render_template("statistics.html", images=[(g[0].decode('utf8'), g[1].decode('utf8')) for g in graphs])


@app.route('/rm', methods=['GET'])
def del_dictionary():
    if request.method == "GET" and request.args.get('dict') is not None:
        if remove_dict(request.args.get('dict')):
            flash('Dictionary ' + request.args.get('dict') + ' removed from database')
    return redirect('/print_dict')
