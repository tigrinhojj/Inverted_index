import json
import argparse


class InvertedIndex:
    """
        A class for creating and handling an inverted index.

        Attributes:
            _inverted_index_dict (dict): A dictionary where the key is a word and the value is a set of article IDs.
    """

    def __init__(self, inverted_index_dict):
        """
            Initializes the inverted index.

            Parameters:
                inverted_index_dict (dict): A dictionary to initialize the index with.
        """

        self._inverted_index_dict = inverted_index_dict

    def query(self, words):
        """
            Returns a set of articles IDs that contain all the words in the query.

            Parameters:
                words (str): A query string.

            Returns:
                set: A set of document IDs.
        """

        words_set = set(words.split())
        id_list = []
        for word in words_set:
            if word in self._inverted_index_dict:
                id_list.append(self._inverted_index_dict[word])
            else:
                id_list.append(set())
        if id_list:
            common_set = id_list[0].intersection(*id_list[1:])
            return common_set
        else:
            return set()

    def dump(self, filepath):
        """
            Serializes and saves the inverted index to a file.

            Parameters:
                filepath (str): Path to the file to save the index.
        """

        dict_to_dump = {}
        for word, id_set in self._inverted_index_dict.items():
            dict_to_dump[word] = list(id_set)
        with open(filepath, 'w') as file:
            json.dump(dict_to_dump, file)

    @classmethod
    def load(cls, filepath):
        """
            Loads and deserializes an inverted index from a file.

            Parameters:
                filepath (str): Path to the file containing the index.

            Returns:
                InvertedIndex: An instance of the InvertedIndex class.
        """

        with open(filepath, 'r') as file:
            dict_to_load = json.load(file)
        for word, id_list in dict_to_load.items():
            dict_to_load[word] = set(id_list)

        return InvertedIndex(dict_to_load)


def load_document(filepath):
    """
        Loads documents from a file and returns them as a dictionary.

        Parameters:
            filepath (str): Path to the file with articles.

        Returns:
            dict: A dictionary where the key is the article ID and the value is its content.
    """

    article_dict = {}
    with open(filepath, 'r', encoding='utf8') as f:
        for line in f:
            try:
                article_id, article_content = line.split('\t', 1)
                article_dict[int(article_id)] = article_content.strip()
            except Exception as e:
                raise Exception('Check your input, the format of the string is as follows: '
                                '{article_id(int) <tab> article_name <spaces> article_content}.') from e

    return article_dict


def build_inverted_index(articles):
    """
        Creates an inverted index for a set of documents.

        Parameters:
            articles (dict): A dictionary of documents where the key is a document ID and the value is its content.

        Returns:
            InvertedIndex: An instance of the InvertedIndex class.
    """

    inverted_index_dict = {}
    for article_id, article_content in articles.items():
        article_content_set = set(article_content.split())
        for word in article_content_set:
            inverted_index_dict.setdefault(word, set()).add(article_id)

    return InvertedIndex(inverted_index_dict)


def build(args):
    """
        Processes command line arguments to build an inverted index.

        Parameters:
            args (argparse.Namespace): Command line arguments.
    """

    articles = load_document(args.dataset)
    inverted_index = build_inverted_index(articles)
    inverted_index.dump(args.index)


def query(args):
    """
        Processes command line arguments to perform queries on the inverted index.

        Parameters:
            args (argparse.Namespace): Command line arguments.
    """

    inverted_index = InvertedIndex.load(args.index)
    with open(args.query_file, 'r') as file:
        for line in file:
            query_words = line.strip()
            result = inverted_index.query(query_words)
            print(','.join(map(str, sorted(result))))


def main():
    """
        Main function setting up the command line argument parser and executing the corresponding commands.
    """

    parser = argparse.ArgumentParser(description="inverted index for articles", )
    subparsers = parser.add_subparsers(dest="command")

    build_parser = subparsers.add_parser('build', help='constructs an inverted index and saves it to disk')
    build_parser.add_argument('--dataset', required=True, help='path to dataset to build Inverted Index')
    build_parser.add_argument('--index', required=True, help='path for Inverted Index dump')
    build_parser.set_defaults(func=build)

    query_parser = subparsers.add_parser('query',
                                         help='find common articles for words in each query from the query file')
    query_parser.add_argument('--index', required=True, help='path to load Inverted Index')
    query_parser.add_argument('--query_file', required=True,
                              help='path to query_file with collection of queries to run against Inverted Index')
    query_parser.set_defaults(func=query)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    else:
        args.func(args)


main()
