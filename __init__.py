from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import urllib, json, random, re
from urllib.request import Request, urlopen

class TronaldDump(MycroftSkill):

    @intent_handler('dump.tronald.intent')
    def handle_dump_tronald(self, message):
        topic = message.data.get('topic', '')
        url_params = urllib.parse.urlencode({ 'query': topic })
        api_url = 'https://api.tronalddump.io/search/quote?%s' % url_params
        headers = {'User-Agent': 'Mozilla/5.0'}
        try:
            with urlopen(Request(api_url, headers)) as url:
                result = json.loads(url.read().decode())
                if result['count'] == 0:
                    self.speak_dialog('no.result', {'topic': topic})
                else:
                    i = random.randint(0, result['count'] - 1)
                    raw_quote = result['_embedded']['quotes'][i]['value']
                    speakable_quote = remove_http_links(raw_quote)
                    self.speak(speakable_quote)
        except urllib.error.HTTPError as e:
            self.speak_dialog('http.error')
        except urllib.error.URLError as e:
            self.speak_dialog('url.error')

def remove_http_links(raw_quote):
    return re.sub(r'https?:\/\/.*\s?', '', raw_quote)

def create_skill():
    return TronaldDump()
