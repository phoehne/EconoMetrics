import pandas as pd
from pandas import DataFrame, Series
import pandas.io.data as web
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Wedge
from matplotlib.patches import Arrow
from matplotlib.lines import Line2D


def macd(ax, quotes_df, width=0.6, sigcolor='r', macdcolor='b', histcolor='0.60', signame='Signal', macdname='MACD', histname='Histogram'):
    lines = []
    patches = []
    offset = width/2.0

    for i in range(1, len(quotes_df)):
        cur_sig = quotes_df[signame][i-1]
        nxt_sig = quotes_df[signame][i]

        cur_macd = quotes_df[macdname][i-1]
        nxt_macd = quotes_df[macdname][i]

        cur_hist = quotes_df[histname][i]

        sig_ln = Line2D(xdata=(i-1, i), ydata=(cur_sig, nxt_sig), color=sigcolor, linewidth=0.5, 
                        antialiased=True)
        macd_ln = Line2D(xdata=(i-1, i), ydata=(cur_macd, nxt_macd), color=macdcolor, linewidth=0.5, 
                         antialiased=True)
        
        if(cur_hist > 0):
            rect = Rectangle(xy=(i-offset,0), width=width, height=cur_hist, facecolor=histcolor, 
                             edgecolor=histcolor, linewidth=0.5, antialiased=True) 
        else:
            rect = Rectangle(xy=(i-offset,cur_hist), width=width, height=(-cur_hist), 
                             facecolor=histcolor, edgecolor=histcolor, linewidth=0.5, antialiased=True)

        lines.append(sig_ln)
        lines.append(macd_ln)
        patches.append(rect)

        ax.add_line(sig_ln)
        ax.add_line(macd_ln)
        ax.add_patch(rect)

    ax.set_xlim(0, len(quotes_df))
    ax.grid(axis='x', color='0.4', aa=True)
    ax.autoscale_view()
    return lines,patches

def candlestick(ax, quotes_df, width=0.2, colorup='w', colordown='k', alpha=1.0):
    lines = []
    patches = []
    offset = width/2.0

    for i in range(len(quotes_df)):
        pr_open = quotes_df['Open'][i]
        pr_high = quotes_df['High'][i]
        pr_low =  quotes_df['Low'][i]
        pr_close = quotes_df['Close'][i]

        if pr_close >= pr_open:
            color = colorup
            lower = pr_open
            upper = pr_close
            height = pr_close - pr_open
        else:
            color = colordown
            lower = pr_close
            upper = pr_open
            height = pr_open - pr_close

        vline  = Line2D(xdata=(i, i), ydata=(pr_low, lower), color='k', linewidth=0.5, antialiased=True)
        vline2 = Line2D(xdata=(i, i), ydata=(upper, pr_high), color='k', linewidth=0.5, antialiased=True)
        rect = Rectangle(xy=(i - offset, lower), width=width, height=height, facecolor=color, 
                         edgecolor='k', linewidth=0.5)
        rect.set_alpha(alpha)

        lines.append(vline)
        lines.append(vline2)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_line(vline2)
        ax.add_patch(rect)
    ax.set_xlim(0, len(quotes_df))
    ax.grid(axis='x', color='0.4', aa=True)
    ax.autoscale_view()
    return lines, patches

def highlow(ax, quotes_df, width=0.6, relhighcolor='g', rellowcolor='r', boxheight=0.6, relname="HighLow", highvalue="High", lowvalue="Low"):
    patches = []
    offset = width/2.0

    maxHigh = quotes_df[highvalue].max()
    minLow = quotes_df[lowvalue].min()
    dy = (maxHigh - minLow)/30.0

    for i in range(1, len(quotes_df)):
        wedge = None
        if quotes_df[relname][i] == highvalue:
            wedge = Arrow(x=i, y=quotes_df[highvalue][i] + 0.05, dx=0, dy=dy, width=(width * 3.0), fc=relhighcolor, ec=relhighcolor, aa=True)
        elif quotes_df[relname][i] == lowvalue:
            wedge = Arrow(x=i, y=quotes_df[lowvalue][i] - 0.05, dx=0, dy=-dy, width=(width * 3.0), fc=rellowcolor, ec=rellowcolor, aa=True)

        if wedge:
            patches.append(wedge)
            ax.add_patch(wedge)

    ax.set_xlim(0, len(quotes_df))
    ax.autoscale_view()
    return patches

