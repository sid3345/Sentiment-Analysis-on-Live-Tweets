# coding: utf-8

#import sentiment_analysis_python
import matplotlib.pyplot as plt
from sentiment_analysis_python import sentiment_analysis
from tkinter import *

class Application(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.instruction = Label(self,text ="Find the Sentiment % of the word")

        self.instruction.grid(row=0, column=0, columnspan = 2, sticky= W)

        self.sentence = Label(self, text = "Enter a topic for analysis: ")

        self.sentence.grid(row=1, column=0, sticky=W)

        self.entry = Entry(self)

        self.entry.grid(row = 1, column=1,sticky=W)

        self.submit_button= Button(self,text="Submit", command=self.reveal)

        self.submit_button.grid(row=2, column=0, sticky = W)

        self.text = Text(self,width=75,height = 25, wrap = WORD)

        self.text.grid(row=3, column = 0, columnspan = 2, sticky = W)
        #self.clear_button = Button(self, text = "Clear Text", command =self.clear_text)
        #self.clear_button.grid(row=2, column=1, sticky=W)

    def reveal(self):

        self.text = Text(self,width=75,height = 35, wrap = WORD)

        self.text.grid(row=3, column = 0, columnspan = 2, sticky = W)

        #fd = open("sentiment_topic.txt", "w")
        sentences = self.entry.get()

        #fd.write(sentences)
        #fd.close()
        '''self.text.insert(0.0, tweets +"\n ")'''
        p_tweet_percent, n_tweet_percent, neutral_tweet_percent= sentiment_analysis(sentences)

        # percentage of positive tweets
        self.text.insert(0.0,"Positive tweets percentage: {} %".format(p_tweet_percent)+"\n")

        # percentage of negative tweets
        self.text.insert(0.0,"Negative tweets percentage: {} %".format(n_tweet_percent)+"\n")

        self.text.insert(0.0,"Neutral tweets percentage: {} % ".format(neutral_tweet_percent)+"\n")

        fd=open("tweets.txt","r")
        tweets_stored=fd.read()
        self.text.insert(0.0, "\nTweets: "+tweets_stored+"\n")
        #self.text.insert(0.0,fd.read)
        #fd.truncate(0)
        fd.close()

        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#8c564b"]
        # explode = (0, 0, 0, 0, 0)
        print(p_tweet_percent, n_tweet_percent, neutral_tweet_percent)
        plt.pie([p_tweet_percent, n_tweet_percent, neutral_tweet_percent], labels=["positive", "negative", "neutral"], colors=colors,
                autopct='%1.1f%%', shadow=True)
        plt.title("Sentiment Analysis of {} on Twitter\n".format(sentences))
        plt.show()
        #plt.lift()
        #plt.attributes('-topmost', True)
        #plt.after_idle(root.attributes, '-topmost', False)

        '''x = []
        y = []
        with open('sentiment_tweet.csv', 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')
            for row in plots:
                x.append(int(row[0]))
                y.append(int(row[1]))'''

        '''plt.plot(x, y, label='Loaded from file!')
        x=(len(ptweets)+1)
        y=(len(ntweets)+1)
        print x,y
        plt.xlabel('+ve tweets')
        plt.ylabel('-ve tweets')
        plt.title('Interesting Graph\nCheck it out')
        plt.legend()
        plt.show()'''

        '''# declare the variables for the pie chart, using the Counter variables for "sizes"
        colors = ['green', 'red', 'grey']
        sizes = [positive, negative, neutral]
        labels = 'Positive', 'Negative', 'Neutral'
        ## use matplotlib to plot the chart
        plt.pie(
            x=sizes,
            shadow=True,
            colors=colors,
            labels=labels,
            startangle=90)

        plt.title("Sentiment of {} Tweets about {}".format(number, sentences))
        plt.show()'''

root = Tk()

root.minsize(300,300)
root.geometry("800x800")
root.title("Sentiment Analysis in Twitter")

app = Application(root)
root.mainloop()