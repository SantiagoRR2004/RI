from whoosh.query import And, Or, Term, DateRange
from whoosh.qparser import MultifieldParser
from whoosh.index import FileIndex
from datetime import datetime
from typing import List
import interface

LIMIT = 5


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


if __name__ == "__main__":
    interface.EFEQueryUI()
