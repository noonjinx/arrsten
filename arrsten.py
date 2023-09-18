import re
import random
import json
import string
import argparse
import nltk.data
from mastodon import Mastodon

DELIMITER = 'XXDELIMITERXX';

DEFAULT_QUOTE = {
    "text"   : "An error seems to have occurred.",
    "author" : "Jane Arrsten",
    "title"  : "Lack Of Testing"
}
 
# Parse command line arguments

parser = argparse.ArgumentParser(description="Quote Like A Pirate",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--debug", action="store_true", help="debug mode (show original quote)")
parser.add_argument("-t", "--toot", action="store_true", help="toot the quote")
args = parser.parse_args()
config = vars(args)

class Arrsten:

    # List of novels

    novels = []

    novels.append( { "title" : "Pride And Prejudice", "file" : "prideandprejudice.txt", "author" : "Jane Austen" } )
    novels.append( { "title" : "Sense And Sensibility", "file" : "senseandsensibility.txt", "author" : "Jane Austen" } )
    novels.append( { "title" : "Northanger Abbey", "file" : "northangerabbey.txt", "author" : "Jane Austen" } )
    novels.append( { "title" : "Mansfield Park", "file" : "mansfieldpark.txt", "author" : "Jane Austen" } )
    novels.append( { "title" : "Persuasion", "file" : "persuasion.txt", "author" : "Jane Austen" } )
    novels.append( { "title" : "Emma", "file" : "emma.txt", "author" : "Jane Austen" } )

    # List of piratey phrases to add to content

    phrases = []
    phrases.append("Yarrr")
    phrases.append("Arrr")
    phrases.append("Arrgh")
    phrases.append("Garrr")
    phrases.append("Shiver my timbers")
    phrases.append("Splice the mainbrace")
    phrases.append("Yo-ho-ho, and a bottle of rum")
    phrases.append("Drink and the devil")
    phrases.append("Devil take you")
    phrases.append("Damn your eyes")
    phrases.append("Flop like a fish")
    phrases.append("Fever and leaches")
    phrases.append("All hands on deck")
    phrases.append("Avast you")
    phrases.append("Avast behind")
    phrases.append("Sink me")
    phrases.append("Blast my binnacle")
    phrases.append("Swash my buckle")
    phrases.append("Powder my monkey")
    phrases.append("Batten down the hatches")
    phrases.append("Blow the man down")
    phrases.append("Feed the fish")
    phrases.append("Roger my jolly")
    phrases.append("Wag my scally")
    phrases.append("Scuttle my poop")
    phrases.append("There she blows")
    phrases.append("Son of a biscuit eater")
    phrases.append("Three sheets to the wind")
    phrases.append("Woggle my horn")
    phrases.append("Dead men tell no tales")
    phrases.append("Slap my dungbie")
    phrases.append("Swab the deck")
    phrases.append("All aboard the Skylark")
    phrases.append("Widen your berth")
    phrases.append("Show a leg there")
    phrases.append("Beware the doldrums")
    phrases.append("Lost in deep water")
    phrases.append("All at sea")
    phrases.append("High and dry")
    phrases.append("Close to the wind")
    phrases.append("Sink or swim")
    phrases.append("You blasted boat rocker")
    phrases.append("Loose your cannons")
    phrases.append("Fashion my bristols")
    phrases.append("Shape my ship")
    phrases.append("Copper my bottom")
    phrases.append("Land my lubbers")
    phrases.append("Cut my jib")
    phrases.append("Scrape my barrel")
    phrases.append("Trim my sails")
    phrases.append("Broaden my beam")
    phrases.append("Abandon ship")
    phrases.append("Chock my blocks")
    phrases.append("Fly my crows")
    phrases.append("Stem my tides")
    phrases.append("Hard about")
    phrases.append("Sail and spray")
    phrases.append("Toast the devil")
    phrases.append("Glut the hold")
    phrases.append("Free the lines")
    phrases.append("Square the yards")
    phrases.append("On a Westward wind")
    phrases.append("Bones and beaches")
    phrases.append("Up the mizzen")

    regular_verbs = [
        "accept",
        "add",
        "admire",
        "agree",
        "allow",
        "appear",
        "argue",
        "arrive",
        "ask",
        "base",
        "believe",
        "call",
        "carry",
        "cause",
        "change",
        "choose",
        "claim",
        "close",
        "conceal",
        "consider",
        "continue",
        "cover",
        "create",
        "dare",
        "decide",
        "declare",
        "describe",
        "deserve",
        "determine",
        "detest",
        "develop",
        "die",
        "drop",
        "end",
        "enter",
        "expect",
        "explain",
        "face",
        "fail",
        "feel",
        "fill",
        "focus",
        "follow",
        "forget",
        "happen",
        "hate",
        "help",
        "hope",
        "identify",
        "include",
        "increase",
        "indicate",
        "involve",
        "join",
        "kill",
        "know",
        "laugh",
        "lay",
        "like",
        "listen",
        "live",
        "look",
        "love",
        "move",
        "need",
        "note",
        "occur",
        "offer",
        "open",
        "owe",
        "pass",
        "pick",
        "place",
        "plan",
        "play",
        "point",
        "prefer",
        "prepare",
        "produce",
        "protect",
        "provide",
        "pull",
        "push",
        "raise",
        "reach",
        "realize",
        "receive",
        "recognize",
        "reduce",
        "remain",
        "remember",
        "report",
        "represent",
        "require",
        "return",
        "save",
        "say",
        "see",
        "seem",
        "serve",
        "share",
        "start",
        "stay",
        "stop",
        "suggest",
        "support",
        "take",
        "talk",
        "tear",
        "thank",
        "think",
        "try",
        "turn",
        "use",
        "wait",
        "walk",
        "walk",
        "want",
        "watch",
        "wonder",
        "work"
    ]

    # Simple translations, eg. "am" is translated to "be"

    simple_translations = {
        "i"       : "oi",
        "am"      : "be",
        "are"     : "be",
        "is"      : "be",
        "was"     : "were",
        "were"    : "was",
        "your"    : "yer",
        "yours"   : "yers",
        "you're"  : "yer",
        "you"     : "yer",
        "for"     : "fer",
        "my"      : "me",
        "and"     : "an'",
        "yes"     : "aye",
        "hello"   : "ahoy",
        "hi"      : "ahoy",
        "there"   : "ther",
        "the"     : "thur",
        "their"   : "theys",
        "he"      : "hee",
        "our"     : "arr",
        "to"      : "ter",
        "into"    : "inter",
        "of"      : "o'",
        "nonsense" : "narnsense",
        "like"    : "loike"
    }

    # Prefixes, eg. Remove leading "H" so "Hold Hands" becomes "'Old Ands"

    prefixes = {}
    prefixes["h"] = "'"

    # Suffixes, eg. Remove training "ing" so "Looking" becomes "Lookin'"

    suffixes = {}
    suffixes["(\w\w\w)ing"] = "\\1in'"
    suffixes["(\w\w\w)ings"] = "\\1in's"
    suffixes["(\w\w\w)ingly"] = "\\1in'ly"

    # Infixes, eh. Remove internal "h" so "inexhaustible" becomes "inex'austible"

    infixes = {}
    infixes["([^acegiopstw])h"] = "\\1\'"
    
    # Translate a line of text into pirate speak

    def translate(self, text):

        work = text

        # "I ask" becomes "I do ask"

        for verb in self.regular_verbs:
            work = re.sub(r'\b(I|you|we)\s+('+verb+r')\b', r'\1 do '+DELIMITER+r'\2'+DELIMITER, work, flags=re.IGNORECASE)
        
        # "He asks" becomes "He do ask"

        for verb in self.regular_verbs:
            work = re.sub(r'\b(he|she|one)\s('+verb+r')s\b', r'\1 do '+DELIMITER+r'\2'+DELIMITER, work, flags=re.IGNORECASE)
        
        # "I asked" become "I did ask"

        for verb in self.regular_verbs:
            work = re.sub(r'\b(I|you|we|he|she|one|they)\s+('+verb+r')d\b', r'\1 did '+DELIMITER+r'\2'+DELIMITER, work, flags=re.IGNORECASE)

        work = re.sub(DELIMITER, '', work)

        # "Hello" becomes "Ahoy" etc

        for key, value in self.simple_translations.items():
            work = re.sub('\\b'+key+'\\b', DELIMITER+value+DELIMITER, work)
            key = key.capitalize()
            value = value.capitalize()
            work = re.sub('\\b'+key+'\\b', DELIMITER+value+DELIMITER, work)

        work = re.sub(DELIMITER, '', work)

        # "Happines" become "'appiness" etc

        for key, value in self.prefixes.items():
            work = re.sub('\\b'+key, value, work)
            key = key.capitalize()
            value = value.capitalize()
            work = re.sub('\\b'+key, value, work)
        
        # "Working" becomes "Workin'" etc

        for key, value in self.suffixes.items():
            work = re.sub(key+'\\b', value, work)

        # "Exhume" become "Ex'ume" etc

        for key, value in self.infixes.items():
            work = re.sub(key, value, work, flags=re.IGNORECASE)

        # "O' a" become "Orra" etc

        work = re.sub(r"\bo'\s+(a|e|i|o|u)\b", r"orr\1", work, flags=re.IGNORECASE)

        return work

    def add_phrase(self, text):

        work = text

        # Add a piratey phrase at start or end

        phrase = random.choice(self.phrases)
        choice = random.randint(0,1)
        if ( choice == 0):
            if ( work.startswith('"')):
                work = '"'+phrase+'! '+work[1:]
            else:
                work = phrase+'! '+work;
        else:
            if ( work.endswith('"')):
                work = work[:-1]+' '+phrase+'!"';
            else:
                work = work+' '+phrase+'!';

        return work
    
    def add_hashtags(self, text, author, title):
        
        # Add hashtags

        work = text

        author = '#'+re.sub(r'\W+', '',string.capwords(author))
        title = '#'+re.sub(r'\W+', '',string.capwords(title))
        work = work+'\n\n'+author+' '+title

        return work

    def select_quote(self):

        quote = DEFAULT_QUOTE

        choice = random.randint(0,3)

        if (choice == 0):

            if(config["debug"]):
                print("DEBUG: Reading from data file")

            # Read data file  ``

            f = open('data/quotes.json')
            data = json.load(f)
            quotes = data['quotes']
            f.close()

            # Pick quote at random

            quote = random.choice(quotes)
            if ( config["debug"]):
                print("DEBUG: Text = '"+quote["text"]+"'")

        else:

            # Choose random novel

            novel = random.choice(self.novels)

            if(config["debug"]):
                print("DEBUG: Reading from novel: "+novel["title"])

            # Split novel into sentences

            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            fp = open("data/"+novel["file"])
            data = fp.read()
            tokens = tokenizer.tokenize(data)

            # Pick random token
            # Try a few times if it too short or too long or doesnt translate well

            text = random.choice(tokens)
            text = re.sub('\n+', ' ', text)
            work = self.translate(text)
            for x in range(500):
                if ( config["debug"]):
                    print("DEBUG: Text = '"+text+"'")
                bad = False
                if ( len(text) < 30 ):
                    if ( config["debug"]):
                        print("DEBUG: Text was too short")
                    bad = True
                if ( len(text) > 450 ):
                    if ( config["debug"]):
                        print("DEBUG: Text was too long")
                    bad = True
                if ( text == work ):
                    if ( config["debug"]):
                        print("DEBUG: Translation was too boring")
                    bad = True
                if ( bad ):
                    text = random.choice(tokens)
                    text = re.sub('\n+', ' ', text)
                    work = self.translate(text)
                else:
                    break

            # Hack to handle tokenizer splitting without checking " characters

            if(text.count('"')%2 == 1):
                if(text.endswith('"')):
                    text = '"'+text
                else:
                    text = text+'"'

            # Create quote structure

            quote = {
                "text"   : text,
                "author" : novel["author"],
                "title"  : novel["title"]
            }
        
        return quote
    
    def process_quote(self, quote):

        work = quote["text"]
        if ( config["debug"]):
            print("DEBUG: Text = '"+work+"'")

        # Add piratey phrases

        work = self.add_phrase(work)
        if ( config["debug"]):
            print("DEBUG: With phrase = '"+work+"'")

        # Translate

        work = self.translate(work)
        if ( config["debug"]):
            print("DEBUG: Translated = '"+work+"'")

        # Add hashtags

        work = self.add_hashtags(work, quote["author"], quote["title"])
        if ( config["debug"]):
            print("DEBUG: With hashtags = '"+work+"'")

        # Return result

        quote["text"] = work

        return quote

    # Run class

    def run(self):

        original = self.select_quote()
        processed = self.process_quote(original)

        # Try a few times if result is too long
        for y in range(10):
            if ( len(processed["text"]) > 500):
                if ( config["debug"] ):
                    print("DEBUG: Result was too long")
                original = self.select_quote()
                processed = self.process_quote(original)

        if ( len(processed["text"]) > 500):
            processed = DEFAULT_QUOTE

        print( processed["text"] )

        if( config["toot"] ):
            mastodon = Mastodon(
                access_token = 'token.secret',
                api_base_url = 'https://botsin.space/'
            )
            mastodon.status_post(processed["text"])

# Instantiate class and run it

arrsten = Arrsten()
arrsten.run()
