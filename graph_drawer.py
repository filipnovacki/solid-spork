from dbapi import get_word_count, get_dicts
import pandas as pd
import matplotlib.pyplot as plt


def draw_graph(dictionary):
    wc = get_word_count(dictionary)
    df = pd.DataFrame(wc).groupby('count').count()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('Word occurrences')
    ax1.set_ylabel('Word number')

    plt.grid(True)
    plt.plot(df)
    plt.savefig('templates/graphs/' + dictionary + 'wc.png')
