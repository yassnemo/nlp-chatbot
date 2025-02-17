import nltk
import random
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

nltk.download('punkt')
nltk.download('stopwords')

class SimpleChatbot:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))
        self.intent_keywords = self._initialize_intent_keywords()
        self.responses = {
            'greeting': ['Hello!', 'Hi there!', 'Greetings!'],
            'farewell': ['Goodbye!', 'See you later!', 'Bye!'],
            'joke': [
                'Why did the chicken cross the road? To get to the other side!',
                'What do you call fake spaghetti? An impasta!'
            ],
            'thanks': ['You are welcome!', 'No problem!', 'My pleasure!'],
            'fallback': [
                "I'm not sure I understand. Could you rephrase that?",
                "I didn't catch that. Can you say it again?"
            ]
        }

    def _initialize_intent_keywords(self):
        intent_keywords_raw = {
            'greeting': ['hello', 'hi', 'hey', 'greetings', 'howdy'],
            'farewell': ['bye', 'goodbye', 'later', 'see', 'soon'],
            'joke': ['joke', 'laugh', 'funny', 'hilarious'],
            'thanks': ['thank', 'thanks', 'appreciate'],
        }
        intent_keywords = {}
        for intent, keywords in intent_keywords_raw.items():
            processed_keywords = []
            for kw in keywords:
                kw = kw.lower().translate(str.maketrans('', '', string.punctuation))
                tokens = word_tokenize(kw)
                if tokens:
                    stemmed = self.stemmer.stem(tokens[0])
                    processed_keywords.append(stemmed)
            intent_keywords[intent] = list(set(processed_keywords))  # rm duplicates
        return intent_keywords

    def preprocess(self, text):
        text = text.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        stemmed_tokens = [self.stemmer.stem(word) for word in filtered_tokens]
        return stemmed_tokens

    def detect_intent(self, tokens):
        max_matches = 0
        best_intent = 'fallback'
        for intent, keywords in self.intent_keywords.items():
            matches = sum(1 for token in tokens if token in keywords)
            if matches > max_matches:
                max_matches = matches
                best_intent = intent
        return best_intent

    def get_response(self, intent):
        return random.choice(self.responses.get(intent, self.responses['fallback']))

    def start_chat(self):
        print("Bot: Hello! I'm your friendly chatbot. How can I help you today?")
        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                print("\nBot: Goodbye!")
                break
            if not user_input:
                continue
            processed_tokens = self.preprocess(user_input)
            intent = self.detect_intent(processed_tokens)
            response = self.get_response(intent)
            print(f"Bot: {response}")
            if intent == 'farewell':
                break

if __name__ == "__main__":
    chatbot = SimpleChatbot()
    chatbot.start_chat()