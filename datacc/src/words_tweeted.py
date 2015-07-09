if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: python %s <input_file_name> <output_file_name>" % sys.argv[0], file=sys.stderr)
        exit(-1)

    inputFile = sys.argv[1]
    assert os.path.isfile(inputFile), "invalid file: \"%s\"" % inputFile

    outputFile = sys.argv[2]

    print(inputFile)
    print(outputFile)
