import string

from jinja2 import Template


def sectionise(*input_dict):
    words = []

    for word in input_dict[0]:
        try:
            blank_word = {'name': word.name,
                          'pronunciation': word.pronunciation.lower(),
                          'explanation': list([(a.split('.')[1], word.synonyms[a][0]) for a in word.synonyms])}
        except AttributeError as e:
            print(str(e))
            continue
        except:
            blank_word = {'name': word.name,
                          'pronunciation': word.pronunciation.lower(),
                          'explanation': None}

        words.append(blank_word)

    sectioned = [
        {
            'section': x,
            'words': [y for y in words if not y['name'].isdigit() and (y['name'][0] == x or y['name'][0] == x.lower())]
        } for x in (string.ascii_letters[26:])
    ]

    return sectioned


def generate_pdf(tex_string, pdfname='dict.pdf'):
    import subprocess
    import os
    import tempfile
    import shutil
    current = os.getcwd()
    temp = tempfile.mkdtemp()
    os.chdir(temp)

    f = open('cover.tex', 'w')
    f.write(tex_string)
    f.close()

    proc = subprocess.Popen(['pdflatex', 'cover.tex'])
    subprocess.Popen(['pdflatex', tex_string])
    proc.communicate()

    os.rename('cover.pdf', pdfname)
    shutil.copy(pdfname, current)
    shutil.rmtree(temp)
    os.chdir(current)


def render(dictionary):
    template = open('dictionary/dictionary.tex.jinja').read()
    template = Template(template)
    rendered = template.render(entries=dictionary)
    generate_pdf(rendered)
