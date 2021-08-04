"""Plots radar backscatter and microwave brightness temperature series"""
import matplotlib.pyplot as plt

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
    ax.legend(loc="lower left")
    return ax


def plot_ka(df, ax=None, fig_label=None):
    """Plots Ka radar channels"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    df.plot(ax=ax, color=RADAR_COLORS, style=RADAR_LINESTYLES)
    ax.set_ylim(-35, 10)
    ax.set_ylabel("Backscatter (dB)")
    ax.legend(loc="lower left")
    return ax


def plot_sbr(df, ax=None, fig_label=None):
    """Plots SBR Tb"""
    if not ax: plt.gca()
    plotting.add_panel(ax=ax, fig_label=fig_label)
    df.plot(ax=ax)
    ax.legend(loc="lower left")


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

    fig, ax = plt.subplots(3, 1, figsize=(7, 9),
                           sharex=True,
                           constrained_layout=True)
    plot_ku(ku_df, ax=ax[0], fig_label="a) Ku")
    plot_ka(ka_df, ax=ax[1], fig_label="b) Ka")
    plot_sbr(sbr, ax=ax[2], fig_label="c) SBR")
    
    plt.show()
    fig.savefig("mosaic_rain_on_snow_microwave.png")
    return


if __name__ == "__main__":
    plot_microwave()
