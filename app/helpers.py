import csv
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def csv_reader(filename):
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        fields = next(csvreader)
        rows=[]
        for row in csvreader:
            rows.append(row)
    return fields, rows

def scatterplot(fields, rows, xcol, ycol, fit):
    cols = np.array(rows).T
    img = BytesIO()
    xvals = np.array([float(val) for val in cols[xcol]])
    yvals = np.array([float(val) for val in cols[ycol]])
    plt.scatter(xvals,yvals)
    plt.xlabel(fields[xcol])
    plt.ylabel(fields[ycol])
    coeff = [0.]
    if fit == "lin":
        coeff = np.polyfit(xvals, yvals, 1)
        plt.plot(xvals, coeff[0]*xvals + coeff[1], color = "g")
    elif fit == "quad":
        coeff= np.polyfit(xvals, yvals, 2)
        plt.plot(xvals, coeff[0]*xvals*xvals + coeff[1]*xvals + coeff[2] , color = "g")
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url, np.around(coeff,2)

def barplot(fields, rows, xcol, ycol):
    cols = np.array(rows).T
    img = BytesIO()
    xvals = cols[xcol]
    yvals = [float(val) for val in cols[ycol]]
    plt.bar(xvals,yvals)
    plt.xlabel(fields[xcol])
    plt.ylabel(fields[ycol])
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    return plot_url
