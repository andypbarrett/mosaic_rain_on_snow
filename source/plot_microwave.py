"""Plots radar backscatter and microwave brightness temperature series"""
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

import reader
import plotting


RADAR_COLORS = ['tab:red',
                'tab:red',
                'tab:blue',
                'tab:blue',
                'tab:green',
                'tab:green']
RADAR_LINESTYLES = ['-',
                    '--',
                    '-',
                    '--',
                    '-',
                    '--']


def plot_ku(df, ax=None, fig_label=None):
    """Plots Ku radar channels"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    df.plot(ax=ax, color=RADAR_COLORS, style=RADAR_LINESTYLES)
    ax.set_ylim(-35, 10)
    ax.set_ylabel("Backscatter (dB)")
    ax.set_yticks(range(-35,15,5))
    ax.legend(loc="lower left", ncol=2)
    return ax


def plot_ka(df, ax=None, fig_label=None):
    """Plots Ka radar channels"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    df.plot(ax=ax, color=RADAR_COLORS, style=RADAR_LINESTYLES)
    ax.set_ylim(-35, 10)
    ax.set_ylabel("Backscatter (dB)")
    ax.set_yticks(range(-35,15,5))
    ax.legend(loc="lower left", ncol=2)
    return ax


def plot_sbr(df, ax=None, fig_label=None):
    """Plots SBR Tb"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    df.plot(ax=ax, marker='.', linestyle='None')
    ax.set_ylim(150, 300)
    ax.set_ylabel("Brightness Temperature (K)")
    ax.legend(loc="lower left", ncol=2)



def kd_plot(df, ax=None, fig_label=None):
    """Creates kernal density plot panel"""
    if not ax: ax = plt.gca()


def split_kuka(kuka, frequency):
    """Split kuka dataframe into Ku and Ka"""
    df = kuka.loc[:,[frequency in col for col in kuka.columns]]
    df.columns = [c.replace(f"{frequency}_", "") for c in df.columns]
    return df


def plot_microwave():
    kuka = reader.kukadata()
    sbr = reader.sbrdata()

    # For now, split Ku and Ka channels into separate Dataframes
    ku_df = split_kuka(kuka, "Ku")
    ka_df = split_kuka(kuka, "Ka")

    fig = plt.figure(figsize=(7, 9), constrained_layout=True)
    gs = GridSpec(3, 5, figure=fig)
    ax0 = fig.add_subplot(gs[0, :-1])
    plot_ku(ku_df, ax=ax0, fig_label="a) Ku")

    ax1 = fig.add_subplot(gs[1, :-1], sharex=ax0)
    plot_ka(ka_df, ax=ax1, fig_label="c) Ka")

    ax2 = fig.add_subplot(gs[2, :-1], sharex=ax0)
    plot_sbr(sbr, ax=ax2, fig_label="e) SBR")

    # Kernal density plots, following Vishnu's method
    ax3 = fig.add_subplot(gs[0, 4], sharey=ax0)
    kd_plot(ku_df, ax=ax3, fig_label="b)")


    fig.set_constrained_layout_pads(h_pad=0.01)
    plt.show()

    fig.savefig("mosaic_rain_on_snow_microwave.png")
    return


if __name__ == "__main__":
    plot_microwave()
