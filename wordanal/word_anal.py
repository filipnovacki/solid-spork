from textblob import TextBlob
from nltk.corpus import wordnet

input_text = '''Since the beginning of the internet, millions and millions and millions of \
blogs have been created. Many have died due to lost interest or their owners \
giving up on the idea, while others have thrived and continue to grow, making \
money and earning their owners a steady income. It’s a constant evolution of \
content that keeps people coming back for more, especially if these blogs \
contact highly resourceful material that people find useful and interesting.'''

tb = TextBlob(input_text)
words = tb.words


for word in words:
    wordsyn = wordnet.synsets(word)
    if len(wordsyn) == 0:
        continue
    print('\n====================')
    print(word)
    print('====================')
    for w in wordsyn:
        print(w.name().split('.')[0], w.pos(), w.definition(), w.examples())

