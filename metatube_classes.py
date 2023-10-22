from youtube_search import YoutubeSearch
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from claude_api import Client


class MetaTube:
    """
    a class that can:
    - send a search to YouTube
    - scrape transcripts from result videos
    - create a prompt for Claude to summarize the transcripts
    - send and receive info to and from Calude

    the class is used for this entire pipline

    Parameters
    ----------
    num_reviews: int
        max number of YouTube videos from search results to scrape transcripts from

    product_type: str
        the type of product (video game, skin care product, household appliance)

    product_name: str
        the name of the product (Warcraft III, Xiaomi Robot Vacuum E10)

    Attributes
    ----------
    num_reviews: int
        max number of YouTube videos from search results to scrape transcripts from

    product_type: str
        the type of product (video game, skin care product, household appliance)

    product_name: str
        the name of the product (Warcraft III, Xiaomi Robot Vacuum E10)

    COOKIE: str
        the individual cookie string for Claude AI

    text_formatter: TextFormatter
        a text formatter instance from youtube_transcript_api, used to turn transcripts to simple strings

    prompt_template_path: str
        path to the prompt template text file

    sep: str
        the separator used between reviews in the prompt delivered to Claude

    search_results: list
        a list of YouTube search results (dictionaries), populated when search is performed

    transcripts: dict
        a dictionary in which the keys are YouTube channel names, and the values are the transcripts
        of the matching video reviews, populated when transcripts are requested

    Methods
    -------
    get_youtube_data()
        searches YouTube for reviews and gets the resulting video data

    get_transcripts()
        iterates over search results and scrapes transcripts from videos

    format_transcript_lines(transcript)
        static method, gets rid of superfluous line breaks in a transcript

    create_prompt()
        creates the prompt to send to Claude based on the pattern in prompt.txt, the user input and the transcripts

    get_prompt()
        runs all the process thus far - from searching YouTube to creating the prompt, and returns the prompt

    query_claude(prompt)
        sends a prompt to Claude and returns its response

    run()
        runs the entire pipline from top to bottom - from searching YouTube to returning Claude's response
    """
    def __init__(self, num_reviews, product_type, product_name):
        with open('cookie.txt', 'r') as f:
            self.COOKIE = f.read()

        # general use
        self.text_formatter = TextFormatter()
        self.prompt_template_path = 'metatube_prompt.txt'
        self.sep = '\n\n------------------\n\n'

        # search parameters
        self.num_reviews = num_reviews
        self.product_type = product_type
        self.product_name = product_name

        # results
        self.search_results = None
        self.transcripts = None

    def get_youtube_data(self):
        """searches YouTube according to the class' attributes and populates the
        search_results attribute with the results
        """
        self.search_results = YoutubeSearch(f'{self.product_name} review',
                                            max_results=self.num_reviews).to_dict()

    def get_transcripts(self):
        """iterates over the search_results attribute and populates the transcripts attribute with a dictionary
        the keys are channel names and the values are transcripts of matching videos

        :raise: ValueError, if search_results is None (a search has not been performed)
        """
        if self.search_results is None:
            raise ValueError('must have search results for getting transcripts')

        trans = {}

        for res in self.search_results:
            # use video id to get transcript
            transcript = YouTubeTranscriptApi.get_transcript(res['id'])
            trans[res['channel']] = self.format_transcript_lines(self.text_formatter.format_transcript(transcript))

        self.transcripts = trans

    @staticmethod
    def format_transcript_lines(transcript):
        """gets rid of superfluous line breaks in a transcript

        :param transcript: string representing a video transcript
        :return: str, the new transcript without line breaks
        """
        return transcript.replace('\n', ' ')

    def create_prompt(self):
        """creates the prompt to send to Claude based on the pattern in prompt.txt, the user input and the transcripts

        :raise: ValueError, of transcripts is None (acquiring transcripts has not been performed yet)
        :return: a string representing the final prompt
        """
        if self.transcripts is None:
            raise ValueError('must have transcripts for prompt')

        # get prompt template from file
        with open(self.prompt_template_path, 'r') as f:
            s = f.read()

        # replace placeholders with user values
        s = (s.replace('<$num$>', str(len(self.search_results))).replace('<$product_type$>', self.product_type)
             .replace('<$product_name$>', self.product_name)) + '\n\n'

        # add the transcripts to the prompt
        for channel, transcript in self.transcripts.items():
            s += f'Review by {channel}:\n\n{transcript}{self.sep}'

        return s[:-1*len(self.sep)]

    def get_prompt(self):
        """runs all the process thus far - from searching YouTube to creating the prompt, and returns the prompt

        :return: a string representing the prompt
        """
        self.get_youtube_data()
        self.get_transcripts()
        return self.create_prompt()

    def query_claude(self, prompt):
        """sends a prompt to Claude and returns its response

        :param prompt: a string representing the prompt to send
        :return: a string representing Claude's response
        """
        claude_api = Client(self.COOKIE)
        conversation_id = claude_api.create_new_chat()['uuid']
        return claude_api.send_message(prompt, conversation_id)

    def run(self):
        """runs the entire pipline from top to bottom - from searching YouTube to returning Claude's response

        :return: a string representing Claude's response
        """
        p = self.get_prompt()
        return self.query_claude(p)
