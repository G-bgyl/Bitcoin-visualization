import os
from flask import Flask, render_template, request, redirect
import visualize_dc as vis
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
__file__='/Users/G_bgyl/si507/final_project/visualize_dc.py'
my_path = os.path.dirname(__file__)
currency='BTC'

@app.route("/")
def index():
    ## print the guestbook
    return render_template("index.html") # , entries=model.get_entries()

@app.route("/boxplot")
def boxplot():
    ## add a guestbook entry
    return render_template("boxplot.html")

@app.route("/postentry", methods=["POST"])
def postentry():
    year = request.form["year"]
    boxplot = vis.boxplot(year)
    # print(boxplot)
    df_box_plot = pd.DataFrame(boxplot, columns=['spot_price', 'month'])
    df_box_plot.boxplot(column='spot_price', by='month')
    plt.title('%s Price for %s' % (currency, year))
    plt.suptitle("")
    path_boxplot=my_path + "/static/boxplot_%s.png" % (year)
    plt.savefig(path_boxplot)

    print('path_boxplot:',path_boxplot)
    sub_path="boxplot_%s.png" % (year)
    return render_template("boxplot.html",path=sub_path)

if __name__=="__main__":
    # model.init()
    app.run(debug=True)