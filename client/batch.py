from sys import argv
from client import run
import time

filename = 'batch_input/input.txt'
command_template = 'get retweets id={id}'
pace_requests = True

# filename = 'batch_input/processed.batch1.txt'
# command_template = 'summary retweets id={id}'
# pace_requests = False


def get_id(data):
    if data['retweeted_count'] > 0:
        print "not original tweet. user_mentions:", data['user_mentions']
        return data['retweeted_id']

    elif data['retweets'] > 0:
        return data['id']

    return None


# get input data
header, lines = run.get_file_actions(filename)

columns = {
    'id': 1,
    'user_mentions': 2,
    'retweets': 5,
    'retweeted_id': 6,
    'retweeted_count': 8
}

# do we just want to run a single line?
args = argv[1:]
if len(args):
    line_number = int(args[0])
    lines = [lines[line_number]]

for line in lines:

    #extract relevant data from line
    data = {}
    for c in columns:
        if columns[c] < len(line):
            value = line[columns[c]]
            if run.is_numeric(value):
                value = int(value)
            data[c] = value
        else:
            data[c] = ''


    #construct command
    print "****** id", data['id'], ", retweets", data['retweets']
    id = get_id(data)

    if id:
        command = command_template.format(id=id)
        run.run_action(command.split(' '))

    #sleep for 1 second to comply with rate limits
    if pace_requests:
        time.sleep(1.5)
