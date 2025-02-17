import nltk
import random
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from transformers import pipeline, Conversation

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

class Chatbot:
    def __init__(self, use_ai=False):
        """
        If use_ai is True, the bot will generate responses using DialoGPT
        (via Hugging Face's Transformers). Otherwise, it uses predefined responses.
        """
        self.use_ai = use_ai
        self.lemmatizer = WordNetLemmatizer()
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
        if self.use_ai:
            self.conversational_pipeline = pipeline("conversational", model="microsoft/DialoGPT-medium")

    def _initialize_intent_keywords(self):
        intent_keywords_raw = {
            'greeting': ['hello', 'hi', 'hey', 'greetings', 'howdy'],
            'farewell': ['bye', 'goodbye', 'see you', 'later'],
            'joke': ['joke', 'laugh', 'funny', 'hilarious'],
            'thanks': ['thank you', 'thanks', 'appreciate']
        }
        intent_keywords = {}
        for intent, phrases in intent_keywords_raw.items():
            processed_phrases = []
            for phrase in phrases:
                phrase = phrase.lower().translate(str.maketrans('', '', string.punctuation))
                tokens = word_tokenize(phrase)
                if tokens:
                    lemmatized_tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
                    processed_phrases.append(' '.join(lemmatized_tokens))
            intent_keywords[intent] = list(set(processed_phrases))
        return intent_keywords

    def preprocess(self, text):
        """
        Preprocess the text: lower-case, remove punctuation, tokenize,
        remove stop words, and lemmatize.
        Returns both the token list and the cleaned text (for phrase matching).
        """
        text_clean = text.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text_clean)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]
        lemmatized_tokens = [self.lemmatizer.lemmatize(word) for word in filtered_tokens]
        return lemmatized_tokens, text_clean

    def detect_intent(self, tokens, text_clean):
        """
        Checks the preprocessed tokens and the cleaned text against the keywords.
        Returns the intent with the most keyword matches.
        """
        max_matches = 0
        best_intent = 'fallback'
        for intent, phrases in self.intent_keywords.items():
            matches = 0
            for phrase in phrases:
                if ' ' in phrase:
                    if phrase in text_clean:
                        matches += 1
                else:
                    if phrase in tokens:
                        matches += 1
            if matches > max_matches:
                max_matches = matches
                best_intent = intent
        return best_intent

    def get_response(self, intent, user_input):
        """
        Returns a response. If use_ai is True, use DialoGPT (via Hugging Face)
        to generate a response based on the input. Otherwise, use a predefined response.
        """
        if self.use_ai:
            try:
                conversation = Conversation(user_input)
                result = self.conversational_pipeline(conversation)
                return result.generated_responses[-1]
            except Exception as e:
                print("Error with conversational AI:", e)
                return "I'm having trouble thinking right now. Can you try again?"
        else:
            return random.choice(self.responses.get(intent, self.responses['fallback']))

    def start_chat(self):
        print("Bot: Hello! I'm your chatbot. How can I help you today?")
        while True:
            try:
                user_input = input("You: ").strip()
            except EOFError:
                print("\nBot: Goodbye!")
                break
            if not user_input:
                continue
            tokens, text_clean = self.preprocess(user_input)
            intent = self.detect_intent(tokens, text_clean)
            response = self.get_response(intent, user_input)
            print(f"Bot: {response}")
            if intent == 'farewell':
                break

if __name__ == "__main__":
    chatbot = Chatbot(use_ai=True)
    chatbot.start_chat()
