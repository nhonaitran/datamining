import numpy as np

def nonempty(line):
    return(len(line)>0)

def load(filename):
    """Reads in content of the specified file, and maps each line to (line number, words count appeared in the line) pair."""
    wordCounts = sc \
                  .textFile(filename) \
                  .filter(nonempty) \
                  .zipWithIndex() \
                  .map(lambda x: (x[1], len(set(x[0].strip().split(" ")))))
    return(wordCounts)

# def save(filename, data):
#     sc \
#     .parallelize(data) \
#     .saveAsTextFile(filename)

def save(filename, val):
    with open(filename, "a") as f:
        f.write(str(val)+"\n")

def updateTweetsMedian(infile, outfile):
    wordsPerLine = load(infile)
    n = wordsPerLine.count()
    [save(outfile, \
        np.median( \
        wordsPerLine \
        .filter(lambda x: x[0] <= i)
        .sortByKey() \
        .values() \
        .collect() \
    )) for i in range(n)]


# def loadTweetByLine(fileName):
#     with open(fileName) as f:
#         content =  f.read().splitlines()
#     data = [len(set(line.split())) for line in content]
#     return(data)
#
#
# def updateTweetsMedian(infile, outfile):
#     try:
#         wordsPerLine = loadTweetByLine(infile)
#         n = len(wordsPerLine)
#         [save(outfile, np.median(wordsPerLine[0:i])) for i in range(1,n+1)]
#     except (OSError, IOError) as e:
#         print(e)
#         raise

if __name__ == '__main__':
    import sys
    import os.path
    from pyspark import SparkContext, SparkConf

    if len(sys.argv) < 3:
        print("Usage: python %s <input_file_name> <output_file_name>" % sys.argv[0], file=sys.stderr)
        exit(-1)

    inputFile = sys.argv[1]
    outputFile = sys.argv[2]

    sc = SparkContext(appName="PythonMedian", conf=SparkConf().set("spark.driver.host", "localhost"))

    print("Computing tweets median:")
    try:
        updateTweetsMedian(inputFile, outputFile)
        print("Completed successfully!")
    except:
        print("Stopped.")

    sc.stop()
