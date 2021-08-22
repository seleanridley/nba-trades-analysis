import streamlit as st
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
import numpy as np
import pandas as pd
import pickle
from neo4j import GraphDatabase

import nba_api
from nba_api.stats.static import players

def load_driver():
    driver = GraphDatabase.driver('bolt://localhost:7687', auth=('neo4j', 'admin'))
    return driver

def get_triplets(tx):
    result = tx.run("""MATCH (a)-[p]->(b)
                    WHERE b.name IN ['Russell Westbrook', 'Alex Caruso', 'Lonzo Ball']
                    RETURN a.name, b.name, b.img
                        """)

    return [(record['a.name'], 'value', record['b.name'], record['b.img']) for record in result]


def app():
    #trades_df = pickle.load(open('data/trades_df.p', 'rb'))

    driver = load_driver()

    config = Config(height=500,
                    width=700,
                   # nodeHighlightBehavior=True,
                    directed=True,
                    collapsible=True)


    #store = TripleStore()
    nodes = []
    edges = []
   
    with driver.session() as session:
        transactions = session.read_transaction(get_triplets)

    for t in transactions:
        nodes.append(Node(id=t[0], size=600))
        nodes.append(Node(id=t[2], size=600, svg=t[-1]))
        #print(type(t[-1]))
        edges.append(Edge(source=t[0], target=t[2], type='CURVE SMOOTH'))

        #store.add_triple(*t)

    #agraph(list(store.getNodes()), (store.getEdges()), config)
    agraph(nodes, edges, config)

if __name__=="__main__":
    app()
