#!/usr/bin/env bash

# the run script for running the word count and unique median features.

<full_path_to_spark_root_dir>/bin/spark-submit ./src/words_tweeted.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
<full_oath_to_spark_root_dir>/bin/spark-submit ./src/median_unique.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt

# Example:
#/Users/nhonaitran/Projects/spark-1.4.0-bin-hadoop2.6/bin/spark-submit ./src/words_tweeted.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
#/Users/nhonaitran/Projects/spark-1.4.0-bin-hadoop2.6/bin/spark-submit ./src/median_unique.py ./tweet_input/tweets.txt ./tweet_output/ft2.txt
