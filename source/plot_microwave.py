"""Plots radar backscatter and microwave brightness temperature series"""
import matplotlib.pyplot as plt

import reader
import plotting


def plot_microwave():
    kuka = reader.kukadata()
    sbr = reader.sbrdata()

    print(kuka.head())
    print(sbr.head())

    return


if __name__ == "__main__":
    plot_microwave()
