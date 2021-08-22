import pandas as pd
import requests
import re
import json

from bs4 import BeautifulSoup

from nba_api.stats.static import players

class Ratings2kScraper():

    def __init__(self):
        self.base_url = "https://2kratings.com/{}"
        self.attributes_df = pd.DataFrame()

    def scrape_profile(self, player_name):
    
        #if len(player_name) == 0:
        #    return {}

        attr_dict = {}

        url_name = player_name.replace(' ', '-')

        
        r = requests.get(self.base_url.format(url_name))
        soup = BeautifulSoup(r.content, 'html.parser')
        #print(player_name, ": ", soup.find('title'))
        if not soup.find('title'):
            print("Could not find ", player_name)
            return {}

        
        #Get Player Image
        id = players.find_players_by_full_name(player_name) #.replace(' ', '\s')) #player_name.replace(' ', '_'))
        print(id)
        if id:
            id = id[0]['id']
            img_url = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{}.png".format(id)
            attr_dict['img'] = img_url
        else:
            attr_dict['img'] = None


        #Get Player Ratings
        ratings = {}
        labels = ["Overall", "Inside Scoring", "Outside Scoring", "Athleticism", "Playmaking", "Rebounding", "Defending"]
        scripts = soup.findAll('script')

        s = ''
        for x in scripts:
            
            if 'chartjs-radar' in x.get_text():
                s = x.get_text()
                break
        
        if len(s) > 0:
            m = re.search(r"\[([\d,\s]+)\]", s)
            scores = [int(x) for x in m.group(1).split(',') if x != '']
            ratings = dict(zip(labels, scores))

        #Get Player Info
        info_dict = {}
        info_labels = ['Team', 'Archetype', 'Position', 'Jersey']
        info = soup.find('div', {"class": "player-info"})
        if info:
            player_i = info.findAll('p', {"class": 'mb-0'})
            p_list = [x.get_text(strip=True).split(':') for x in player_i][1:]
            info_dict = {p[0]: p[1].strip() for p in p_list if p[0] in info_labels}


        #Concat Dicts and insert into pandas Dataframe
        attr_dict = {**attr_dict, **ratings, **info_dict}
        return attr_dict






if __name__=="__main__":
    ratings = Ratings2kScraper()
    y = ratings.scrape_profile('Damian Lillard')
    print(y)