import base64
import io

import matplotlib.pyplot as plt
import pandas as pd

from dbapi import get_word_count, get_word_names


def draw_occ_graph(dictionary):
    wc = get_word_count(dictionary)
    df = pd.DataFrame(wc).groupby('count').count()

    with plt.xkcd():
        fig = plt.figure()

        ax1 = fig.add_subplot(111)
        ax1.set_xlabel('Word occurrences')
        ax1.set_ylabel('Word number')
        ax1.set_title(dictionary + " - graph ")
        ax1.set_yscale('log', basey=2)

        plt.tight_layout()
        plt.grid(True)
        plt.plot(df)

        output = io.BytesIO()
        plt.savefig(output, format='png')
        output.seek(0)
        fig_png = base64.b64encode(output.getvalue())

        plt.close()
        return fig_png



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
        ax1.set_title(dictionary + " - graph ")

        plt.tight_layout()
        plt.grid(True)
        plt.plot(df)

        output = io.BytesIO()
        plt.savefig(output, format='png')
        output.seek(0)
        fig_png = base64.b64encode(output.getvalue())

        plt.close()
        return fig_png
