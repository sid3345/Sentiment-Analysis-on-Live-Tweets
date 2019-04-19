import re
import sys
#appending to system path for module detection
#from sentiment_analysis_python_GUI import Application

sys.path.append('C:\Python36\Lib\site-packages')
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import csv
#import matplotlib.pyplot as plt
#from sentiment_analysis_python_GUI import Application
#from sentiment_analysis_python_GUI import reveal

class TwitterClient(object):
            ''' Generic Twitter Class for sentiment analysis.   '''
            #sntTweets = csv.writer(open("sentiment_Tweet.csv", "wb"))
            p_count = 0
            n_count = 0
            neutral_count = 0

            def __init__(self):
                '''    Class constructor or initialization method.     '''
                # keys and tokens from the Twitter Dev Console
                consumer_key = 'yoIwFkjZGYDa49aO16XqSNqcN'
                consumer_secret = 'gl4LQOItV7Z1aFwNrlvaiKJ3t8o8h99blMIAmnmdHxYjzjRAxO' 
                access_token = '624310916-E7fDF2IE8P6bfY1oVFglASf6F8RnxMd3vgSXFqnZ'
                access_token_secret = 'ID9JcoXHsDcKtvNcnmBGcCQhUlO0wmwAxBJ6LCesiUAas'

                # attempt authentication
                try:
                    # create OAuthHandler object
                    self.auth = OAuthHandler(consumer_key, consumer_secret)
                    # set access token and secret
                    self.auth.set_access_token(access_token, access_token_secret)
                    # create tweepy API object to fetch tweets
                    self.api = tweepy.API(self.auth)
                except:
                    print("Error: Authentication Failed")

            def clean_tweet(self, tweet):
                '''
                Utility function to clean tweet text by removing links, special characters
                using simple regex statements.
                '''
                return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

            def get_tweet_sentiment(self, tweet):
                '''
                Utility function to classify sentiment of passed tweet
                using textblob's sentiment method
                '''

                # create TextBlob object of passed tweet text
                analysis = TextBlob(self.clean_tweet(tweet))
                # set sentiment
                if analysis.sentiment.polarity > 0:
                    return 'positive'
                elif analysis.sentiment.polarity == 0:
                    return 'neutral'
                else:
                    return 'negative'

                '''for row in tweets:
                    blob = TextBlob(self.clean_tweet(tweet))
                    if blob.sentiment.polarity > 0:
                        sntTweets.writerow([row[0], row[1], row[2], blob.sentiment.polarity, "positive"])
                    elif blob.sentiment.polarity < 0:
                        sntTweets.writerow([row[0], row[1], row[2], blob.sentiment.polarity, "negative"])
                    elif blob.sentiment.polarity == 0.0:
                        sntTweets.writerow([row[0], row[1], row[2], blob.sentiment.polarity, "neutral"])'''

            def get_tweets(self, query, count=10):
                '''     Main function to fetch tweets and parse them.   '''
                tweets = []    # empty list to store parsed tweets
                #tweet_csv = csv.writer(open("sentiment_Tweet", "a+b"))

                try:
                    # call twitter api to fetch tweets
                    fetched_tweets = self.api.search(q = query, count = count)

                    myFile = open('sentiment_tweet.csv', 'a')
                    myFile.truncate(0)
                    myFields = ['text', 'sentiment']
                    writer = csv.DictWriter(myFile, fieldnames=myFields)
                    writer.writeheader()

                    # parsing tweets one by one
                    for tweet in fetched_tweets:
                        # empty dictionary to store required params of a tweet
                        parsed_tweet = {}

                        # saving text of tweet
                        parsed_tweet['text'] = tweet.text
                        # saving sentiment of tweet
                        parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                        #tweet_csv.writerow([row[0], blob.sentiment.polarity, "negative"])

                        tweet_csv=tweet.text
                        sentiment_csv=self.get_tweet_sentiment(tweet.text)

                        '''for k in tweet_csv.split("\n"):
                                  tweet_csv_split=re.sub(r"[^a-zA-Z0-9]+", ' ', k)'''
                        writer.writerow({'text' :tweet_csv.encode('ascii', 'ignore').decode('ascii'), 'sentiment' :sentiment_csv.encode('ascii', 'ignore').decode('ascii')})

                        # appending parsed tweet to tweets list
                        if tweet.retweet_count > 0:
                            # if tweet has retweets, ensure that it is appended only once
                            if parsed_tweet not in tweets:
                                tweets.append(parsed_tweet)
                        else:
                            tweets.append(parsed_tweet)

                    myFile.close()
                    # return parsed tweets
                    return tweets

                except tweepy.TweepError as e:
                    # print error (if any)
                    print("Error : " + str(e))


def sentiment_analysis(sentences):
          # creating object of TwitterClient Class
          api = TwitterClient()

          #query from user
          #topic= raw_input('Enter topic for sentiment analysis: ')
          #fd = open("sentiment_topic.txt", "r")
          #topic=fd.read()
          #print (topic)
          #fd.close()

          #sentences=Application.reveal(self)
          print(sentences)

          # calling function to get tweets
          tweets = api.get_tweets(query=sentences , count = 30)

          # picking positive tweets from tweets
          ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
          # percentage of positive tweets

          #print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
          global p_tweet_percent
          p_tweet_percent  =100*len(ptweets)/len(tweets)

          # picking negative tweets from tweets
          ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

          # percentage of negative tweets
          # print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
          global n_tweet_percent
          n_tweet_percent =100*len(ntweets)/len(tweets)

          # percentage of neutral tweets
          neutral_tweet= len(tweets)- len(ntweets)- len(ptweets)
          #print("Neutral tweets percentage: {} % ".format(100*neutral_tweet/len(tweets)))
          global neutral_tweet_percent
          neutral_tweet_percent=100*neutral_tweet/len(tweets)

          fd = open("tweets.txt", "a")
          fd.truncate(0)
          # printing first 5 positive tweets
          #print("\n\nNegative tweets:")
          fd.write("\n Positive Tweets \n")
          for tweet in ptweets[:7]:
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                #fd.seek(fd.tell()+10)
                #print(fd.tell())
                fd.write("\n"+tweet['text'].translate(non_bmp_map).encode('ascii', 'ignore').decode('ascii')+"\n")

          # printing first 5 negative tweets
          #print("\n\nNegative tweets:")
          fd.write("\n \n Negative Tweets \n")
          for tweet in ntweets[:7]:
                non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
                #fd.seek(fd.tell() + 10)
                fd.write("\n"+tweet['text'].translate(non_bmp_map).encode('ascii', 'ignore').decode('ascii')+"\n")

          fd.close()

          #alltweets = csv.reader(open("search-data/uniqueSearchTweets.csv", 'rb'))
          '''def getStats(fileRead):

              results = csv.writer(open("sentiment_Tweet.csv", "wb"))
              tot = 0;
              pos = 0;
              neg = 0;
              neu = 0;
              for row in fileRead:
                  tot = tot + 1;
                  if row[4] == "positive":
                      pos = pos + 1;
                  elif row[4] == "negative":
                      neg = neg + 1;
                  elif row[4] == "neutral":
                      neu = neu + 1;

              print "total tweets: ", tot
              print "positive: ", pos
              print "negative: ", neg
              print "neutral: ", neu
              results.writerow([tot, pos, neg, neu])

              getStats("sentiment_Tweet.csv")'''

          return n_tweet_percent, p_tweet_percent, neutral_tweet_percent;
