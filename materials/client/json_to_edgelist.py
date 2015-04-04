import os
import json
from client.data import DataAPI
from collections import defaultdict

RETWEET_DATA_PATH = 'data/statuses/retweets'
RETWEETS_OUTPUT = 'retweet_relationships/retweets.txt'
POTENTIAL_RETWEETS_OUTPUT = 'retweet_relationships/potential_retweets.txt'

SATELLITE_SCREEN_NAME = 'PyTennessee' # the main twitter handle that we're interested in analyzing

fields = [
    'created_at',           #when was it retweeted?
    'user|screen_name'      #who retweeted?
]

class Relationships(object):

    def __init__(self, satellite_screen_name):
        self.satellite_screen_name = satellite_screen_name

        # these will be a dict of dicts: [original_tweeter][retweeter] = num_retweets
        self.retweets = {}

        # even though SATELLITE_SCREEN_NAME may not be the original tweeter, for those that tweeted afterwards,
        # they could have potentially seen the tweet from SATELLITE_SCREEN_NAME
        self.possible_satellite_retweeter = defaultdict(int) # will be dict of [retweeter] = num_retweets

    def add(self, filename):

        file_parts = filename.split('.')
        tweet_source = file_parts[1]

        if tweet_source not in self.retweets:
            self.retweets[tweet_source] = defaultdict(int)

        with open(filename, 'r') as f:
            retweets = json.loads(f.read())

        #tweets are most recent first; let's reverse it into chronological order
        retweets.reverse()

        is_possible_retweeter = False
        for retweet in retweets:
            relevant_data = Relationships._get_relevant_data(retweet)
            if relevant_data:
                retweeter = relevant_data['screen_name']
                self.retweets[tweet_source][retweeter] += 1

                if is_possible_retweeter:
                    self.possible_satellite_retweeter[retweeter] += 1
                elif retweeter == self.satellite_screen_name:
                    is_possible_retweeter = True

    def save_retweets(self, filename):
        Relationships._save_relationships(self.retweets, filename)

    def save_potential_retweets(self, filename):
        satellite_relationships = {
            self.satellite_screen_name: self.possible_satellite_retweeter
        }
        Relationships._save_relationships(satellite_relationships, filename)

    @staticmethod
    def _create_parent_dirs(file_path):
        parent_directory = os.path.dirname(file_path)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)

    @staticmethod
    def _save_relationships(relationships, filename):
        flat_relationships = []
        for source in relationships:
            for retweeter in relationships[source]:
                flat_relationships.append("%s %s {'weight': %s}" % (
                    source,
                    retweeter,
                    relationships[source][retweeter]))

        Relationships._create_parent_dirs(filename)
        with open(filename, 'w') as f:
            f.write('\n'.join(flat_relationships))


    @staticmethod
    def _get_relevant_data(retweet):
        relevant_data = {}
        for field in fields:
            keys = field.split('|')
            value = DataAPI.find_key(retweet, keys)
            if not value:
                #can't add relationship to the graph if we don't have all the relevant info
                return None
            relevant_data[keys[-1]] = value
        return relevant_data


def get_retweet_json_filenames(path):
    filenames = []
    for (dir_path, dir_names, file_names) in os.walk(path):
        if dir_path == path:
            for filename in file_names:
                if '.summary' not in filename and '.last' not in filename:
                    filenames.append(os.path.join(dir_path, filename))
    return filenames


def run():
    filenames = get_retweet_json_filenames(RETWEET_DATA_PATH)
    relationships = Relationships(SATELLITE_SCREEN_NAME)
    for filename in filenames:
        relationships.add(filename)
    relationships.save_retweets(RETWEETS_OUTPUT)
    relationships.save_potential_retweets(POTENTIAL_RETWEETS_OUTPUT)


def test(filename):
    relationships = Relationships(SATELLITE_SCREEN_NAME)
    relationships.add(filename)
    # print json.dumps(relationships.retweets, indent=2)
    relationships.save_retweets(RETWEETS_OUTPUT)
    # for source in relationships.retweets:
    #     for retweeter in relationships.retweets[source]:
    #         print source, retweeter, relationships.retweets[source][retweeter]


run()

# test('data/statuses/retweets/552606442596073472.kcunning.json')
