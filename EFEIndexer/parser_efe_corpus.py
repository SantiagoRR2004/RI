from collection import Collection
import os

current_dir = os.path.dirname(os.path.abspath(__file__))


def parse_efe_corpus(dirname: str = "efe"):
    efe_path = os.path.join(current_dir, dirname)

    collection = Collection(efe_path)

    for file in collection.files:
        print(file.documents[0].getData()["title"])


if __name__ == "__main__":
    parse_efe_corpus()
