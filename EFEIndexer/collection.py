from whoosh import fields
from whoosh import index
from file import File
import os


class Collection:
    """
    Class representing a collection of documents.
    """

    schema = fields.Schema(
        documentNumber=fields.ID(stored=True, unique=True),
        # Skip documentID as it is the same as documentNumber
        datetime=fields.DATETIME(stored=True),
    )

    def __init__(self, inputFolder: str) -> None:
        """
        Initialize Collection object.

        Args:
            - inputFolder (str): The folder containing the input documents

        Returns:
            - None
        """
        self.inputFolder = inputFolder

        self.setAll()

    def setAll(self) -> None:
        """
        Set all attributes of the document.

        Args:
            - None

        Returns:
            - None
        """
        self.setFiles()

    def setFiles(self) -> None:
        """
        Set the document files.

        Args:
            - None

        Returns:
            - None
        """
        self.files: list[File] = []
        for file in os.listdir(self.inputFolder):
            if file.endswith(".sgml"):
                filePath = os.path.join(self.inputFolder, file)
                self.files.append(File(filePath))

    def createIndex(self, indexpath: str) -> None:
        """
        Create the index for the collection.

        Args:
            - indexpath (str): The path to the index

        Returns:
            - None
        """
        if not os.path.exists(indexpath):
            os.mkdir(indexpath)
        ix = index.create_in(indexpath, self.schema)
        writer = ix.writer()
        for file in self.files:
            for document in file.documents:
                data = document.getData()
                writer.add_document(
                    documentNumber=data["documentNumber"],
                    datetime=data["datetime"],
                )
        writer.commit()
