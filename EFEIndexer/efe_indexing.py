import argparse
from parser_efe_corpus import parse_efe_corpus

# python efe_indexing.py --create --path <path_ouput> --documents <SGML_files>
# python efe_indexing.py --add --path <index_path> --documents <SGML_files>
# python efe_indexing.py --stats --path <index_path>

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    create_parser = subparsers.add_parser("--create", help="Create a new index")
    create_parser.add_argument(
        "--path", type=str, required=True, help="Path to the output index"
    )
    create_parser.add_argument(
        "--documents", type=str, required=False, help="Dir name of SGML files"
    )

    add_parser = subparsers.add_parser(
        "--add", help="Add documents to an existing index"
    )
    add_parser.add_argument(
        "--path", type=str, required=True, help="Path to the existing index"
    )
    add_parser.add_argument(
        "--documents", type=str, required=False, help="Dir name of SGML files"
    )

    stats_parser = subparsers.add_parser("--stats", help="Show index statistics")
    stats_parser.add_argument(
        "--path", type=str, required=True, help="Path to the existing index"
    )

    args = parser.parse_args()

    if args.command == "create":
        print(f"Creating index at {args.path} with documents {args.documents}")
        if args.documents:
            parse_efe_corpus(args.documents)
        else:
            parse_efe_corpus()

    elif args.command == "add":
        print(f"Adding documents {args.documents} to index at {args.path}")

    elif args.command == "stats":
        print(f"Showing statistics for index at {args.path}")
