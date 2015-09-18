import matplotlib.pyplot as plt
import numpy as np
import io

def rainfall_bar_chart(vals, labels, title):
        x = np.arange(len(labels))
        barwidth = 0.8

        fig = plt.figure()
        ax = plt.subplot(111)
        ax.bar(x, vals, width=barwidth)
        ax.set_xticks(x + barwidth/2.)
        ax.set_xticklabels(labels)
        ax.set_title(title)
        ax.set_ylabel("rainfall (mm)")

        bytestream = io.BytesIO()
        fig.savefig(bytestream, format="png")
        plt.close(fig)
        bytestream.seek(0)
        return bytestream
