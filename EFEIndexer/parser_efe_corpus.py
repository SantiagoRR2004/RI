from collection import Collection
import os


def parse_efe_corpus(dirpath: str = "efe") -> Collection:
    """
    Parse the EFE corpus located in the specified directory.

    Args:
        - dirname (str): The directory containing the EFE SGML files. Default is "efe".

    Returns:
        - Collection: A Collection object containing the parsed documents.
    """
    return Collection(dirpath)


if __name__ == "__main__":
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    c = parse_efe_corpus(os.path.join(currentDirectory, "efe"))

    for file in c.files:
        print(file.documents[0].getData()["title"])
