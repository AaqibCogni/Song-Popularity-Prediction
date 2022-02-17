#!/usr/bin/env python
# coding: utf-8
import re
import random
from langdetect import detect_langs
from bs4 import BeautifulSoup
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from tqdm import tqdm


# # Preprocessing Lyrics field of All Songs Data
# 
# In the Preprocessing phase we do the following in the order below:-
# 
# 1. Begin by removing round, square (along with text ) and curly brackets.
# 2. Remove line breaks from the text.
# 3. Detect and Remove non English Songs
# 4. Remove any punctuations or limited set of special characters like , or . or # etc.
# 5. Check if tags are present
# 6. Check if the word is made up of english letters and is not alpha-numeric
# 7. Check to see if the length of the word is greater than 2
# 8. Detect and replace contractions with original word.
# 9. Convert the word to lowercase

# Import Dataset
all_song_data = pd.read_excel(r'"D:\.....\All Song Data with Popularity.xlsx"')


# # Functions Created For Preprocessing

# Detect Non English Songs from the list of Songs
def get_eng_prob(text):
    detections = detect_langs(text)
    for detection in detections:
        if detection.lang == 'en':
            return detection.prob
    return 0

# Function to replace contractions with actual words
def contracted(phrase): 
    phrase = re.sub(r"ain't", "am not",phrase)
    phrase = re.sub("aren't", "are not",phrase)
    phrase = re.sub("can't", "cannot",phrase)
    phrase = re.sub("can't've", "cannot have",phrase)
    phrase = re.sub("cause", "because",phrase)
    phrase = re.sub("could've", "could have",phrase)
    phrase = re.sub("couldn't", "could not",phrase)
    phrase = re.sub("couldn't've", "could not have",phrase)
    phrase = re.sub("didn't", "did not",phrase)
    phrase = re.sub("doesn't", "does not",phrase)
    phrase = re.sub("don't", "do not",phrase)
    phrase = re.sub("hadn't", "had not",phrase)
    phrase = re.sub("hadn't've", "had not have",phrase)
    phrase = re.sub("hasn't", "has not",phrase)
    phrase = re.sub("haven't", "have not",phrase)
    phrase = re.sub("he'd", "he had",phrase)
    phrase = re.sub("he'd've", "he would have",phrase)
    phrase = re.sub("he'll", "he will",phrase)
    phrase = re.sub("he'll've", "he will have",phrase)
    phrase = re.sub("he's", "he has",phrase)
    phrase = re.sub("how'd", "how did",phrase)
    phrase = re.sub("how'd'y", "how do you",phrase)
    phrase = re.sub("how'll", "how will",phrase)
    phrase = re.sub("how's", "how is",phrase)
    phrase = re.sub("I'd", "I would",phrase)
    phrase = re.sub("I'd've", "I would have",phrase)
    phrase = re.sub("I'll", "I will",phrase)
    phrase = re.sub("I'll've", "I will have",phrase)
    phrase = re.sub("I'm", "I am",phrase)
    phrase = re.sub("I've", "I have",phrase)
    phrase = re.sub("isn't", "is not",phrase)
    phrase = re.sub("it'd", "it had",phrase)
    phrase = re.sub("it'd've", "it would have",phrase)
    phrase = re.sub("it'll", "it will",phrase)
    phrase = re.sub("it'll've", "it will have",phrase)
    phrase = re.sub("it's", "it is",phrase)
    phrase = re.sub("let's", "let us",phrase)
    phrase = re.sub("ma'am", "madam",phrase)
    phrase = re.sub("mayn't", "may not",phrase)
    phrase = re.sub("might've", "might have",phrase)
    phrase = re.sub("mightn't", "might not",phrase)
    phrase = re.sub("mightn't've", "might not have",phrase)
    phrase = re.sub("must've", "must have",phrase)
    phrase = re.sub("mustn't", "must not",phrase)
    phrase = re.sub("mustn't've", "must not have",phrase)
    phrase = re.sub("needn't", "need not",phrase)
    phrase = re.sub("needn't've", "need not have",phrase)
    phrase = re.sub("o'clock", "of the clock",phrase)
    phrase = re.sub("oughtn't", "ought not",phrase)
    phrase = re.sub("oughtn't've", "ought not have",phrase)
    phrase = re.sub("shan't", "shall not",phrase)
    phrase = re.sub("sha'n't", "shall not",phrase)
    phrase = re.sub("shan't've", "shall not have",phrase)
    phrase = re.sub("she'd", "she had / she would",phrase)
    phrase = re.sub("she'd've", "she would have",phrase)
    phrase = re.sub("she'll", "she will",phrase)
    phrase = re.sub("she'll've", "she will have",phrase)
    phrase = re.sub("she's", "she is",phrase)
    phrase = re.sub("should've", "should have",phrase)
    phrase = re.sub("shouldn't", "should not",phrase)
    phrase = re.sub("shouldn't've", "should not have",phrase)
    phrase = re.sub("so've", "so have",phrase)
    phrase = re.sub("so's", "so is",phrase)
    phrase = re.sub("that'd", "that had",phrase)
    phrase = re.sub("that'd've", "that would have",phrase)
    phrase = re.sub("that's", "that is",phrase)
    phrase = re.sub("there'd", "there had",phrase)
    phrase = re.sub("there'd've", "there would have",phrase)
    phrase = re.sub("there's", "there is",phrase)
    phrase = re.sub("they'd", "they had",phrase)
    phrase = re.sub("they'd've", "they would have",phrase)
    phrase = re.sub("they'll", "they will",phrase)
    phrase = re.sub("they'll've", "they will have",phrase)
    phrase = re.sub("they're", "they are",phrase)
    phrase = re.sub("they've", "they have",phrase)
    phrase = re.sub("to've", "to have",phrase)
    phrase = re.sub("wasn't", "was not",phrase)
    phrase = re.sub("we'd", "we would",phrase)
    phrase = re.sub("we'd've", "we would have",phrase)
    phrase = re.sub("we'll", "we will",phrase)
    phrase = re.sub("we'll've", "we will have",phrase)
    phrase = re.sub("we're", "we are",phrase)
    phrase = re.sub("we've", "we have",phrase)
    phrase = re.sub("weren't", "were not",phrase)
    phrase = re.sub("what'll", "what will",phrase)
    phrase = re.sub("what'll've", "what will have",phrase)
    phrase = re.sub("what're", "what are",phrase)
    phrase = re.sub("what's", "what is",phrase)
    phrase = re.sub("what've", "what have",phrase)
    phrase = re.sub("when's", "when is",phrase)
    phrase = re.sub("when've", "when have",phrase)
    phrase = re.sub("where'd", "where did",phrase)
    phrase = re.sub("where's", "where is",phrase)
    phrase = re.sub("where've", "where have",phrase)
    phrase = re.sub("who'll", "who will",phrase)
    phrase = re.sub("who'll've", "who will have",phrase)
    phrase = re.sub("who's", "who is",phrase)
    phrase = re.sub("who've", "who have",phrase)
    phrase = re.sub("why's", "why is",phrase)
    phrase = re.sub("why've", "why have",phrase)
    phrase = re.sub("will've", "will have",phrase)
    phrase = re.sub("won't", "will not",phrase)
    phrase = re.sub("won't've", "will not have",phrase)
    phrase = re.sub("would've", "would have",phrase)
    phrase = re.sub("wouldn't", "would not",phrase)
    phrase = re.sub("wouldn't've", "would not have",phrase)
    phrase = re.sub("y'all", "you all",phrase)
    phrase = re.sub("y'all'd", "you all would",phrase)
    phrase = re.sub("y'all'd've", "you all would have",phrase)
    phrase = re.sub("y'all're", "you all are",phrase)
    phrase = re.sub("y'all've", "you all have",phrase)
    phrase = re.sub("you'd", "you would",phrase)
    phrase = re.sub("you'd've", "you would have",phrase)
    phrase = re.sub("you'll", "you will",phrase)
    phrase = re.sub("you'll've", "you will have",phrase)
    phrase = re.sub("you're", "you are",phrase)
    phrase = re.sub("you've", "you have",phrase)
    return phrase

def cleanhtml(sentence): #function to clean htmltags
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, " ", sentence)
    return cleantext

def cleanpunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    return  cleaned

def preprocessing_lyrics(df):
    text_in_round_brackets = sum(list(df['Lyrics'].map(lambda s: re.findall(r'\((.*?)\)',str(s)))), [])
    print('Number of round brackets: {}'.format(len(text_in_round_brackets)))
    text_in_square_brackets = sum(list(df['Lyrics'].map(lambda s: re.findall(r'\[(.*?)\]',str(s)))), [])
    print('Number of square brackets: {}'.format(len(text_in_square_brackets)))
    text_in_curly_brackets = sum(list(df['Lyrics'].map(lambda s: re.findall(r'\{(.*?)\}',str(s)))), [])
    print('Number of Curly brackets: {}'.format(len(text_in_curly_brackets)))
    
    # remove round brackets but not text within
    df['Lyrics'] = df['Lyrics'].map(lambda s: re.sub(r'\(|\)', '', str(s)))
    # remove square brackets and text within
    df['Lyrics'] = df['Lyrics'].map(lambda s: re.sub(r'\[(.*?)\] ', '', str(s)))
    # remove Curly brackets and text within
    df['Lyrics'] = df['Lyrics'].map(lambda s: re.sub(r'\{|\} ', '', str(s)))
    
    # Detect and remove non english songs
    df['en_prob'] = df['Lyrics'].map(get_eng_prob)
    print('Number of english songs: {}'.format(sum(df['en_prob'] >= 0.8)))
    print('Number of non-english songs: {}'.format(sum(df['en_prob'] < 0.8)))  
    df = df.loc[df['en_prob']>= 0.8]
    df.reset_index(drop=True,inplace=True)
    
    # Check if tags are present in the lyrics field
    df['Tag Present'] = df['Lyrics'].map(lambda s : bool(BeautifulSoup(str(s), "html.parser").find()))
    
    i = 0
    final_lyrics = []
    s = ""
    for lyrics in tqdm(df["Lyrics"].values):
        filteredLyrics = []
        EachLyrics = ""
        lyricsHTMLCleaned = cleanhtml(lyrics)
        lyricsHTMLCleaned = contracted(lyricsHTMLCleaned)
        for eachWord in lyricsHTMLCleaned.split(): 
            for sentencePunctCleaned in cleanpunc(eachWord).split():
                if((sentencePunctCleaned.isalpha()) & (len(sentencePunctCleaned)>2)):
                    sentenceLower = sentencePunctCleaned.lower()
                    s = (sno.stem(sentenceLower))
                    filteredLyrics.append(s)
        EachLyrics = ' '.join(filteredLyrics)
        final_lyrics.append(EachLyrics)
    df['cleanedLyrics'] = final_lyrics    
    return df

all_song_data = preprocessing_lyrics(all_song_data)
