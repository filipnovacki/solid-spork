from jinja2 import Template

# template = '''
# Ime\t| Prezime
# ---------------------
# {% for ime, prezime in imena -%}
# {{ ime }}\t| {{ prezime}}
# {% endfor %}
# '''

template = open('dictionary.tex.jinja').read()

words = [{
    'name': 'Aardvark',
    'pronunciation':'ahrd-vahrk',
    'pos':'Verb',
    'explanation':'A nocturnal badger-sized burrowing mammal of Africa, with\
    long ears, a tubular snout, and a long extensible tongue, feeding on ants\
    and termites. Also called antbear.'},
    {'name': 'Bardvak',
    'pronunciation':'ahrd-vahrk',
    'pos':'Verb',
    'explanation':'A nocturnal badger-sized burrowing mammal of Africa, with\
    long ears, a tubular snout, and a long extensible tongue, feeding on ants\
    and termites. Also called antbear.'}]

template = Template(template)
rendered = template.render(entries = words)

print(rendered)

