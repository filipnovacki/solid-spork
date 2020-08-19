import string

from jinja2 import Template


def sectionise(*input_dict):
    words = []

    for word in input_dict[0]:
        print('Usao sam u ', word, type(word))
        print(list((a.split('.')[0], word.synonyms[a]) for a in word.synonyms))
        #print(list((a.split('.')[0]) for a in word.synonyms))
        try:
            blank_word = {'name': word.name,
                          'pronunciation': word.pronunciation.lower(),
                          #'pos': word.pos,
                          'explanation': list([(a.split('.')[1], word.synonyms[a][0]) for a in word.synonyms])}
                          #'explanation': set((a.split('.')[0].replace("_", " "), word.synonyms[a][0]) for a in word.synonyms)}
                #[str(a.split('.'[1])) + ' ' + str(int(a.split('.')[2])) + ". " + word.synonyms[a][0] for a in
                #word.synonyms])}
        except AttributeError as e:
            print(str(e))
            continue
        except:
            blank_word = {'name': word.name,
                          'pronunciation': word.pronunciation.lower(),
                          #'pos': None,
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
    f = open('cover.tex', 'w')
    f.write(tex_string)
    f.close()
    return
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


def render(dictionary):
    template = open('dictionary/dictionary.tex.jinja').read()

    '''
    dictionary = [{'section': 'A', 'words': [{'name': 'Aardvark',
                                              'pronunciation': 'ahrd-vahrk',
                                              'pos': 'Verb',
                                              'explanation': 'A nocturnal badger-sized burrowing mammal of Africa, with\
        long ears, a tubular snout, and a long extensible tongue, feeding on ants\
        and termites. Also called antbear.'},
                                            ]
                  },
                  {'section': 'B', 'words': [{  'name': 'Bardvak',
                                                'pronunciation': 'ahrd-vahrk',
                                                'pos': 'Verb',
                                                'explanation': 'A nocturnal badger-sized burrowing mammal of Africa, with\
        long ears, a tubular snout, and a long extensible tongue, feeding on ants\
        and termites. Also called antbear.'},
                                            ]
                    }
            ] '''

    template = Template(template)
    rendered = template.render(entries=dictionary)

    generate_pdf(rendered)
