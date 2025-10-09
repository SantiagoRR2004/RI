import os
from file import File

current_dir = os.path.dirname(os.path.abspath(__file__))


def parse_efe_corpus():
    efe_path = os.path.join(current_dir, "efe")

    files: list[File] = []
    for file in os.listdir(efe_path):
        if file.endswith(".sgml"):
            file_path = os.path.join(efe_path, file)
            file_obj = File(file_path)
            files.append(file_obj)

    for file in files:
        print(file.documents[0].getData()["title"])


if __name__ == "__main__":
    parse_efe_corpus()
