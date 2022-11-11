import pycountry as pyc
import json
from geopy.distance import geodesic as GD
import networkx as nx
import math
from flask import Flask, jsonify, render_template
from bson import json_util
from pymongo import MongoClient
from queue import PriorityQueue
from dijkstra_algorithm import dijkstra

app = Flask(__name__)
client = MongoClient("mongodb+srv://<username>:<password>@cluster0.m6ouyv0.mongodb.net/?retryWrites=true&w=majority")
db = client.acomplex

nodes = list(db.nodes.find())
links = list(db.links.find())
flights_graph = nx.DiGraph()
for link in links:

    d = GD(     (nodes[link["source"]]["lat"], nodes[link["source"]]["lon"]),
                (nodes[link["target"]]["lat"], nodes[link["source"]]["lon"])).km
    flights_graph.add_edge(link["source"], link["target"], weight = d)

@app.route('/dijkstra/<int:start>/<int:end>')
def dijkstra_route(start, end):
    # run dijkstra
    path, dist = dijkstra(flights_graph, start, end)
    #get nodes and links necesary to show the path
    _nodes = []
    _links = []
    for node in path:
        _nodes.append(nodes[node-1])

    for i in range(len(path)-1):
        temp_link = list(db.links.find({"source": path[i], "target": path[i+1]}))[0]
        _links.append(temp_link)
    # return the path
    return json.dumps({'nodes': _nodes, 'links': _links}, default=json_util.default)


@app.route('/nodes')
def returnNodes():  # put application's code here
    return json.dumps({'nodes': nodes, 'links': links}, default=json_util.default)

@app.route('/countries')
def returnCountryList():
    countries = []
    for i in nodes:
        countries.append(i['country'])
    _countries = list()
    for i in set(countries):
        temp_dict = dict()
        temp_dict["country"] = i
        temp_pyc = pyc.countries.get(name = i)
        if temp_pyc is not None:
            temp_dict["code"] = temp_pyc.alpha_2
        else:
            temp_dict["code"] = None
        _countries.append(temp_dict)

    return jsonify(_countries)

@app.route('/airports/<string:country>')
def returnAirports(country):
    _airports = list()
    temp_pyc = pyc.countries.get(name = country)
    if temp_pyc is not None:
        coutry_code = temp_pyc.alpha_2
    else:
        coutry_code = None
    for i in nodes:
        if i['country'] == country:
            temp_dict = dict()
            temp_dict["airport"] = i["name"]
            temp_dict["code"] = coutry_code
            _airports.append(temp_dict)
    return jsonify(_airports)

if __name__ == '__main__':
    app.run()
