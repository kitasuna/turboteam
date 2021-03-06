from text_functions import *
from sys import argv
from datetime import datetime
from linelog import LineLog
import argparse

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import load_iris

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file', required=True, help='File to parse')
    parser.add_argument('-d', '--density', required=False, help='Check the density of a certain word')
    parser.add_argument('-sd', '--start-date', required=False, help='Date to start parsing from. Inclusive.')
    parser.add_argument('-ed', '--end-date', required=False, help='Date to end parsing from. Inclusive.')
    parser.add_argument('--interactive', required=False, action='store_true', help='Run in interactive mode')
    opts = parser.parse_args()
    # stole this from a tutorial
    # leaving it in in case it comes in handy
    #if not (opts.plot_file or opts.csv_file):
    #    parser.error("You have to specify either a --csv-file or --plot-file!")
    #return opts
    return opts

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()

def main():
    daily_tally = 0
    unused_lines = 0
    current_date = False
    daily_lines = {}
    user_lines = {}
    word_count = {}
    chat_lines = {} # List of chat text blocks for topic extraction

    n_features = 1000
    n_samples = 2000
    n_topics = 10
    n_top_words = 10

    # gets our command line args
    opts = parse_args()

    # set up our log file object
    logfile = LineLog(opts.input_file)

    # make sure our dates (if we have them) parse correctly
    if(opts.end_date):
        try:
            end_date = datetime.strptime(opts.end_date, "%Y/%m/%d")
            logfile.set_end_date(end_date)
        except ValueError:
            end_date = None


    # make sure our dates (if we have them) parse correctly
    if(opts.start_date):
        try:
            start_date = datetime.strptime(opts.start_date, "%Y/%m/%d")
            logfile.advance_to(start_date)
        except ValueError:
            start_date = None

    while logfile.current_line < logfile.num_lines:

        l = logfile.get_next_line()
        
        if logfile.current_date != current_date:
            daily_lines[logfile.current_date.strftime('%Y/%m/%d')] = 0
            current_date = logfile.current_date

        if type(l).__name__ == 'Chatline':
            daily_lines[logfile.current_date.strftime('%Y/%m/%d')] += 1

            # Find who wrote this one, if anyone
            user_name = l.user

            #Word count is a dictionary that counts words for each person
            word_count.setdefault(user_name,{})
            line_word_count(l.text, l.user, word_count)
            if(logfile.current_date.strftime('%Y/%m/%d') in chat_lines):
                chat_lines[logfile.current_date.strftime('%Y/%m/%d')] += ' ' + l.text
            else:
                chat_lines[logfile.current_date.strftime('%Y/%m/%d')] = l.text;

            if user_name in user_lines:
                user_lines[user_name] += 1
            else:
                user_lines[user_name] = 1
        elif type(l).__name__ == 'Badline':
            #print('No match for "', l.text, '"');
            unused_lines += 1

        
    #print('Line count is ' + str(file_len(opts.input_file)))
    #print('sum of daily line count is', str(sum(daily_lines.values())))
    #print('sum of dude line count is', str(sum(dude_lines.values())))
    #print('unused line count is', unused_lines)
    #print(daily_lines)
    #print(dude_lines)
    
    # Topic extraction
    # Use tf-idf features for NMF.
    tfidf_vectorizer = TfidfVectorizer(max_df=0.4, min_df=0.01, stop_words='english')
    # tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(chat_lines.values())

    # Use tf (raw term count) features for LDA.
    tf_vectorizer = CountVectorizer(max_df=0.4, min_df=0.1,
                                    stop_words='english')
    tf = tf_vectorizer.fit_transform(chat_lines.values())

    # Fit the NMF model
    nmf = NMF(n_components=n_topics, random_state=1, alpha=0, l1_ratio=0).fit(tfidf)

    print("\nTopics in NMF model:")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    print_top_words(nmf, tfidf_feature_names, n_top_words)

    print("Fitting LDA models with tf features, n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=5,
                                    learning_method='online', learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)

    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)

    # Find word density
    if(opts.density):
        for user in word_count:
            print(user + "'s " + opts.density + " density is: " + str(word_density(opts.density,user,word_count)))


    if(opts.interactive):
        while input('Stay ') != 'no':
            he_says_what_how_much(input('Who? '),input('What? (lowercase) '),word_count)

main()

