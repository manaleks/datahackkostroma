# -*- coding: utf8 -*-
from flask import Flask, request, render_template
try:
  import simplejson as json
except:
  import json
  
import yandex_data

app = Flask(__name__)

# DATAHACKKOSTROMA
@app.route('/', methods=['GET', 'POST'])
def datahackkostroma():
    if request.method == 'POST':
        cities = request.form['cities']
        phrases = request.form['phrases']

        if cities == "" or phrases == "":
            return render_template('sorry.html')

        cities = cities.split(';')
        phrases = phrases.split(';')

        with open("log.txt", "a") as f:
            f.write("New request: yandex-search" + "\n" + "cities: " + str(cities) + "\t" + "phrases: " + str(phrases) + "\n")
        yandex_dat = yandex_data.super_run(phrases=phrases, cities=cities)
        data = {"yandex_data":yandex_dat}

        with open("log.txt", "a") as f:
            f.write("\n" + "Request answer: " + str(data) + "\n" + "###" * 50 + "\n")

        dataj = json.dumps(data, "utf-8")

        return render_template('datahackkostroma.html', result_yandex=dataj)

    return render_template('datahackkostroma.html')

with open("log.txt", "w") as f:
    f.write("Server started...\n")

if __name__ == "__main__":
    app.run(debug=True)