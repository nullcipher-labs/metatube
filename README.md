# metatube
an app that, given a name and type of product, uses Claude AI to deliver a summary of youtube reviews of the product.
this app gets a product description from the user, then scrapes youtube for reviews, downloads the transcripts of the review videos, and summarizes them using Claude AI.
yet another example of an automation pipeline using ai for tasks that could not be automated before :)

# prerequisites
youtube-search<br>https://pypi.org/project/youtube-search/<br>pip install youtube-search
<br><br>
youtube-transcript-api<br>https://pypi.org/project/youtube-transcript-api/<br>pip install youtube-transcript-api
<br><br>
Claude-API<br>https://github.com/KoushikNavuluri/Claude-API<br>pip install claude-api

# setup
for the app to work you have to copy your Claude cookie string into the cookie.txt file.
<br>here:<br>https://github.com/KoushikNavuluri/Claude-API<br>
you can find a guide on how to get your individual cookie string.

# how to use
the app has a tkinter GUI that looks like this:

![metatube_example](https://github.com/nullcipher-labs/metatube/assets/35743548/01d39393-8019-4444-a0ec-c21d79c4cdc1)

the user must enter:
- in red: the name of the product (in this example, the video game "Lords of the Fallen", that just released around the time of writing this readme)
- in blue: the type of the product, video game, software, skin care product etc
- in green: the number of youtube video to scrape, goes from first result in a youtube search of the products name (+ the word "review") onwards (small numbers reccommended for right now)

 the hit the go button (marked in pink).

 the progress box will report on the apps current action, and the output box will contain the editable summary when done.

 # python project
 the project has two python files:
 1. metatube_classes.py - contains the bot class that has all of the relevant functionality (Metatube)
 2. metatube_main.py - contains the tkinter elements and ties them together to the Metatube instance

there are also two txt files:
1. metatube_prompt.txt - contains the prompt phrasing pattern for Claude, do not edit
2. cookie.txt - contains the cookies string for yourself, as seen in the setup section
