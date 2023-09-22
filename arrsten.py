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
 
MAX_LENGTH = 500

QUOTES_FILE = "data/quotes.json"

# Parse command line arguments

parser = argparse.ArgumentParser(description="Quote Like A Pirate", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-t", "--text", help="process the specified text")
parser.add_argument("-s", "--search", help="search for the quote")
parser.add_argument("-d", "--debug", action="store_true", help="debug mode (show original quote)")
parser.add_argument("-q", "--quiet", action="store_true", help="quiet mode (supress hashtags)")
parser.add_argument("-p", "--post", action="store_true", help="post the quote")

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
    phrases.append("Belay there")
    phrases.append("Sink me")
    phrases.append("Blast my binnacle")
    phrases.append("Swash my buckle")
    phrases.append("Powder my monkey")
    phrases.append("Tie my tiller down")
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
    phrases.append("Scrape my keel")
    phrases.append("There is red port left")
    phrases.append("Abaft the beam")
    phrases.append("No! my Starboard")
    phrases.append("Weevilly biscuits")
    phrases.append("Marque my letter")
    phrases.append("Bones and beaches")
    phrases.append("Up the mizzen")
    phrases.append("Loose the halliards")
    phrases.append("Under the flag of bones")
    phrases.append("Glug my grog")
    phrases.append("Anchor's aweigh")
    phrases.append("Plunder my booty")
    phrases.append("Up the mizzen")
    phrases.append("Move fast and break stuff")
    phrases.append("Beware the zombie scrum")
    phrases.append("Wrinkle my baggies")
    phrases.append("Balls to four watch")
    phrases.append("Beat that quarter")
    phrases.append("Wind and water")
    phrases.append("Bilged on her anchor")
    phrases.append("A bitter end")
    phrases.append("Tighten the boom vang")
    phrases.append("Brace for a broadside")
    phrases.append("Taste the cat")
    phrases.append("Caulk my planks")
    phrases.append("Truss up the clews")
    phrases.append("Hitch my cloves")
    phrases.append("Timber my horn")
    phrases.append("Up Jacob's ladder")
    phrases.append("Widen your joggle and nib")
    phrases.append("I'll be keelhauled")
    phrases.append("Kiss the gunner's daughter")
    phrases.append("Up the lubber's hole")
    phrases.append("Man overboard")
    phrases.append("Run before the wind")
    phrases.append("Swigging the rigging")
    phrases.append("Warm the bell")

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
    infixes["knowledge"] = "knarledge"
    
    # Try in vain to cleanup bad sentence splitting

    def clean_text(self, text):

        work = text

        # Get rid of duplicate white space

        work = re.sub('\s+',' ',work)

        # Hacks to try in vain to tidy up bad sentence splitting around double quotes

        # Handle... Oh Sir Percy!" she exclaimed... by adding a " at the start

        work = re.sub( r'^([^"]+)"\s+', r'"\1" ', work )

        # Handle... she exclaimed, "Oh Sir Percy!... by adding a " at the end

        work = re.sub( r'\s+"([^"]+)$', r' "\1" ', work )

        # If there are still an odd number of double quotes, add another at start or end

        if work.count('"')%2 == 1:
            if work.endswith('"'):
                work = '"'+work
            else:
                work = work+'"'

        return work

    # Translate a line of text into pirate speak

    def translate(self, text):

        work = text

        # Translate verbs

        # "I ask" becomes "I do ask" etc

        for verb in self.regular_verbs:
            work = re.sub(r'\b(I|you|we)\s+('+verb+r')\b', r'\1 do '+DELIMITER+r'\2'+DELIMITER, work, flags=re.IGNORECASE)
        
        # "He asks" becomes "He do ask" etc

        for verb in self.regular_verbs:
            work = re.sub(r'\b(he|she|one)\s('+verb+r')s\b', r'\1 do '+DELIMITER+r'\2'+DELIMITER, work, flags=re.IGNORECASE)
        
        # "I asked" become "I did ask" etc

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

    # Add a piratey phrase at start or end of text

    def add_phrase(self, text):

        work = text

        # Pick a random piratey phrase

        phrase = random.choice(self.phrases)

        # Decide where to put it (0=start, 1=end) but if possible put it
        # inside double quotes as it's funnier if a character is saying it

        choice = random.randint(0,1)
        choice = 1
        if choice == 0:

            # If text includes the start of a quote - eg. "Something

            if re.match( r'^[^"]*"\S', work ):
                i = work.find('"')
                work = work[:i+1]+phrase+"! "+work[i+1:]
            else:
                work = phrase+'! '+work;

        else:

            # If text includes the end of a quote - eg. Something."
            if work.rfind(',"') >= 0:
                i = work.rfind(',"')
                work = work[:i+1]+' '+phrase.lower()+"!"+work[i+1:]
            elif work.rfind('"') >= 0:
                i = work.rfind('"')
                work = work[:i]+' '+phrase+"!"+work[i:]
            else:
                work = work+' '+phrase+'!';

        return work
    
    def add_hashtags(self, text, author, title):
        
        # Add hashtags (or simple attribution if running in quiet mode)

        work = text

        if config["quiet"]:
            author = string.capwords(author)
            title = string.capwords(title)
            work = work+'\n\n'+author+', "'+title+'"'
        else:
            author = '#'+re.sub(r'\W+', '',string.capwords(author))
            title = '#'+re.sub(r'\W+', '',string.capwords(title))
            work = work+'\n\n'+author+' '+title+' '+'#TalkLikeAPirate'
        
        return work

    # Read quotes file

    def read_quotes_file(self):

        f = open(QUOTES_FILE)
        data = json.load(f)
        quotes = data['quotes']
        f.close()

        return quotes

    # Select quote from data files or from input

    def select_quote(self):

        quote = DEFAULT_QUOTE

        if config["text"]:

            # Use command line text if it was supplied

            quote["text"] = config["text"]

        elif config["search"]:

            # Search for text if it was requested

            quotes = self.read_quotes_file()
            
            for candidate in quotes:
                if re.search(config["search"], candidate["text"], re.IGNORECASE):
                    quote = candidate

        else:

            choice = random.randint(0,3)

            if choice == 0:

                # Read qoutes file and make a random choice

                quotes = self.read_quotes_file()
                quote = random.choice(quotes)

            else:

                # Choose random novel

                novel = random.choice(self.novels)

                # Read novel

                f = open("data/"+novel["file"])
                data = f.read()
                f.close()

                # Split novel into sentences

                tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
                tokens = tokenizer.tokenize(data)

                # Pick random token
                # Try a few times if it too short or too long or doesnt translate well

                text = random.choice(tokens)
                work = self.translate(text)
                for x in range(MAX_LENGTH):
                    bad = False
                    if len(text) < 30:
                        bad = True
                    if len(text) > MAX_LENGTH - 50:
                        bad = True
                    if text == work:
                        bad = True
                    if bad:
                        text = random.choice(tokens)
                        text = re.sub('\n+', ' ', text)
                        work = self.translate(text)
                    else:
                        break

                # Create quote structure

                quote = {
                    "text"   : text,
                    "author" : novel["author"],
                    "title"  : novel["title"]
                }
        
        return quote
    
    # Clean up quote, add a piratey phrase and translate the whole thing
    
    def process_quote(self, quote):

        work = quote["text"]

        # Clean up the text, ballancing quotes etc

        work = self.clean_text(work)

        # Add piratey phrases

        work = self.add_phrase(work)

        # Translate

        work = self.translate(work)

        # Add hashtags

        work = self.add_hashtags(work, quote["author"], quote["title"])

        # Return result

        quote["text"] = work

        return quote

    # Run class

    def run(self):

        # Select a random quote and process it

        original = self.select_quote()
        processed = self.process_quote(original)

        # Try a few more times if result is too long

        for y in range(10):
            if len(processed["text"]) > MAX_LENGTH:
                original = self.select_quote()
                processed = self.process_quote(original)

        # Give up if length is still too big

        if len(processed["text"]) > MAX_LENGTH:
            processed = DEFAULT_QUOTE

        print( processed["text"] )

        # Post result to mastodon if requested

        if config["post"]:

            mastodon = Mastodon(
                access_token = 'token.secret',
                api_base_url = 'https://botsin.space/'
            )

            mastodon.status_post(processed["text"])

# Instantiate class and run it

arrsten = Arrsten()
arrsten.run()
