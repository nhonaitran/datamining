from operator import add
from pyspark import SparkContext, SparkConf
import sys

def keyValuePairMapper(word):
    """Transform word to a key/value pair."""
    return (word, 1)

def formatter(x):
    '''Transform key/value pair to a string.'''
    return(x[0]+' '+str(x[1]))

def main(sc, *args):
    print("Computing number of times words tweeted:")
    try:
        inputFile = args[0]
        outputFile = args[1]

        # Read content of entire input file and returns a list of individual words
        lines = sc \
                .textFile(inputFile) \
                .flatMap(lambda x: x.strip().split(" "))

        # Perform words count
        wordsCount = lines \
                    .map(keyValuePairMapper) \
                    .reduceByKey(add)

        # Sort results, map results to specific format
        formatted = wordsCount \
                    .sortByKey() \
                    .map(formatter)

        # Save formatted results to file
        formatted.saveAsTextFile(outputFile)

        print("Completed successfully!")

    except (Exception) as e:
        print(e)
        print("Stopped.")

    sc.stop()

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python %s <input_file_name> <output_file_name>" % sys.argv[0])
        exit(-1)

    # Initialize the spark context
    conf = SparkConf().setAppName("WordsTweeted")
    sc = SparkContext(conf=conf)
    main(sc, *sys.argv[1:])
