import string

from jinja2 import Template
from nltk.corpus import wordnet as wn


def start_test(word):
    wordsyn = wn.synset(word)
    return wordsyn
    return sectionise(wn.synset(word))


def sectionise(*input_dict):
    # sectioned {
    words = []

    for word in input_dict:
        try:
            blank_word = {'name': word.name,
                          'pronunciation': word.pronunciation,
                          'pos': word.pos,
                          'explanation': word.syns}
        except:
            blank_word = {'name': word.name,
                          'pronunciation': word.pronunciation,
                          'pos': None,
                          'explanation': None}

        words.append(blank_word)

    sectioned = [{'section': x, 'words': [y for y in words if y['name'][0] == x or y['name'][0] == x.lower()]} for x in string.ascii_letters[26:]]

    return sectioned


def render(dictionary):
    template = open('dictionary.tex.jinja').read()

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

    print(rendered)


