from concurrent.futures import ProcessPoolExecutor
from whoosh import fields
from whoosh import index
from whoosh import analysis
from file import File
import tqdm
import os


class NOTHING(fields.FieldType):
    """
    Configured field type for fields you want do not want to index or store.

    This is necessary because we use dictionary unpacking to add documents
    """

    indexed = False
    stored = False

    def __init__(self):
        pass


class Collection:
    """
    Class representing a collection of documents.
    """

    text_analyzer = analysis.SimpleAnalyzer()
    schema = fields.Schema(
        documentNumber=fields.ID(stored=True, unique=True),
        # Skip documentID as it is the same as documentNumber
        documentID=NOTHING(),
        datetime=fields.DATETIME(stored=True),
        subCategory=NOTHING(),  # This is an abbreviation of category
        files=NOTHING(),  # Not needed
        destination=NOTHING(),  # Not compulsory, it is the abbreviation of location where the notice is read.
        category=fields.KEYWORD(stored=True, analyzer=text_analyzer),  # Compulsory
        key=NOTHING(),  # Not needed
        number=NOTHING(),  # Not needed
        priority=NOTHING(),  # There are only "R", "U" and some "B"
        title=fields.TEXT(stored=True, analyzer=text_analyzer),  # Compulsory
        text=fields.TEXT(stored=True, analyzer=text_analyzer),  # Main content
        author=fields.KEYWORD(
            stored=True, analyzer=text_analyzer, commas=False
        ),  # Not compulsory
        location=fields.TEXT(stored=True),
        keywords=fields.KEYWORD(stored=True, commas=True),  # Compulsory
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
        futures = []

        sgmlFiles = [
            file for file in os.listdir(self.inputFolder) if file.endswith(".sgml")
        ]

        with ProcessPoolExecutor() as executor:
            for file in sgmlFiles:
                filePath = os.path.join(self.inputFolder, file)
                futures.append(executor.submit(File, filePath))

        for future in futures:
            self.files.append(future.result())

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

        documents = [document for file in self.files for document in file.documents]

        for document in tqdm.tqdm(documents, desc="Adding documents to index"):
            data = document.getData()
            writer.add_document(**data)

        writer.commit()

    def addToIndex(self, indexpath: str) -> None:
        """
        Add documents to an existing index.

        Args:
            - indexpath (str): The path to the existing index

        Returns:
            - None
        """
        if not os.path.exists(indexpath):
            raise ValueError(f"Index path {indexpath} does not exist.")
        ix = index.open_dir(indexpath)
        writer = ix.writer()
        documents = [document for file in self.files for document in file.documents]
        for document in tqdm.tqdm(documents, desc="Adding documents to index"):
            data = document.getData()
            writer.add_document(**data)

        writer.commit()
