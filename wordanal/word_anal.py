from textblob       import TextBlob
from nltk.corpus    import wordnet as wn
import cmudict

entries = cmudict.dict()

input_text = '''Since the beginning of the internet, millions and millions and millions of \
blogs have been created. Many have died due to lost interest or their owners \
giving up on the idea, while others have thrived and continue to grow, making \
money and earning their owners a steady income. It’s a constant evolution of \
content that keeps people coming back for more, especially if these blogs \
contact highly resourceful material that people fin'''

# Create a map between Treebank and WordNet'''
# WordNet POS tags are: NOUN = 'n', ADJ = 's', VERB = 'v', ADV = 'r', ADJ_SAT = 'a'
# Descriptions (c) https://web.stanford.edu/~jurafsky/slp3/10.pdf
tag_map = {
        'CC':None, # coordin. conjunction (and, but, or)
        'CD':wn.NOUN, # cardinal number (one, two)
        'DT':None, # determiner (a, the)
        'EX':wn.ADV, # existential ‘there’ (there)
        'FW':None, # foreign word (mea culpa)
        'IN':wn.ADV, # preposition/sub-conj (of, in, by)
        'JJ':[wn.ADJ, wn.ADJ_SAT], # adjective (yellow)
        'JJR':[wn.ADJ, wn.ADJ_SAT], # adj., comparative (bigger)
        'JJS':[wn.ADJ, wn.ADJ_SAT], # adj., superlative (wildest)
        'LS':None, # list item marker (1, 2, One)
        'MD':None, # modal (can, should)
        'NN':wn.NOUN, # noun, sing. or mass (llama)
        'NNS':wn.NOUN, # noun, plural (llamas)
        'NNP':wn.NOUN, # proper noun, sing. (IBM)
        'NNPS':wn.NOUN, # proper noun, plural (Carolinas)
        'PDT':[wn.ADJ, wn.ADJ_SAT], # predeterminer (all, both)
        'POS':None, # possessive ending (’s )
        'PRP':None, # personal pronoun (I, you, he)
        'PRP$':None, # possessive pronoun (your, one’s)
        'RB':wn.ADV, # adverb (quickly, never)
        'RBR':wn.ADV, # adverb, comparative (faster)
        'RBS':wn.ADV, # adverb, superlative (fastest)
        'RP':[wn.ADJ, wn.ADJ_SAT], # particle (up, off)
        'SYM':None, # symbol (+,%, &)
        'TO':None, # “to” (to)
        'UH':None, # interjection (ah, oops)
        'VB':wn.VERB, # verb base form (eat)
        'VBD':wn.VERB, # verb past tense (ate)
        'VBG':wn.VERB, # verb gerund (eating)
        'VBN':wn.VERB, # verb past participle (eaten)
        'VBP':wn.VERB, # verb non-3sg pres (eat)
        'VBZ':wn.VERB, # verb 3sg pres (eats)
        'WDT':None, # wh-determiner (which, that)
        'WP':None, # wh-pronoun (what, who)
        'WP$':None, # possessive (wh- whose)
        'WRB':None, # wh-adverb (how, where)
        '$':None, #  dollar sign ($)
        '#':None, # pound sign (#)
        '“':None, # left quote (‘ or “)
        '”':None, # right quote (’ or ”)
        '(':None, # left parenthesis ([, (, {, <)
        ')':None, # right parenthesis (], ), }, >)d useful and interesting.
}

tb = TextBlob(input_text)
words = tb.words

'''Input text, returns list of words'''
def input_text(text):
    return TextBlob(text).words

'''Returns structure of fully explained words'''
def define(word):
    wordsyn = wn.synsets(word)
    '''Couldn't find word'''
    if len(wordsyn) == 0:
        return
    out = { 'pronunciation': [' '.join(a) for a in entries[word.split('.')[0]]],
            'syns': {a.name():(a.definition(), a.examples()) for a in wordsyn}
            }
    return out

for word in words:
    print()
    print(define(word))
