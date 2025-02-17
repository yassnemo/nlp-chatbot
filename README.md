# 🤖 NLP Chatbot&#x20;

# 📌 Overview

This is an \*\* (NLP) chatbot\*\* that can respond to user messages using:

1. **Predefined rule-based responses** for basic intents (e.g., greetings, goodbyes, jokes...).
2. **AI-generated responses** using Microsoft's DialoGPT model via Hugging Face's Transformers library.

The chatbot can be used in either **rule-based mode** or **AI-powered mode**, making it flexible for different use cases.

## 🎯 Features

✅ Recognizes and responds to common intents (greetings, thanks, jokes).\
✅ Processes user input using **tokenization, stopword removal (to focus on the more meaningful and informative words in a text. ), and lemmatization (the process of grouping together different inflected forms of the same word)**.\
✅ Uses **Hugging Face's Transformers** to generate intelligent, context-aware replies.\
✅ Supports both **predefined responses** and **AI-generated responses**.

---

## 🚀 Installation Guide

### 1️⃣ **Clone the Repository**

```bash
git clone https://github.com/yassnemo/nlp-chatbot.git
cd chatbot-project
```

### 2️⃣ **Set Up a Virtual Environment (Optional but Recommended)**

- **Mac/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **Windows (PowerShell;Git):**
  ```powershell
  python -m venv venv
  venv\Scripts\activate
  ```

### 3️⃣ **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4️⃣ **Run the Chatbot**

```bash
python chatbot.py
```

---


## 📜 Simple Run Down For How It Works

1. **Text Preprocessing**

   - Converts user input to lowercase.
   - Removes punctuation and stopwords.
   - Uses **lemmatization** for better understanding.

2. **Intent Detection**

   - Matches processed input with predefined keywords.
   - If no clear intent is found, defaults to AI-generated responses.

3. **Response Generation**

   - **Rule-Based Mode:** Picks a response from predefined lists.
   - **AI Mode:** Uses **DialoGPT** via Hugging Face to generate replies. 

---

## 🧠 Using the AI-Powered Mode

By default, the chatbot runs with **AI Mode enabled**. To disable it and use only predefined responses, modify this line in `chatbot.py`:

```python
chatbot = Chatbot(use_ai=False)  # Change to True for AI powered responses
```

### 🔗 Hugging Face API Option

If you prefer to use Hugging Face's API instead of a local model:

1. Get a **free API key** from [Hugging Face](https://huggingface.co/settings/tokens).
2. Set it as an environment variable:
   ```bash
   export HF_API_KEY="your_api_key_here"
   ```
3. Modify `chatbot.py` to use the API.
