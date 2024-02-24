# Inverted_index
The purpose of information retrieval is finding material of an unstructured nature that satisfies an information need from within large collections. An example of an information retrieval task is the search for relevant Wikipedia articles by a given query. In the simplest case, we want to find articles that contain all words from the query. To do this, we can iterate through all documents one by one and check that all words from the query are present in the document. However, Wikipedia currently has over 51 million articles, so direct search is too expensive.  

Modern search engines use special data structures for fast search, such as inverted index. An inverted index is a data structure that for each word indicates a set of articles containing that word. To find a set of suitable articles for a query, we need to intersect sets of articles for all words in the query.  

In this project, the InvertedIndex class was implemented as a command line interface (CLI).
# About CLI:
Program are able to handle 2 types of commands: build and query.  

The build command takes a Wikipedia dump as input, constructs an inverted index and saves it to disk. The build subparser have 2 parameters --dataset (path to dataset to build Inverted Index) and --index (path for Inverted Index dump).  

The query command must find common articles for words in each query from the query file. The query subparser have 2 parameters --index (path to load Inverted Index) and --query_file (query_file with collection of queries to run against
Inverted Index). In query_file, each row is a separate query. For each query, output the article id's in stdout in ascending order, separated by a single comma.
