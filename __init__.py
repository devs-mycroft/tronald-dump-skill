from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.log import LOG
import urllib, urllib.request, json, random, re
from urllib.request import Request

__author__ = 'krisgesling'
LOGGER = LOG(__name__)

class TronaldDump(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('dump.tronald.intent')
    def handle_dump_tronald(self, message):
        topic = message.data.get('topic', '')
        urlParams = { 'query': topic }
        apiUrl = "https://api.tronalddump.io/search/quote?%s" % urllib.parse.urlencode(urlParams)
        try:
            with urllib.request.urlopen(Request(apiUrl, headers={'User-Agent': 'Mozilla/5.0'})) as url:
                result = json.loads(url.read().decode())
                if result['count'] == 0:
                    self.speak_dialog('no.result', {'topic': topic})
                else:
                    i = random.randint(0, result['count'] - 1)
                    rawQuote = result['_embedded']['quotes'][i]['value']
                    speakingQuote = re.sub(r'https?:\/\/.*\s?', '', rawQuote)
                    self.speak_dialog('dump.tronald', {'quote': speakingQuote})
        except urllib.error.HTTPError as e:
            self.speak_dialog('http.error')
        except urllib.error.URLError as e:
            self.speak_dialog('url.error')

    def stop(self):
        pass

def create_skill():
    return TronaldDump()
