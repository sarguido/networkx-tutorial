import config
import json
import os
import oauth2 as oauth
import urllib

HTTP_STATUS_OKAY = '200'

class TwitterAPI(object):

    def __init__(self):
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token = os.environ['ACCESS_TOKEN']
        access_secret = os.environ['ACCESS_SECRET']

        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth.Token(key=access_token, secret=access_secret)

        self.client = oauth.Client(consumer, token)

    # ------- SPECIFIC RESOURCE METHODS -------
    def get_following(self, params):
        return self.get_and_save_resource(config.RESOURCE.FOLLOWING, params, "users")

    def get_followers(self, params):
        return self.get_and_save_resource(config.RESOURCE.FOLLOWERS, params, "users")

    # ------- GENERIC RESOURCE METHOD -------
    def get_and_save_resource(self, resource, params, data_field=None):
        """
        :param resource: the twitter api resource, eg "followers/list"
        :param params: resource params, eg { "screen_name": "foo", "cursor": "-1"}
        :param data_field: what field actually contains the data results, eg data["users"]
        :return: the next cursor (or None)
        """

        if "screen_name" not in params or "cursor" not in params:
            print "expected params: screen_name, cursor"
            return None

        url = self.get_url(resource, params)
        data = self.get_response(url)
        if data:
            self.save_as(data, self.get_filename(resource, params))
            next_cursor = None

            if type(data) is dict:
                if 'next_cursor' in data:
                    next_cursor = data['next_cursor']
                if data_field:
                    result_summary = len(data[data_field])
                else:
                    result_summary = {k: len(data[k]) for k in data}
            else:
                result_summary = len(data)
            print "next cursor: ", next_cursor, "num results: ", result_summary
            return next_cursor

    def get_response(self, url):
        header, response = self.client.request(url, method="GET")

        if header['status'] <> HTTP_STATUS_OKAY:
            print header['status'], response
            return None
        else:
            return json.loads(response)

    @staticmethod
    def get_url(resource, params):
        return config.TWITTER_BASE_URL.format(resource=resource) + urllib.urlencode(params)

    @staticmethod
    def save_as(data, filename):
        full_path = os.path.join(config.PARENT_DATA_FOLDER, filename)
        parent_directory = os.path.dirname(full_path)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        with open(full_path, 'w') as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def get_filename(resource, params):
        return '{resource}.{screen_name}.{cursor}.json'.format(
            resource=resource,
            screen_name=params['screen_name'],
            cursor=params['cursor'])