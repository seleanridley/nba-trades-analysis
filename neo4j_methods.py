import pickle 

import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable

from transactions_scraper import Bball_Scraper
from ratings2kscrapper import Ratings2kScraper
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

class LoadNeo4J():

    def __init__(self):
        host, port, user, password = config('NEO4J')
        self.driver = GraphDatabase.driver(f'neo4j://{host}:{port}', auth=(user, password))

    def close(self):
        self.driver.close()

    # Represents a trade between a team and a player
    @classmethod
    def create_acquisition(cls, tx, team, player):
        query = """
            MERGE (a:Team {name: $team_name})
            MERGE (b:Player {name: $player_name}) 
            MERGE (a)-[:ACQUIRED]->(b)
        """
        try:
            tx.run(query, team_name=team, player_name=player)

        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    @classmethod
    def create_release(cls, tx, team, player):
        query = """
            MERGE (a:Team {name: $team_name})
            MERGE (b:Player {name: $player_name}) 
            MERGE (a)-[:RELEASED]->(b)
        """
        try:
            tx.run(query, team_name=team, player_name=player)

        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    @classmethod
    def get_players(cls, tx):
        q_get_players = """
            MATCH(a) WHERE a:Player RETURN a.name AS player_name
        """

        try:
            result = tx.run(q_get_players)
            return [record["player_name"] for record in result]


        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=q_get_players, exception=exception))
            raise


    @classmethod
    def assign_attributes(cls, tx, players):
        r = Ratings2kScraper()

        for player in players:
            #TODO: Fix this
            if len(player.split()) < 2:
                continue

            print(player)
            player_dict = r.scrape_profile(player)

            q_add_attr = """
                MATCH (a {name: $name})
                SET a += $props
                RETURN a
            """
            try:
                result = tx.run(q_add_attr, name=player, props=player_dict)

            # Capture any errors along with the query and data for traceability
            except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(
                    query=q_add_attr, exception=exception))
                raise

    
    def run(self):
        b = Bball_Scraper()
        #b.get_teams()

        #for team in b.nba_teams:
        #    b.run(team, '2018-06-09')
        b.trades_df = pickle.load(open('data/trades_df.p', 'rb'))

        nj = LoadNeo4J()

        with nj.driver.session() as session:
            for _, row in b.trades_df.iterrows():
                if row['Acquired'] != '':
                    session.write_transaction(nj.create_acquisition, row['Team'], row['Acquired'])
                if row['Relinquished'] != '':
                    session.write_transaction(nj.create_release, row['Team'], row['Relinquished'])

            
        nj.driver.close()


if __name__ =="__main__":
    n = LoadNeo4J()
    #n.run()
    #players = pickle.load(open('data/db_current_players.p', 'rb'))
    with n.driver.session() as session:
        players = session.read_transaction(n.get_players)
        session.write_transaction(n.assign_attributes, players)

    #pickle.dump(players, open('data/db_current_players.p', 'wb'))

    n.driver.close()
