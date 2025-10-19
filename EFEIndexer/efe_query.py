import os
from typing import List
from whoosh import index
from whoosh.index import FileIndex
from whoosh.searching import Searcher
from whoosh.qparser import MultifieldParser
from whoosh.query import And, Or, Term, DateRange, Phrase
from datetime import datetime
from whoosh import analysis


LIMIT = 5
"""
schema = fields.Schema(
        documentNumber=fields.ID(stored=True, unique=True),
        datetime=fields.DATETIME(stored=True),
        category=fields.KEYWORD(stored=True, analyzer=text_analyzer),  # Compulsory
        title=fields.TEXT(stored=True, analyzer=text_analyzer),  # Compulsory
        subtitle=fields.TEXT(stored=True, analyzer=text_analyzer),  # The same as title
        text=fields.TEXT(stored=True, analyzer=text_analyzer),  # Main content
        author=fields.TEXT(stored=True, analyzer=text_analyzer), 
        location=fields.TEXT(stored=True),
        keywords=fields.KEYWORD(stored=True, commas=True),  # Compulsory
    )
"""


def search(
    ix: FileIndex,
    query_text: str,
    fields: List[str],
    categories: List[str] | None = None,
    keyword: List[str] | None = None,
    location: List[str] | None = None,
    author: List[str] | None = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    with ix.searcher() as searcher:
        parser = MultifieldParser(fields, schema=ix.schema)
        query = parser.parse(query_text)

        filters = []
        # https://whoosh.readthedocs.io/en/latest/api/query.html#query-classes
        # we can change Term for FuzzyTerm if we want to allow some mistakes
        if categories:
            filters.append(Or([Term("category", category) for category in categories]))
        if keyword:
            filters.append(Or([Term("keywords", k) for k in keyword]))
        if location:
            filters.append(Or([Term("location", loc) for loc in location]))
        if author:
            author_queries = []
            for auth in author:
                tokens = auth.split()
                author_queries.append(And([Term("author", t) for t in tokens]))
            filters.append(Or(author_queries))
        if date_from or date_to:
            filters.append(DateRange("datetime", date_from, date_to))

        if filters:
            query = And([query] + filters)

        results = searcher.search(query, limit=None)
        total = len(results)

        print(f"\nTotal results: {total}\n")

        for i, result in enumerate(results[:LIMIT], 1):
            print(f"[{i}] {result['title']}")
            subtitle = result.get("subtitle", "")
            if subtitle:
                print(f"    Subtitle: {subtitle}")
            print(f"    Document: {result['documentNumber']}")
            print(f"    Date: {result['datetime']}")
            print(f"    Category: {result.get('category', 'N/A')}")
            print(f"    Author: {result.get('author', 'N/A')}")
            print(f"    Location: {result.get('location', 'N/A')}")
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
        print("2. Exit")
        choice = input("\nSelect option: ").strip()

        if choice == "1":
            query_text = input("Enter query: ").strip()
            if not query_text:
                print("Query cannot be empty")
                continue

            print(
                "\nFields to search or filter by (in case of add more than one element per camp, write them separated by comma ','):\n"
            )
            fields_input = input(
                "Fields to search (title,subtitle,text,category,location,author,keywords) [default: title,subtitle,text]: "
            ).strip()
            if fields_input:
                fields = [f.strip() for f in fields_input.split(",")]
            else:
                fields = ["title", "subtitle", "text"]

            categories_input = input("Filter by categories (optional): ").strip()
            if categories_input:
                categories = [c.strip().lower() for c in categories_input.split(",")]
            else:
                categories = None
            keyword = input("Filter by keywords (optional): ").strip()
            if keyword:
                keyword = [k.strip().lower() for k in keyword.split(",")]
            else:
                keyword = None
            location_input = input("Filter by locations (optional): ").strip()
            if location_input:
                location = [l.strip().lower() for l in location_input.split(",")]
            else:
                location = None
            author_input = input("Filter by authors (optional): ").strip()
            if author_input:
                author = [a.strip() for a in author_input.split(",")]
            else:
                author = None

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

            search(
                ix,
                query_text,
                fields,
                categories,
                keyword,
                location,
                author,
                date_from,
                date_to,
            )

        elif choice == "2":
            print("Exiting...")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
