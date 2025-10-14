from file import File
import os


class Collection:
    """
    Class representing a collection of documents.
    """

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
