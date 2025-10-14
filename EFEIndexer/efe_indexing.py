from parser_efe_corpus import parse_efe_corpus
import argparse
import sys
import os

# python efe_indexing.py --create --path <path_ouput> --documents <SGML_files>
# python efe_indexing.py --add --path <index_path> --documents <SGML_files>
# python efe_indexing.py --stats --path <index_path>

if __name__ == "__main__":
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
        print(f"Creating index at {args.path} with documents {args.documents}")
        if args.documents:
            parse_efe_corpus(args.documents)
        else:
            parse_efe_corpus()

    elif args.add:
        print(f"Adding documents {args.documents} to index at {args.path}")

    elif args.stats:
        print(f"Showing statistics for index at {args.path}")
