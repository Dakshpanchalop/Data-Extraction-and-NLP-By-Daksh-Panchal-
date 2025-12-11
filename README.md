Objective
The objective is to extract textual data articles from the given URL and perform text analysis to compute stop words and variables.
All the steps mentioned below are after the extraction of articles using beautiful soups and newspaper3k libraries, Folder name: (articles).

STEP 1 — Stop Words Preparation
•	All stop word files are combined into a single list
•	Converted into lowercase and duplicates removed
•	Output saved as (compiled_stopwords.pkl)
•	These stop words are removed later during text cleaning

STEP 2 — Text Cleaning
 Process done for each article in the articles/ folder:
•	Removing punctuations & special characters
•	Removing stop words using the combined list
•	Tokenization (split into words)
Cleaned files are stored inside folder (cleaned articles)

STEP 3 — Sentiment Analysis
Using dictionaries from folder (Master Dictionary)
•	positive-words.txt
•	negative-words.txt
Calculated Metrics:
•	Positive Score
•	Negative Score
•	Polarity Score
➝ Polarity = (Positive – Negative) / (Positive + Negative + 0.000001)
•	Subjectivity Score
➝ Subjectivity = (Positive + Negative) / (Total Words + 0.000001)
Result saved as: Sentiment_Scores.csv

STEP 4 — Readability Statistics
•	Word Count
•	Complex Word Count
•	Percentage Complex Words
•	Average Sentence Length
•	Fog Index
➝ Fog Index = 0.4 × (Average Sentence Length + % Complex Words)
•	Personal Pronouns Count
•	Syllable Count per Word
•	Average Word Length
Results saved as: Readability_Scores.csv

STEP 5 — Finalizing Output in Excel file
We merged:
•	Input.xlsx
•	Sentiment scores
•	Readability scores
Final output: Output Data Structure.xlsx

How to run the main.py file to generate output
•	The main.py file is provided and should be ran in the order as mentioned below
•	Steps Below:
•	compile_stopwords
•	clean_articles
•	sentiment_analysis
•	readability_analysis
•	generate_final_output


All dependencies required
•	VS-Code / Jupyter Notebook
•	Pandas
•	OS
•	Beautiful Soups (web scraping)
•	Newspaper3k (web scraping)
•	Openpyxl (required by pandas for Excel export)
•	Pickle (used for loading stop words)
•	RE (Regex used for text cleaning)
