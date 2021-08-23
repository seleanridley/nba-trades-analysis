import streamlit as st
from streamlit_agraph import agraph, TripleStore, Node, Edge, Config
import streamlit.components.v1 as components

import importlib  
d3_react_component = importlib.import_module("d3-react-component")

nba_d3_component = d3_react_component.nba_d3_component


from neo4j import GraphDatabase

from nba_api.stats.static import players
import configparser

def config(name):
    config = configparser.ConfigParser()
    config.read('database.ini')
    params = [
        config.get(name, 'host'),
        config.get(name, 'port'),
        config.get(name, 'user'),
        config.get(name, 'password')
    ]
    return params

def load_driver():
    host, port, user, password = config('NEO4J')
    driver = GraphDatabase.driver(f'neo4j://{host}:{port}', auth=(user, password))
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
    title = 'NBA Trades Network'
    st.markdown(title)
    #components.html("<html><body><h1>Hello, World</h1></body></html>", width=200, height=200)
    nba_d3_component()

    #app()
