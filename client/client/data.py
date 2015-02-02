import os
import json

import config

class DataAPI(object):

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
    def summarize_items(resource, params, summary=True, details=False):

        properties = None
        data_field=None
        if 'summarize' in resource:
            properties = resource['summarize']
        if 'data_field' in resource:
            data_field = resource['data_field']

        file_paths = DataAPI.get_filenames(resource, params)

        if 'desc' in resource and resource['desc']:
            file_paths.reverse()

        lines, endpoints = DataAPI.get_summaries(file_paths, data_field, resource, params, properties)

        file_prefix = DataAPI._file_prefix(resource, params)

        with open(file_prefix + 'summary-summary.txt', 'w') as f:
            f.write('count\tfilename\t' + '\t'.join(properties) + '\n')
            f.write('\n'.join(endpoints))

        with open(file_prefix + 'summary.txt', 'w') as f:
            f.write('\t'.join(properties) + '\n')
            f.write('\n'.join(lines))

        if summary:
            print 'count\tfilename\t' + '\t'.join(properties) + '\n'
            print '\n'.join(endpoints)

        if details:
            print '\t'.join(properties) + '\n'
            print '\n'.join(lines)

    @staticmethod
    def adjust_inputs(resource, params):
        #if resource url contains string formatting, do that first
        if 'resource_param' in resource:
            resource_param = resource['resource_param']
            resource['url'] = resource['url'] % {resource_param: params[resource_param]}
            del params[resource['resource_param']]

    @staticmethod
    def get_summaries(file_paths, data_field, resource, params, properties):

        lines = []
        endpoints = []
        for path in file_paths:
            with open(path, 'r') as f:
                if data_field:
                    data = json.loads(f.read())[data_field]
                else:
                    data = json.loads(f.read())

            if properties is None:
                excluded_fields = DataAPI.get_excluded_fields()
                properties = [x for x in data[0].keys() if x not in excluded_fields]

            expected_prefix = DataAPI._file_prefix(resource, params)
            file_id = path[(len(expected_prefix)):-5]

            count = str(len(data))
            if type(data) is list:
                endpoints.append(count + '\t' + file_id + '\t' + DataAPI.summarize_item(data[0], properties))
                endpoints.append(count + '\t' + file_id + '\t' + DataAPI.summarize_item(data[-1], properties))

            for u in data:
                if 'limit' in params:
                    params['limit'] -= 1
                    if params['limit'] < 0:
                        return lines, endpoints
                lines.append(DataAPI.summarize_item(u, properties))

        return lines, endpoints

    @staticmethod
    def summarize_item(item, properties):
        x = []
        for p in properties:
            keys = p.split("|")
            value = DataAPI.find_key(item, keys)
            if not value:
                value = 0
            x.append(DataAPI.cleanup_value(value))
        return '\t'.join(x)

    @staticmethod
    def find_key(value, keys):
        if not keys:
            return None
        if type(value) is list:
            results = [DataAPI.find_key(v, keys) for v in value]
            results = [r for r in results if r is not None]
            return '|'.join(results)
        if keys[0] not in value:
            return None
        if len(keys) == 1:
            return value[keys[0]]
        return DataAPI.find_key(value[keys[0]], keys[1:])

    @staticmethod
    def cleanup_value(item):
        if type(item) is str or type(item) is unicode:
            value = item.encode('utf-8')
            if value:
                value = value.replace('\n', '|')
            return value
        else:
            return str(item)

    @staticmethod
    def get_filenames(resource, params):
        file_paths = []
        for (dir_path, dir_names, file_names) in os.walk(config.PARENT_DATA_FOLDER):
            expected_prefix = DataAPI._file_prefix(resource, params)
            for f in file_names:
                file_path = os.path.join(dir_path, f)
                if file_path.startswith(expected_prefix) and file_path.endswith('.json') and '.last.' not in file_path:
                    file_paths.append(file_path)
        return file_paths

    @staticmethod
    def _file_prefix(resource, params):

        prefix_params = resource['filename_fields'][:-1]

        filename_parts = [resource['url']]
        filename_parts.extend([params[p] for p in prefix_params])

        return os.path.join(config.PARENT_DATA_FOLDER, '.'.join(filename_parts) + '.')

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