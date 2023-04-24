# 3. Wrenching Meaning From Chaos — How we selected our way of doing things

## The problem
When it came time to pick out mentions of stock symbols in the Reddit comments, we explored the possibility of using NER (named entity recognition). As such, we attempted to build a recognizer using NLTK and [SpaCy library](https://spacy.io/), but we quickly ran into trouble. Although stock symbols are key elements in the text of Reddit comments, we discovered that content on Reddit is quite deviant from what one would consider functional dialogue. There were far too many mentions of various entities, such the names of people's dogs, wives, and neighbours. (Interestingly, many comments made reference to the same few recurring figures in the world of finance and stock market trading. These popular figures went by a myriad of names: For example, Jerome Powell, the Chair of the Federal Reserve, is known to Redditors as "J-Pow", the "Money Printer", "The Fedfather", and "Printer-in-Chief.")

## The solution — kind of
With our team's collective years of experience scrolling on Reddit, we decided that top-level comments were usually well-formatted, with minimal grammatical or orthographic errors. With this in mind, we thought it effective enough for the purposes of this project to apply a simple regex that attempted to find exact (i.e. properly uppercased) matches of NASDAQ and NYSE tickers to a dataframe of listed companies. Besides, most comments were merely manifestations of people's daily rage — a series of senseless rants that had nothing to do with stock price and volume predictions.

## The second problem
Although we were right in assuming that most top-level comments were free of spelling mistakes, we could not get around the fact that many common words were also valid stock symbols. Let me illustrate our frustrations. Consider the following comment (excuse the profanity — it references a song by Mike Posner):

```
I took a pill in Ibiza

To show members of WSB I was cool

But when I lost $10k in one day to CPI, I was sad but fck it was something to do.
```

The above string, when cleaned, tokenized, and lemmatized, then run through this code:
```python
for index, row in tickers.iterrows():
        for ticker in row.values:
            if ticker in comment:
                mentioned_tickers.append(ticker)
