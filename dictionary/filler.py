from jinja2 import Template

template = open('dictionary.tex.jinja').read()

dictionary = [{'section':'A', 'words':[{'name':'Aardvark', 'pronunciation':'ahrd-vahrk', 'pos':'Verb',
    'explanation':'A nocturnal badger-sized burrowing mammal of Africa, with\
    long ears, a tubular snout, and a long extensible tongue, feeding on ants\
    and termites. Also called antbear.'}]},
    {'section':'B', 'words':[{'name':'Bardvak', 'pronunciation':'ahrd-vahrk', 'pos':'Verb',
    'explanation':'A nocturnal badger-sized burrowing mammal of Africa, with\
    long ears, a tubular snout, and a long extensible tongue, feeding on ants\
    and termites. Also called antbear.'}]}]

template = Template(template)
rendered = template.render(entries = dictionary)

print(rendered)

