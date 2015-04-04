import client as c

# CODE SAMPLE 1
# get the followers for @CuteEmergency, save to file

SCREEN_NAME = 'CuteEmergency'

params = {
    'screen_name': SCREEN_NAME,
    'cursor': '-1'
}
# make twitter call; save to data folder (specified in config.py)
next_cursor = c.tapi.get_and_save_resource(resource='followers/list', params=params, data_field='users')

# cursor was not 0, so set cursor and make another call
params['cursor'] = next_cursor
next_cursor = c.tapi.get_and_save_resource(resource='followers/list', params=params, data_field='users')

# CODE SAMPLE 2
# get first follower for @CuteEmergency, save into x
nth_element = 0
x = c.dapi.get_item(resource='followers/list', screen_name=SCREEN_NAME, index=nth_element, data_field='users')

# twitter results a lot of data that we don't care about; we have a list of fields to ignore in excluded.txt (set in config)
excluded_fields = c.dapi.get_excluded_fields()

# view data for first follower
c.dapi.print_item(x, exclude=excluded_fields)

# view data for next follower
nth_element = 1
x = c.dapi.get_item(resource='followers/list', screen_name=SCREEN_NAME, index=nth_element, data_field='users')
c.dapi.print_item(x, exclude=excluded_fields)

