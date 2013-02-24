# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, subject, summary,link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid
    
    def get_title(self):
        return self.title
    
    def get_subject(self):
        return self.subject
    
    def get_summary(self):
        return self.summary
    
    def get_link(self):
        return self.link
    

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

# TODO: WordTrigger

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        word = self.word.lower()
        text = text.lower()

        # Remove punctation and split the text
        for punc in string.punctuation:
            text = text.replace(punc, " ")
        splittext = text.split(" ")

        # Check if the word is in the text
        return word in splittext

# TODO: TitleTrigger

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        return self.is_word_in(story.get_title())

# TODO: SubjectTrigger
class SubjectTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())
# TODO: SummaryTrigger
class SummaryTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, T,):
        self.trigger = T
    def evaluate(self, x):
        return not self.trigger.evaluate(x)
    
    
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, T1, T2):
        self.trigger1 = T1
        self.trigger2 = T2
    def evaluate(self, x):
        return self.trigger1.evaluate(x) and self.trigger2.evaluate(x)
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, T1, T2):
        self.trigger1 = T1
        self.trigger2 = T2
    def evaluate(self, x):
        return self.trigger1.evaluate(x) or self.trigger2.evaluate(x)

# Phrase Trigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    def evaluate(self, x):
        return self.phrase in x.get_title() or self.phrase in x.get_summary() or self.phrase in x.get_subject()

    
# Question 9

# TODO: PhraseTrigger


#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    storylist= list()
    for trigger in triggerlist:
        for story in stories:
            if trigger.evaluate(story):
                storylist.append(story)

    return storylist

#======================
# Part 4
# User-Specified Triggers
#======================

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)
    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    tdict = {}
    triggerset = list()
    for line in lines:
        s = line.split()
        if s[0] == 'ADD':
            for word in s:
                if word == 'ADD':
                    continue
                else:
                    #print 'adding in dict'
                    triggerset.append(tdict[str(word)])
                    
        else:
            name = s[0]
            if s[1] == 'SUBJECT':
                t = SubjectTrigger(s[2])
            elif s[1] == 'TITLE':
                t = TitleTrigger(s[2])
            elif s[1] == 'SUMMARY':
                t = SummaryTrigger(s[2])
            elif s[1] == 'AND':
                t = AndTrigger(tdict[s[2]], tdict[s[3]])
            elif s[1] == 'OR':
                t = OrTrigger(tdict[s[2]], tdict[s[3]])
            elif s[1] == 'PHRASE':
                phrase = line[len(name)+8:-1]
                t = PhraseTrigger(phrase)
            tdict[name]= t
    return triggerset
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

