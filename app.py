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

    return render_template("index.html")

@app.route("/boxplot")
def boxplot():
    title = 'price fluctuation'
    action = 'box_input'
    return render_template("plot.html",title=title,action=action)

@app.route("/area")
def area():
    title='current price depth'
    action = 'area_input'
    return render_template("plot.html",title=title,action=action)

@app.route("/bar")
def bar():
    title='changing rate'
    action = 'bar_input'
    return render_template("plot.html",title=title,action=action)

@app.route("/line")
def line():
    title='trend'
    action = 'line_input'
    return render_template("plot.html",title=title,action=action)

@app.route("/box_input", methods=["POST"])
def box_input():
    title = 'price fluctuation'
    action = 'box_input'

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
    return render_template("plot.html",path=sub_path,title=title,action=action)
@app.route("/area_input", methods=["POST"])
def area_input():
    title = 'current price depth'
    action = 'area_input'
    type = request.form["type"]
    area_data = vis.area_depth(type)
    path_areaplot = my_path + "/static/areaplot_%s.png" % (type)
    df_area = pd.DataFrame(area_data)
    df_area.plot.area(title='Current Price Depth')
    plt.savefig(path_areaplot)
    sub_path = "areaplot_%s.png" % (type)
    return render_template("plot.html",path=sub_path,title=title,action=action)


@app.route("/bar_input", methods=["POST"])
def bar_input():
    title = 'changing rate'
    action = 'bar_input'
    year = request.form["year"]
    rate_data = vis.rate_bar(year)

    df_rate = pd.DataFrame(rate_data)
    df_rate.plot.bar(title='growth rate')
    path_barplot = my_path + "/static/barplot_%s.png" % (year)
    plt.savefig(path_barplot)
    print('path_barplot:',path_barplot)
    sub_path="barplot_%s.png" % (year)
    return render_template("plot.html",path=sub_path,title=title,action=action)




@app.route("/line_input", methods=["POST"])
def line_input():
    title = 'trend'
    action = 'line_input'
    year = request.form["year"]
    line_chart = vis.line_chart(year)

    path_barplot = my_path + "/static/line_plot_%s.png" % (year)
    df_line = pd.DataFrame(line_chart)
    df_line.plot.line()

    plt.savefig(path_barplot)

    print('path_barplot:',path_barplot)
    sub_path="line_plot_%s.png" % (year)
    return render_template("plot.html",path=sub_path,title=title,action=action)

if __name__=="__main__":
    # model.init()
    app.run(debug=True)