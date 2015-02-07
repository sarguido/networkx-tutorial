# networkx-tutorial
Twitter Network Analysis with NetworkX 

### Sarah and Celia's Todo list:

* ~~C: NetworkX part1: nodes, edges, attributes:~~
* ~~C: NetworkX part2: exporting and importing data:
    *(exporting is good so that attendees can see what their end json-data processing format should look like)*~~
* ~~C: NetworkX part3: types of graphs:~~ .. **somewhat covered in Exporting/Importing to NetworkX graph**
    - ~~undirected, directed~~

* ~~using NetworkX/matplotlib to plot stuff:~~ ... **covered in NetworkX, part 1**
    - ~~C: basics: how to set edge and node sizes~~

* C: clean up PyTN retweet/status data, make simplier data manip scripts just for the tutorial

* ~~the relevant Twitter API calls that we'll use to grab the data:~~ **mostly covered in Step 2 -- Calling the Twitter API (in /notebooks/twitter/)**
    * ~~S: friends, followers~~
    * ~~C: retweets, statuses~~
* how to get the json payloads, and get them into a format that NetworkX can import:
    * S: friends, followers
    * C: retweets, statuses
        - write simple python scripts that would have grabbed the data from Twitter
        - clean up the retweet and user_timeline json files:
            - put them in one consolidated folder
        - write scripts to extract just the data we want, and format it into a JSON format
          that we can use to import into NetworkX
* using networkx & matplotlib to display data:
    * S: friends, followers
    * C: retweets, statuses
        - figure out how to cleanly display the data (to cut out the noise)
            - make edges with only 1 retweet slightly opaque
        - can I make different colored fonts for each node?
        - do I want a directed graph here? or does it not matter?

Twitter Stuff:
* ~~C how to get your Twitter API tokens~~
* ~~C: basic script to make the API calls~~
* C libs needed: oauth2

* S: installation instructions:
    - different ways of following along
    - libs needed for PyTN: networkx, json, malplotlib (warn that this takes a while)
    - libs needed for Twitter: oauth2 (can just put this on the Twitter post-tutorial ipynb)

If there's time:
* C: get last 20% of retweet data (but we'll be okay w/o it)
