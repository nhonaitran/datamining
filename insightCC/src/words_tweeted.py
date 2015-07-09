import os.path
from fileinput import input
from glob import glob

def keyValuePairMapper(word):
    """Creates a key/value pair"""
    return (word, 1)

def formatter(x):
    return(x[0]+' '+str(x[1]))

def load(filename):
    """Reads in entire content of the specified file and creates a RDD of words."""
    wordCounts = (sc
                  .textFile(filename)
                  .flatMap(lambda x: x.strip().split(" ")))
    return(wordCounts)

def countWords(data):
    """Map each word to (word, count) pair before counting the total number of times each word appeared."""
    wordCounts = data \
                    .map(keyValuePairMapper) \
                    .reduceByKey(lambda x,y: x+y)
    return(wordCounts)

def save(filename, wordsCount):
    """Perform mapping of the (word, count) pairs to specific format before writing results to file."""
    wordsCount \
    .sortByKey() \
    .map(formatter) \
    .saveAsTextFile(filename)

def displayUsage():
    print("Usage: python %s <input_file_name> <output_file_name>" % sys.argv[0])

if __name__ == '__main__':
    import sys
    from fileinput import input
    from glob import glob
    from pyspark import SparkContext, SparkConf

    if len(sys.argv) < 3:
        displayUsage()
        sys.exit(1)

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    # Initialize the spark context
    sc = SparkContext(appName="PythonWordsTweeted", conf=SparkConf().set("spark.driver.host", "localhost"))

    print("Computing number of times words tweeted:")
    try:
        # Read content of entire input file and returns a list of individual words
        data = load(inputFile)
        # Count number of times each word appeared in list, and save result to file
        save(outputFile, countWords(data))
        print("Completed successfully.")
    except (Exception) as e:
        print(e)
        print("Stopped.")

    # Shut down spark context
    sc.stop()
