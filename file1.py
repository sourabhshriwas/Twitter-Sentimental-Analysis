import tweepy
from textblob import TextBlob
from tkinter import *
import unicodedata
from unidecode import unidecode
import matplotlib.pyplot as plt


favorite = []
retweet = []
no_of_tweets = []
sizes = []


consumer_key ='krUc2GIlYa0oJSqWks3MAnXk3'
consumer_secret ='TsN0G52FjNB7CHDljvAiBLc6nRcwRHkdzCNAEg6Yp0v9Ed9BFa'
access_token = ''
access_token_secret = ''
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)



def deEmojify(inputString):
    returnString = ""
    for character in inputString:
        try:
            character.encode("ascii")
            returnString += character
        except UnicodeEncodeError:
            returnString += ''
    return returnString

def graph1():
    plt.clf()
    plt.plot(retweet)
    plt.ylabel('retweets')
    plt.xlabel('no of twwets')
    plt.show()


def graph():
    plt.clf()
    labels = 'Positive', 'Neutral', 'Negative'

    colors = ['blue', 'yellow', 'red']
    explode = (0.1, 0, 0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()

def analyse():
    a=val1.get()
    retweet.clear()
    sizes.clear()
    b=val2.get()
    if a is '':
        return None
    pt = 0
    n=0
    nt=0
    avg_pol=0
    avg_sub=0
    lb1.delete(0,END)
    lb2.delete(0, END)
    lb3.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    e5.delete(0, END)
    e6.delete(0, END)
    e7.delete(0, END)
    en1.delete(0,END)
    en2.delete(0,END)
    en3.delete(0,END)
    #public_tweets = api.search(a,count=b,limit=100)

    public_tweets = []
    last_id = -1
    while len(public_tweets) < int(b):
        count = int(b) - len(public_tweets)
        try:
            new_tweets = api.search(q=a, count=count, max_id=str(last_id - 1),text_mode='extended')
            if not new_tweets:
                break
            public_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            break

    lb1.delete(END)
    for tweet in public_tweets:
        a=deEmojify(tweet.text)
        #print(tweet.favorite_count)
        retweet.append(tweet.retweet_count)
        favorite.append(tweet.favorite_count)
        #print(tweet.retweet_count)
        analysis=TextBlob(a)
        #print(analysis.sentiment)
        avg_pol=avg_pol+analysis.sentiment.polarity

        avg_sub=avg_sub+analysis.sentiment.subjectivity
        if analysis.sentiment.polarity > 0:
            #print('positive')
            lb1.insert(END,a)
            pt = pt +1
        elif analysis.sentiment.polarity == 0:
            #print('neutral')
            lb3.insert(END, a)
            n=n+1
        else:
            #print('negative')
            lb2.insert(END,a)
            nt=nt+1

    sizes.append(pt)
    sizes.append(n)
    sizes.append(nt)
    total=nt+pt+n
    en1.insert(END,pt)
    en2.insert(END, nt)
    en3.insert(END, n)
    #print(pt)
    p_percent = ((pt/total)*100)

    e3.insert(END,str(p_percent)+"%")
    #print(n)
    neutral_percent = ((n /total) * 100)

    e5.insert(END,str(neutral_percent)+"%")
    #print(nt)
    n_percent = ((nt /total) * 100)
    e4.insert(END,str(n_percent)+"%")

    #print(avg_pol/total)
    e6.insert(END,(avg_pol/total))

    #print(avg_sub/total)
    e7.insert(END, (avg_sub / total))

    #print(retweet)
    #print(favorite)




window = Tk()


window.title("twitter sentimenty analyser")
window.configure(background="pale turquoise")

window.state('zoomed')


background_image=PhotoImage(file="3.png")
background_label = Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

l1 = Label(window,text = "TWITTER TWEET ANALYSER",fg = "black",bg="deep sky blue" ,font=("Arial Black	",42))
l1.place(x=350,y=20)
#l1.grid(row=0,column=1,columnspan=4)

l2 = Label(window,text = "Enter text to analysis:",fg = "black",bg="deep sky blue"   ,font=("Helvetica", 16))
#l2.grid(row=1,column=0)
l2.place(x=20,y=100)

val1 = StringVar()
e1=Entry(window,textvariable=val1)
#e1.grid(row=1,column=1)
e1.place(x=270,y=105)
e1.configure(width=30)

l3 = Label(window,text = "Enter no of tweets:",bg="deep sky blue",fg = "black",font=("Helvetica", 16))
#l3.grid(row=1,column=2)
l3.place(x=20,y=150)

val2 = StringVar()
e2=Entry(window,textvariable=val2)
#e2.grid(row=1,column=3)
e2.place(x=270,y=155)
e2.configure(width=30)

b1 = Button(window,text = "CLICK TO ANALYSE",command=analyse,bg="black",fg = "blue",font=("Helvetica bold", 18))
#b1.grid(row=3,column=4,columnspan=2)
b1.place(x=700,y=750)
b1.config(height=1,width=20)

b2 = Button(window,text = "CLICK For Retweets",command=graph1,bg="black",fg = "blue",font=("Helvetica", 18))
#b2.grid(row=5,column=4)
b2.place(x=1000,y=750)
b2.config(height=1,width=20)

b3 = Button(window,text = "CLICK for Graph",command=graph,bg="black",fg = "blue",font=("Helvetica",18))
#b3.grid(row=7,column=4)
b3.place(x=1300,y=750)
b3.config(height=1,width=20)

l4 = Label(window,text = "Positive tweets:",fg ="black",bg="deep sky blue" ,font=("Helvetica", 16))
#l4.grid(row=3,column=0,rowspan=2)
l4.place(x=20,y=250)

lb1=Listbox(window, height=10, width=60)
lb1.place(x=270,y=200)
#lb1.grid(row=3,column=1,rowspan=2)

l5 = Label(window,text = "Negative tweets:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
l5.place(x=20,y=450)
#l5.grid(row=5,column=0,rowspan=2)

lb2=Listbox(window, height=10, width=60)
lb2.place(x=270,y=400)
#lb2.grid(row=5,column=1,rowspan=2)

l6 = Label(window,text = "Neutral tweets:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
l6.place(x=20,y=650)
#l6.grid(row=7,column=0,rowspan=2)

lb3=Listbox(window, height=10, width=60)
lb3.place(x=270,y=600)
#lb3.grid(row=7,column=1,rowspan=2)

l7 = Label(window,text = "% of positive tweets:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
l7.place(x=1000,y=300)
#l7.grid(row=3,column=2)

e3=Entry(window)
e3.place(x=1250,y=305)
#e3.grid(row=3,column=3)
e3.configure(width=30)

a1 = Label(window,text = "no of positive tweets:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
a1.place(x=1000,y=350)
#a1.grid(row=4,column=2)

en1=Entry(window)
en1.place(x=1250,y=355)
#en1.grid(row=4,column=3)
en1.configure(width=30)


l8 = Label(window,text = "% of negative tweets:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
l8.place(x=1000,y=450)
#l8.grid(row=5,column=2)

e4=Entry(window)
e4.place(x=1250,y=455)
#e4.grid(row=5,column=3)
e4.configure(width=30)

a2 = Label(window,text = "no of negative tweets:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
a2.place(x=1000,y=500)
#a2.grid(row=6,column=2)

en2=Entry(window)
en2.place(x=1250,y=505)
#en2.grid(row=6,column=3)
en2.configure(width=30)


l9 = Label(window,text = "% of neutral tweets:",fg = "black",bg="deep sky blue",font=("Helvetica", 16))
l9.place(x=1000,y=600)
#l9.grid(row=7,column=2)

e5=Entry(window)
e5.place(x=1250,y=605)
#e5.grid(row=7,column=3)
e5.configure(width=30)

a3 = Label(window,text = "no of neutral tweets:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
a3.place(x=1000,y=650)
#a3.grid(row=8,column=2)

en3=Entry(window)
en3.place(x=1250,y=655)
#en3.grid(row=8,column=3)
en3.configure(width=30)


l10 = Label(window,text = "Average Polarity:",fg = "black",bg="deep sky blue" ,font=("Helvetica", 16))
l10.place(x=1000,y=150)
#l10.grid(row=9,column=0)

e6=Entry(window)
#e6.grid(row=9,column=1)
e6.place(x=1250,y=155)
e6.configure(width=30)


l11= Label(window,text = "Average Subjectivity:",fg ="black",bg="deep sky blue" ,font=("Helvetica", 16))
l11.place(x=1000,y=200)
#l11.grid(row=9,column=2)

e7=Entry(window)
#e7.grid(row=9,column=3)
e7.place(x=1250,y=205)
e7.configure(width=30)


window.mainloop()