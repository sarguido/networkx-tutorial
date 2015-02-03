import config
import json
import os
import oauth2 as oauth
import urllib
from data import DataAPI

HTTP_STATUS_OKAY = '200'
HTTP_RATE_LIMIT_EXCEEDED = '429'

class TwitterAPI(object):

    def __init__(self):
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        access_token = os.environ['ACCESS_TOKEN']
        access_secret = os.environ['ACCESS_SECRET']

        consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
        token = oauth.Token(key=access_token, secret=access_secret)

        self.client = oauth.Client(consumer, token)

    # ------- GENERIC RESOURCE METHOD -------

    def get_resource(self, resource, params):
        """
        :param resource: the twitter api resource, eg "followers/list"
        :param params: resource params, eg { "screen_name": "foo", "cursor": "-1"}
        :param data_field: what field actually contains the data results, eg data["users"]
        :return: a tuple of next_cursor, data. next_cursor can be None.
        """

        url = TwitterAPI.get_url(resource, params)
        print url
        data = self.get_response(url)
        summary = None
        if data:
            other_params = data
            if type(data) is list:
                other_params = data[0]
            if 'summarize_filename_prefix' in resource:
                for field in resource['summarize_filename_prefix']:
                    keys = field.split("|")
                    value = DataAPI.find_key(other_params, keys)
                    if value:
                        params[field] = value
                    else:
                        resource['filename_fields'].remove(field)

            file_path = TwitterAPI.get_filename(resource['url'], params, resource['filename_fields'])
            TwitterAPI.save_resource(data, file_path)
            summary = TwitterAPI.get_summary(data, params, resource)

        return summary, data

    @staticmethod
    def get_next_params(resource, params):
        summary_path = os.path.join(config.PARENT_DATA_FOLDER, TwitterAPI.get_summary_path(resource['url'], params))
        if not os.path.exists(summary_path):
            print "no file at", summary_path
            return {}

        with open(summary_path, 'r') as f:
            summary = json.loads(f.read())
        params = summary['params']
        for key in resource['next']:
            result_key = resource['next'][key]
            params[key] = str(summary['result'][result_key])
        return params

    @staticmethod
    def get_summary_path(resource_url, params):

        last_params = {'x': 'last'}
        if 'screen_name' in params:
            last_params['screen_name'] = params['screen_name']
        elif 'last' in params:
            last_params['screen_name'] = params['last']

        return TwitterAPI.get_filename(resource_url, last_params, last_params.keys())

    @staticmethod
    def get_summary(data, params, resource):
        summary_path = TwitterAPI.get_summary_path(resource['url'], params)
        summary_fields = []
        if 'summary_fields' in resource:
            summary_fields = resource['summary_fields']
        num_items = None

        summary = {}
        summary['params'] = {f: params[f] for f in resource['filename_fields'] if f in params}
        summary['result'] = {}

        if 'data_field' in resource and resource['data_field']:
            for field in summary_fields:
                if field in data:
                    summary['result'][field] = data[field]
            data = data[resource['data_field']]

        if type(data) is list and data:
            num_items = len(data)
            data = data[-1]

        if type(data) is dict:
            for field in summary_fields:
                if field in data:
                    summary['result'][field] = data[field]
        summary['result']['num_items'] = num_items

        TwitterAPI.save_resource(summary, summary_path)

        print "summary", summary
        return summary

    def get_response(self, url):
        header, response = self.client.request(url, method="GET")

        if header['status'] <> HTTP_STATUS_OKAY:
            print header['status'], response

            if header['status'] == HTTP_RATE_LIMIT_EXCEEDED:
                exit(1)

            return None
        else:
            return json.loads(response)

    @staticmethod
    def get_url(resource, params):
        url_params = {p: params[p] for p in params if params[p]}
        return config.TWITTER_BASE_URL.format(resource=resource['url']) + urllib.urlencode(url_params)

    @staticmethod
    def save_resource(data, filename):
        full_path = os.path.join(config.PARENT_DATA_FOLDER, filename)
        parent_directory = os.path.dirname(full_path)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory)
        with open(full_path, 'w') as f:
            f.write(json.dumps(data, indent=4))

    @staticmethod
    def get_filename(resource, params, filename_fields):

        filename_parts = [resource]
        filename_parts.extend([str(params[f]) for f in filename_fields if f in params and params[f]])
        filename_parts.append("json")
        print filename_parts
        return '.'.join(filename_parts)
