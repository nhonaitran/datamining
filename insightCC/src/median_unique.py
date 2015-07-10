import bisect
import sys
from pyspark import SparkContext, SparkConf

def nonBlankLine(line):
    return(len(line) > 0)

def trailingSpaceRemover(line):
    return(line.strip())

def keyValuePairMapper(pair):
    return (pair[1], len(set(pair[0].split(" "))))

def computeMedians(data):
    # since we are processing the file sequentially, this implementation inserts the new counts into a list while maintaining the list in sorted order.
    # This allows fast calculation of the median by looking up either the middle element for odd number of lines or average of the middle two elements for even number of lines being processed.
    #'TODO: Need to push the medians list to worker thread though.... driver will get filled up otherwise.
    n = data.count()
    value = data.first()[1]
    v = [value]
    medians = [value]
    for i in range(1, n):
        # get the word count of the current line.
        value = data.filter(lambda x: x[0] == i).map(lambda x: x[1]).collect()[0]

        # determine the index where the new count value is inserted
        position = bisect.bisect(v, value)

        # insert into list at the specified position, allowing the list still be sorted.
        bisect.insort(v, value)

        # compute median dependent on whether the length of the list is even or odd number.
        m = i+1
        if m % 2 == 0:
            j = m // 2
            median = (v[j-1] + v[j]) / 2.0
        else:
            j = (m + 1) // 2
            median = v[j-1]

        medians.append(median)

    return(sc.parallelize(medians))

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

        # compute running median as each line is processed
        runningMedians = computeMedians(wordsCount)

        # save computed values to file
        runningMedians.saveAsTextFile(outputFile)

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
