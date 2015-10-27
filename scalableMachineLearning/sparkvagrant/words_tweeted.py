
# coding: utf-8

# In[60]:

import os.path
infile = os.path.join("tweet_input","tweets.txt")
outfile = os.path.join("tweet_output", "ft1.txt")
print(infile)
print(outfile)


# In[61]:

def createKeyValuePair(word):
    """Create a key/value pair"""
    return (word, 1)

def formatter(x):
    return(x[0]+' '+str(x[1]))

def countWords(filename):
    """Read in the specified file and count the total number of times each word appeared in the file."""
    wordCounts = (sc
                  .textFile(filename)
                  .flatMap(lambda x: x.split(" "))
                  .map(createKeyValuePair)
                  .reduceByKey(lambda x,y: x+y))
    return(wordCounts)

def formatted(data):
    """Sort RDD and change each element to specific format."""
    formatted = data.sortByKey(True, 3, lambda x: x.lower()).map(formatter)
    return(formatted)

def save(filename, wordsCount):
    """Write to file the words and number of occurences for each word on a line."""
    formatted(wordsCount).saveAsTextFile(filename)


# In[64]:

#print(save(outfile1, countWords(infile)).collect())
save(outfile, countWords(infile))


# In[62]:

print(countWords(infile).collect())


# In[63]:

formatted(countWords(infile)).collect()


# In[65]:

countWords(infile).sortByKey(True, 3, lambda x: x.lower()).collect()


# In[ ]:
