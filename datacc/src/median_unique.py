if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python %s <input_file_name> <output_file_name>" % sys.argv[0], file=sys.stderr)
        exit(-1)

    cnt = len(sys.argv)
    inputFile = sys.argv[1]
    if cnt < 3:
        outputFile = os.path.join("..", "tweet_output", "ft2.txt")
    else:
        outputFile = sys.argv[2]

    assert os.path.isfile(inputFile), "invalid file: \"%s\"" % inputFile
