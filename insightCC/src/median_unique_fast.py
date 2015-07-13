import bisect
import sys
from pyspark import SparkContext, SparkConf
from functools import partial

def nonBlankLine(line):
    return(len(line) > 0)

def trailingSpaceRemover(line):
    return(line.strip())

def keyValuePairMapper(pair):
    return (pair[1], len(set(pair[0].split(" "))))

def rollingMedians(tweetLookup, element):
    """Compute median for all tweets up to specified element's line number.
    Args:
        tweetLookup (broadcast of key/value pairs): the lookup broadcast object used for retrieving tweets up to the specified line number.
        element (int, int): key/value pair containing the line number and words count of a tweet.
    Returns:
        key/value pair (int, int): the line number and computed median for all tweets up to this element.
    """
    if element[0] == 0:
        return element

    linenum = element[0]
    wordCount = element[1]
    tweets = tweetLookup.value[0:linenum]
    counts = [x[1] for x in tweets]
    position = bisect.bisect(counts, wordCount)
    bisect.insort(counts, wordCount)
    m = len(counts)
    if m % 2 == 0:
        j = m // 2
        median = (counts[j-1] + counts[j]) / 2.0
    else:
        j = (m + 1) // 2
        median = counts[j-1]

    return((element[0], median))

def main(sc, *args):
    print("Computing tweets median:")
    try:
        inputFile = args[0]
        outputFile = args[1]

        # read file and create a base RDD
        lines = sc \
                  .textFile(inputFile) \
                  .map(trailingSpaceRemover) \
                  .filter(nonBlankLine)

        # transform base RDD consisting of pairs of line number and words count for each tweet
        wordsCount = lines \
                    .zipWithIndex() \
                    .map(keyValuePairMapper)

        # broadcast the lookup dictionary to the cluster
        tweetLookup = sc.broadcast(wordsCount.collect())

        # compute rolling medians as each line is processed and save computed values to file
        wordsCount \
            .map(partial(rollingMedians, tweetLookup)) \
            .sortByKey() \
            .map(lambda x: x[1]) \
            .saveAsTextFile(outputFile)

        print("Completed successfully!")

    except (Exception) as e:
        print(e)
        print("Stopped.")

    sc.stop()

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python %s <input_file_name> <output_file_name>" % sys.argv[0], file=sys.stderr)
        exit(-1)

    conf = SparkConf().setAppName("MedianUnique")
    sc = SparkContext(conf=conf)
    main(sc, *sys.argv[1:])
