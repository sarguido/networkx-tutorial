import os
import json

import config

class DataAPI(object):

    @staticmethod
    def summarize_friends(screen_name):
        DataAPI.summarize_users(config.RESOURCE.FRIENDS, screen_name, config.SUMMARIZE.FRIENDS)

    @staticmethod
    def summarize_followers(screen_name):
        DataAPI.summarize_users(config.RESOURCE.FOLLOWERS, screen_name, config.SUMMARIZE.FOLLOWERS)

    @staticmethod
    def get_item(resource, screen_name, index, data_field=None):
        file_paths = DataAPI.get_filenames(resource, screen_name)
        for path in file_paths:
            search_result = None
            with open(path, 'r') as f:
                if data_field:
                    item_list = json.loads(f.read())[data_field]
                else:
                    item_list = json.loads(f.read())
                if index < len(item_list):
                    return item_list[index]
                else:
                    # index is in a subsequent file
                    # decrement index by the number of items in this file
                    index -= len(item_list)
        return None

    @staticmethod
    def find_user(resource, screen_name, search_for):
        file_paths = DataAPI.get_filenames(resource, screen_name)
        for path in file_paths:
            search_result = None
            with open(path, 'r') as f:
                search_result = [u for u in json.loads(f.read())['users'] if u['screen_name'] == search_for]
            if search_result:
                return search_result[0]
        return None

    @staticmethod
    def summarize_users(resource, screen_name, properties):
        file_paths = DataAPI.get_filenames(resource, screen_name)
        for path in file_paths:
            users = None
            with open(path, 'r') as f:
                users = [u for u in json.loads(f.read())['users']]
            with open(DataAPI._file_prefix(resource, screen_name) + 'summary.txt', 'w') as f:
                for u in users:
                    x = []
                    for p in properties:
                        if type(u[p]) is str or type(u[p]) is unicode:
                            value = u[p].encode('utf-8')
                            if value:
                                value = value.replace('\n', '|')
                            x.append(value)
                        else:
                            x.append(str(u[p]))
                    f.write('\t'.join(x) + '\n')

    @staticmethod
    def get_filenames(resource, screen_name):
        file_paths = []
        for (dir_path, dir_names, file_names) in os.walk(config.PARENT_DATA_FOLDER):
            expected_prefix = DataAPI._file_prefix(resource, screen_name)
            for f in file_names:
                file_path = os.path.join(dir_path, f)
                if file_path.startswith(expected_prefix) and file_path.endswith('.json'):
                    file_paths.append(file_path)
        return file_paths

    @staticmethod
    def _file_prefix(resource, screen_name):
        return os.path.join(config.PARENT_DATA_FOLDER, resource + '.' + screen_name + '.')

    @staticmethod
    def get_excluded_fields(exclusion_list_filename=None):
        if not exclusion_list_filename:
            exclusion_list_filename = config.EXCLUDED_FIELDS_FILENAME
        path = os.path.join(config.PARENT_DATA_FOLDER, exclusion_list_filename)
        with open(path, 'r') as f:
            return f.read().split("\n")

    # ---- helper methods for viewing user json; separating key/values by dicts (nested) and non-dicts (simple)
    @staticmethod
    def print_item(obj, print_fields=False, exclude=None, caption=None):
        children = []
        x = {}
        for k in obj:
            if exclude is None or k not in exclude:
                if type(obj[k]) is not dict:
                    k_list = []
                    if type(obj[k]) is list:
                        for y in obj[k]:
                            if type(y) is dict:
                                y_include = {y_key: y[y_key] for y_key in y if exclude is None or y_key not in exclude}
                                k_list.append(y_include)
                            else:
                                k_list.append(y)
                        x[k] = k_list
                    else:
                        x[k] = obj[k]
                else:
                    x[k] = '==dict=='
                    if caption:
                        child_caption = caption + " > " + k
                    else:
                        child_caption = k
                    children.append((child_caption, obj[k]))
        # print results
        if print_fields:
            print '\n'.join(sorted(x.keys()))
        if caption:
            print "========", caption, "========"
        print json.dumps(x, indent=4, sort_keys=True)
        for child in children:
            DataAPI.print_item(obj=child[1], caption=child[0], exclude=exclude)