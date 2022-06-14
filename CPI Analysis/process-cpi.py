#!/usr/bin/env python3

import pandas as pd
import io
import dateutil.parser
from collections import defaultdict
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np

#
# Read CPI CSV.
#
with open("CPIAUCSL.csv") as f:
    cpi = f.read()

cpi = pd.read_csv(io.StringIO(cpi))

#
# Parse out values into a dictionary.
#
cpi_values = defaultdict(dict)
for row in cpi.iterrows():
    date = row[1]["DATE"]
    value = row[1]["CPIAUCSL"]

    dt = dateutil.parser.parse(date)
    year = dt.year
    month = dt.month

    if year < 2015:
        continue

    cpi_values[year][month] = value

#
# Make sure we have CPI values for every month of every year we care about.
#
for year in range(2015, 2022):
    for month in range(1, 13):
        if cpi_values[year][month] is None:
            raise Exception("Missing a CPI")

#
# Get the CPI percent change per month and per year.
#
prev = -1

x_axis = []
year_y_axis = []
month_y_axis = []
cpi_y_axis = []

for year in range(2016, 2023):
    for month in range(1, 13):

        if not month in cpi_values[year]:
            break
        cur = cpi_values[year][month]

        if prev != -1:
            absolute_change = cur - prev
            month_percent_change = float(cur) / prev - 1

            if (year-1) in cpi_values:
                prev_year_value = cpi_values[year-1][month]
                yoy_percent_change = float(cur) / prev_year_value - 1
                x_axis.append(f"{year}-{month}")
                year_y_axis.append(yoy_percent_change)
                month_y_axis.append(month_percent_change)
                cpi_y_axis.append(cur)

        prev = cpi_values[year][month]


def show_xaxis_yearly(ax):
    tick_labels = ax.get_xaxis().get_ticklabels()
    for i in range(0, len(tick_labels)):
        label = tick_labels[i]
        if i % 12 == 0:
            label.set_visible(True)
        else:
            label.set_visible(False)
    tick_labels[-1].set_visible(True)


fig, (ax1, ax2, ax3) = plt.subplots(3, sharex='all')
fig.set_size_inches(10, 10)
fig.suptitle("CPI Analysis")

ax1.title.set_text("CPI Absolute")
ax1.plot(x_axis, cpi_y_axis)

ax2.title.set_text("CPI Year Change")
pprint(year_y_axis)
ax2.plot(x_axis, year_y_axis)

ax3.title.set_text("CPI Month Change")
ax3.plot(x_axis, month_y_axis)
show_xaxis_yearly(ax3)

fig.show()