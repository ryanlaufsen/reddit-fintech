import pandas as pd
import spacy
import en_core_web_sm
import re
import emoji
import praw
import nltk
import demoji
from nltk.tokenize import RegexpTokenizer
from praw.models import MoreComments
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import FreqDist

nltk.download('wordnet')

df = pd.read_csv('daily_discussion_moves.csv')

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

grouped_comments = df.groupby('Date')

grouped_comments['Comment'].apply(lambda x: ' '.join(x))

print

dirty_comment = []

# append all the comments into a list
for comment in df['Comment']:
    dirty_comment.append(comment)

# print(dirty_comment)
# preprocessing string
list1 = dirty_comment
list1 = [str(i) for i in list1]
string_uncleand = ','.join(list1)


# print(string_uncleand)

# remove emoji,gif

def remove_emojis(text):
    return demoji.replace(text, '')


emojiless = re.sub(r'\\[a-zA-Z0-9]+', '', string_uncleand)
emojiless = re.sub(r'\[\w+\]\(emote\|t5_\w+\|\d+\)', '', emojiless)
emojiless = re.sub(r'\[\w+\]\(emote\|free_emotes_pack\|\w+\)', '', emojiless)

#print(emojiless)



# tokenizing and cleaning strings
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
tokenized_string = tokenizer.tokenize(emojiless)
#print(tokenized_string)

#preproccing string - converting tokens into lowercase
lower_string_tokenized = [word.lower() for word in tokenized_string]
#print(lower_string_tokenized)

#removing stopwords
nlp = en_core_web_sm.load()

all_stopwords = nlp.Defaults.stop_words

text = lower_string_tokenized
tokens_without_sw = [word for word in text if not word in all_stopwords]
#print(tokens_without_sw)

#normalizing words via lemmatizing

lemmatizer = WordNetLemmatizer()

lemmatized_tokens = ([lemmatizer.lemmatize(w) for w in tokens_without_sw])


#store lemmatized words into a new variable
cleand_output = lemmatized_tokens

#print('Original length of words = ' , (len(string_uncleand)))
#print("num of words after removing emotes and gif = ",(len(emojiless)))
#print("num of words after removing tokeninzing and cleaning =",(len(tokenized_string)) )
#print("num of words after reoving tokenizing, cleeaening and removing stop words = ",(len(tokens_without_sw)))
#print("num of words after removing tokenizing, cleaning , removing stop words and lemmatized =",(len(lemmatized_tokens)))
#print("num of words after final cleaning =",len(cleand_output))

#Calculating polarity score of words