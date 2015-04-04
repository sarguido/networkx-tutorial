PARENT_DATA_FOLDER = 'data' # folder where twitter json results will be saved
TWITTER_BASE_URL = 'https://api.twitter.com/1.1/{resource}.json?count=5000&'
EXCLUDED_FIELDS_FILENAME = 'excluded.txt'

RESOURCE = {
    'followers': {
        'url': 'followers/list',
        'filename_fields': ['screen_name', 'cursor'],
        'summary_fields': ['next_cursor'],
        'next': {'cursor': 'next_cursor'},
        'data_field': 'users',
        'summarize': 'screen_name favourites_count followers_count friends_count name description'.split()
    },

    'friends': {
        'url': 'friends/list',
        'filename_fields': ['screen_name', 'cursor'],
        'summary_fields': ['next_cursor'],
        'next': {'cursor': 'next_cursor'},
        'data_field': 'users',
        'summarize': 'screen_name favourites_count followers_count friends_count name description'.split()
    },

    'statuses': {
        'url': 'statuses/user_timeline',
        'filename_fields': ['screen_name', 'max_id'],
        'summary_fields': ['created_at', 'id_str'],
        'next': {'max_id': 'id_str'},
        'data_field': None,
        'desc': True,
        'summarize': [
            'created_at',
            'id',
            'entities|user_mentions|screen_name',
            'entities|media|type',
            'favorite_count',
            'retweet_count',
            'retweeted_status|id',
            'retweeted_status|favorite_count',
            'retweeted_status|retweet_count',
            'retweeted_status|created_at',
            'entities|media|url',
            'text'
        ]
    },

    'retweeters': {
        'url': 'statuses/retweeters/ids',
        'filename_fields': ['id', 'cursor'],
        'summary_fields': ['next_cursor'],
        'next': {'cursor': 'next_cursor'},
        'data_field': 'ids',
        'summarize': ['ids']
    },

    'retweets': {
        'url': 'statuses/retweets/%(id)s',
        'filename_fields': ['retweeted_status|user|screen_name'],
        'summarize_filename_prefix': ['retweeted_status|user|screen_name'],
        'resource_param': 'id',
        'summarize': [
            # These values are all the same:
            # 'retweeted_status|id',
            'retweeted_status|favorite_count',
            # 'retweeted_status|retweet_count',
            'favorite_count',
            'favorited',
            'user|follower_count',
            'created_at',
            'id',
            'user|screen_name',
            'user|statuses_count',
            'user|favourites_count',
            'entities|user_mentions|screen_name',
            # 'entities|user_mentions|id_str',
            'entities|hashtags|text'
        ]
    }
}



