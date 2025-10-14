from parser_efe_corpus import parse_efe_corpus
import argparse
import shutil
import sys
import os


def create(dirpath: str, indexpath: str):
    # If it exists, remove index
    if os.path.exists(indexpath):
        print(f"Removing index at {indexpath}")
        shutil.rmtree(indexpath)
    else:
        print(f"Creating index at {indexpath} with documents from {dirpath}")
        collection = parse_efe_corpus(dirpath)
        collection.createIndex(indexpath)


if __name__ == "__main__":

    # python efe_indexing.py --create --path <path_output> --documents <SGML_files>
    # python efe_indexing.py --add --path <index_path> --documents <SGML_files>
    # python efe_indexing.py --stats --path <index_path>

    currentDirectory = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create", action="store_true", help="Create a new index")
    group.add_argument(
        "--add", action="store_true", help="Add documents to an existing index"
    )
    group.add_argument("--stats", action="store_true", help="Show index statistics")

    parser.add_argument(
        "--path",
        type=str,
        required=False,
        help="Path to the index directory (output or existing)",
        default=os.path.join(currentDirectory, "indexdir"),
    )
    parser.add_argument(
        "--documents",
        type=str,
        required=False,
        help="Directory containing SGML files",
        default=os.path.join(currentDirectory, "efe"),
    )

    if len(sys.argv) == 1:
        # Default is --create if no subcommand is provided
        sys.argv.insert(1, "--create")

    args = parser.parse_args()

    if args.create:
        create(args.documents, args.path)

    elif args.add:
        print(f"Adding documents {args.documents} to index at {args.path}")

    elif args.stats:
        print(f"Showing statistics for index at {args.path}")
