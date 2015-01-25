PARENT_DATA_FOLDER = 'data' # folder where twitter json results will be saved
TWITTER_BASE_URL = 'https://api.twitter.com/1.1/{resource}.json?count=5000&'
EXCLUDED_FIELDS_FILENAME = 'excluded.txt'

class RESOURCE(object):
    FOLLOWERS = 'followers/list'
    FRIENDS = 'friends/list'

class SUMMARIZE(object):
    FOLLOWERS = 'screen_name favourites_count followers_count friends_count name description'.split()
    FRIENDS = 'screen_name favourites_count followers_count friends_count name description'.split()

