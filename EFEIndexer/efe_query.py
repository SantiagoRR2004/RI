import os
from typing import List
from whoosh import index
from whoosh.index import FileIndex
from whoosh.searching import Searcher
from whoosh.qparser import MultifieldParser
from whoosh.query import And, Or, Term, DateRange
from datetime import datetime


LIMIT = 5


def search(
    ix: FileIndex,
    query_text: str,
    fields: List[str],
    categories: List[str] | None = None,
    keyword: str | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    with ix.searcher() as searcher:
        parser = MultifieldParser(fields, schema=ix.schema)
        query = parser.parse(query_text)

        filters = []
        if categories:
            filters.append(Or([Term("category", category) for category in categories]))
        if keyword:
            filters.append(Term("keywords", keyword))
        if date_from or date_to:
            filters.append(DateRange("datetime", date_from, date_to))

        if filters:
            query = And([query] + filters)

        results = searcher.search(query, limit=None)
        total = len(results)

        print(f"\nTotal results: {total}\n")

        for i, result in enumerate(results[:LIMIT], 1):
            print(f"[{i}] {result['title']}")
            print(f"    Document: {result['documentNumber']}")
            print(f"    Date: {result['datetime']}")
            print(f"    Category: {result.get('category', 'N/A')}")
            print(f"    Text: {result['text'][:200]}...")
            print()


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    index_path = os.path.join(current_dir, "indexdir")

    if not os.path.exists(index_path):
        print(f"Index not found at {index_path}")
        return

    ix = index.open_dir(index_path)

    print("EFE Query System")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. Search")
        print("2. Show top terms")
        print("3. Exit")

        choice = input("\nSelect option: ").strip()

        if choice == "1":
            query_text = input("Enter query: ").strip()
            if not query_text:
                print("Query cannot be empty")
                continue

            fields_input = input(
                "Fields to search (title,text) [default: title,text]: "
            ).strip()
            if fields_input:
                fields = [f.strip() for f in fields_input.split(",")]
            else:
                fields = ["title", "text"]

            categories_input = input("Filter by category (optional): ").strip()
            if categories_input:
                categories = [c.strip() for c in categories_input.split(",")]
            else:
                categories = None

            keyword = input("Filter by keyword (optional): ").strip() or None

            date_from_str = input("Date from YYYYMMDD (optional): ").strip()
            date_to_str = input("Date to YYYYMMDD (optional): ").strip()

            date_from = None
            date_to = None

            if date_from_str:
                try:
                    date_from = datetime.strptime(date_from_str, "%Y%m%d")
                except ValueError:
                    print("Invalid date format")
                    continue

            if date_to_str:
                try:
                    date_to = datetime.strptime(date_to_str, "%Y%m%d")
                except ValueError:
                    print("Invalid date format")
                    continue

            search(ix, query_text, fields, categories, keyword, date_from, date_to)

        elif choice == "2":
            field = input("Field name (category/keywords/title/text): ").strip()
            if not field:
                print("Field cannot be empty")
                continue

            limit_input = input("Number of top terms [default: 10]: ").strip()
            limit = int(limit_input) if limit_input else 10

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
