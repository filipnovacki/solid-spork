from dbapi import get_word_count, get_dicts, get_word_names
import pandas as pd
import matplotlib.pyplot as plt


def draw_occ_graph(dictionary):
    wc = get_word_count(dictionary)
    df = pd.DataFrame(wc).groupby('count').count()

    with plt.xkcd():
        fig = plt.figure()

        ax1 = fig.add_subplot(111)
        ax1.set_xlabel('Word occurrences')
        ax1.set_ylabel('Word number')
        ax1.set_yscale('log', basey=2)

        plt.tight_layout()
        plt.grid(True)
        plt.plot(df)
        plt.savefig('static/' + dictionary + 'wc.png')


def draw_wordlen_graph(dictionary):
    df = pd.DataFrame(get_word_names(dictionary))
    wlen = lambda x: len(x)
    df['wlen'] = df[0].apply(wlen)
    df = df.groupby('wlen').count()

    with plt.xkcd():
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.set_xlabel('Word length')
        ax1.set_ylabel('Number of occurrences')

        plt.tight_layout()
        plt.grid(True)
        plt.plot(df)
        plt.savefig('static/' + dictionary + 'wl.png')
