import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import re
from newspaper import Article

# Read the input Excel file
df = pd.read_excel("Input.xlsx")

# No need to scrape again if articles are already scraped
# Uncomment the below code to perform scraping from scratch.



# # Create folder for saving articles (if not exists)
# output_folder = "articles"
# os.makedirs(output_folder, exist_ok=True)

# def extract_article_text(url):
#     try:
#         response = requests.get(url, timeout=10)
#         soup = BeautifulSoup(response.content, "html.parser")

#         # Remove script & style tags
#         for tag in soup(["script", "style", "noscript"]):
#             tag.decompose()

#         # Extract visible text from paragraphs
#         paragraphs = soup.find_all('p')
#         article_text = "\n".join([p.get_text(strip=True) for p in paragraphs])

#         return article_text if article_text.strip() else None

#     except Exception as e:
#         print(f"Error fetching {url}: {e}")
#         return None


# for index, row in df.iterrows():
#     url_id = row["URL_ID"]
#     url = row["URL"]

#     print(f"Scraping {url_id} {url}")

#     article_text = extract_article_text(url)

#     if article_text:
#         filename = os.path.join(output_folder, f"{url_id}.txt")
#         with open(filename, "w", encoding="utf-8") as file:
#             file.write(article_text)
#         print(f"Saved -{filename}")
#     else:
#         print(f"❌ Failed to extract content for {url_id}")

# print("\n All extractable articles are saved in 'articles' folder.")




# # Folders
# output_folder = "articles"
# os.makedirs(output_folder, exist_ok=True)

# # Load Input.xlsx
# df = pd.read_excel("Input.xlsx")

# # Prepare list of URLs to retry (only not-yet-scraped files)
# retry_urls = []
# for _, row in df.iterrows():
#     url_id, url = row["URL_ID"], row["URL"]
#     file_path = os.path.join(output_folder, f"{url_id}.txt")
#     if not os.path.exists(file_path):
#         retry_urls.append((url_id, url))

# print(f"Total URLs to retry: {len(retry_urls)}")


# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# def scrape_bs(url):
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         soup = BeautifulSoup(res.content, "html.parser")
#         for tag in soup(["script", "style", "noscript"]):
#             tag.decompose()
#         paragraphs = soup.find_all("p")
#         text = "\n".join(p.get_text(strip=True) for p in paragraphs)
#         return text if text.strip() else None
#     except:
#         return None

# def scrape_newspaper(url):
#     try:
#         article = Article(url)
#         article.download()
#         article.parse()
#         return article.text if article.text.strip() else None
#     except:
#         return None


# still_failed = []

# for url_id, url in retry_urls:
#     print(f"\nScraping {url_id}: {url}")
    
#     text = scrape_bs(url)
#     if not text:
#         print(" Beautifulsoup failed, trying Newspaper3k...")
#         text = scrape_newspaper(url)

#     if text:
#         file_path = os.path.join(output_folder, f"{url_id}.txt")
#         with open(file_path, "w", encoding="utf-8") as f:
#             f.write(text)
#         print(f" Saved {file_path}")
#     else:
#         print(" ❌ Still failed")
#         still_failed.append((url_id, url))



# ---- STEP 1: Compile StopWords ----
import pickle

STOPWORDS_DIR = "StopWords"   # Folder contains all 7 stopwords files
OUTPUT_STOPWORDS = "compiled_stopwords.pkl"

def load_stopwords(folder):
    stopwords = set()
    
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder, filename)
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    word = line.strip().lower()
                    if word and word.isalpha():  # remove numbers and special chars
                        stopwords.add(word)
    
    return stopwords


if __name__ == "__main__":
    stopwords = load_stopwords(STOPWORDS_DIR)

    with open(OUTPUT_STOPWORDS, "wb") as f:
        pickle.dump(stopwords, f)

    print(f"Total StopWords Loaded: {len(stopwords)}")
    print("Sample Stopwords:", list(stopwords)[:25])
    print(f"Saved compiled stopwords to: {OUTPUT_STOPWORDS}")



# ---- STEP 2: Clean & Preprocess Articles ----

ARTICLES_DIR = "articles"
OUTPUT_DIR = "cleaned_articles"
STOPWORDS_PATH = "compiled_stopwords.pkl"

# Load stopwords
with open(STOPWORDS_PATH, "rb") as f:
    stopwords = pickle.load(f)

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def clean_text(text):
    text = text.lower()                                      # Lowercase
    text = re.sub(r'[^a-z\s]', ' ', text)                    # Remove punctuation & numbers
    words = text.split()                                     # Tokenize
    filtered_words = [w for w in words if w not in stopwords]
    return " ".join(filtered_words)


for filename in os.listdir(ARTICLES_DIR):
    if filename.endswith(".txt"):
        file_path = os.path.join(ARTICLES_DIR, filename)
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()

        cleaned = clean_text(raw_text)

        out_path = os.path.join(OUTPUT_DIR, filename)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"Processed: {filename}")

print("\n All text articles cleaned successfully.")
print(f"Cleaned files saved in folder: {OUTPUT_DIR}")



# ---- STEP 3: Sentiment Analysis ----


CLEANED_DIR = "cleaned_articles"
POS_PATH = "MasterDictionary/positive-words.txt"
NEG_PATH = "MasterDictionary/negative-words.txt"

# Load positive and negative words
def load_words(filepath):
    words = set()
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            w = line.strip().lower()
            if w.isalpha():
                words.add(w)
    return words

positive_words = load_words(POS_PATH)
negative_words = load_words(NEG_PATH)

results = []

for filename in os.listdir(CLEANED_DIR):
    if filename.endswith(".txt"):
        path = os.path.join(CLEANED_DIR, filename)

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            words = text.split()

        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)

        polarity = (pos_count - neg_count) / ((pos_count + neg_count) + 0.000001)
        subjectivity = (pos_count + neg_count) / (len(words) + 0.000001)

        url_id = filename.split(".")[0]

        results.append({
            "URL_ID": url_id,
            "Positive Score": pos_count,
            "Negative Score": neg_count,
            "Polarity Score": polarity,
            "Subjectivity Score": subjectivity
        })

df = pd.DataFrame(results)
df.to_csv("Sentiment_Scores.csv", index=False)

print("\nSentiment Analysis completed.")
print("Output saved as: Sentiment_Scores.csv")



# ---- STEP 4: Readability & Text Statistics ----


CLEANED_DIR = "cleaned_articles"

# Count syllables
def count_syllables(word):
    word = word.lower()
    vowels = "aeiou"
    count = 0
    if word and word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i-1] not in vowels:
            count += 1
    if word.endswith("es") or word.endswith("ed"):
        count -= 1
    if count <= 0:
        count = 1
    return count

results = []

for filename in os.listdir(CLEANED_DIR):
    if filename.endswith(".txt"):
        path = os.path.join(CLEANED_DIR, filename)
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        words = text.split()
        word_count = len(words)

        syllable_count = sum(count_syllables(w) for w in words)
        avg_syllables_per_word = syllable_count / (word_count + 0.000001)

        complex_words = [w for w in words if count_syllables(w) >= 3]
        complex_word_count = len(complex_words)

        percent_complex_words = complex_word_count / (word_count + 0.000001)

        # Sentence count using punctuation references
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if len(s.split()) > 1]
        sentence_count = len(sentences)
        avg_sentence_length = word_count / (sentence_count + 0.000001)

        fog_index = 0.4 * (avg_sentence_length + percent_complex_words)

        # Personal pronouns
        pronouns = re.findall(r'\b(i|we|my|ours|us)\b', text, flags=re.IGNORECASE)
        personal_pronouns = len(pronouns)

        # Average word length
        char_count = sum(len(w) for w in words)
        avg_word_length = char_count / (word_count + 0.000001)

        url_id = filename.split(".")[0]

        results.append({
            "URL_ID": url_id,
            "Word Count": word_count,
            "Complex Word Count": complex_word_count,
            "% Complex Words": percent_complex_words,
            "Average Sentence Length": avg_sentence_length,
            "Fog Index": fog_index,
            "Syllable Per Word": avg_syllables_per_word,
            "Personal Pronouns": personal_pronouns,
            "Average Word Length": avg_word_length
        })

df = pd.DataFrame(results)
df.to_csv("Readability_Scores.csv", index=False)

print("\nReadability Analysis completed.")
print("Output saved as: Readability_Scores.csv")



# --- STEP 5: Final Output File ---

# Load our previous results
sent_df = pd.read_csv("Sentiment_Scores.csv")
read_df = pd.read_csv("Readability_Scores.csv")

# Load input sheet to get URLs
input_df = pd.read_excel("Input.xlsx")

# Merge results based on URL_ID column
final_df = input_df.merge(sent_df, on="URL_ID", how="left")
final_df = final_df.merge(read_df, on="URL_ID", how="left")

# Save final result
final_df.to_excel("Output Data Structure.xlsx", index=False)

print("File saved as: Output Data Structure.xlsx")
