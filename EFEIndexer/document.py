import re


class Document:
    """
    Class representing a document object.
    """

    def __init__(self, rawText: str) -> None:
        """
        Initialize Document object.

        Args:
            - rawText (str): The raw text of the document

        Returns:
            - None
        """
        self.rawText = rawText

        self.setAll()

    def setAll(self) -> None:
        """
        Set all attributes of the document.

        Args:
            - None

        Returns:
            - None
        """
        self.setDocumentNumber()
        self.setDocumentID()
        self.setDate()
        self.setTime()
        self.setSubCategory()
        self.setFiles()
        self.setDestination()
        self.setCategory()
        self.setKey()
        self.setNumber()
        self.setPriority()
        self.setTitle()
        self.setText()
        self.setKeywords()

    def setDocumentNumber(self) -> None:
        """
        Set the document number.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<DOCNO>(.*?)</DOCNO>", self.rawText)
        self.documentNumber = match.group(1)

    def setDocumentID(self) -> None:
        """
        Set the document ID.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<DOCID>(.*?)</DOCID>", self.rawText)
        self.documentID = match.group(1)

    def setDate(self) -> None:
        """
        Set the document date.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<DATE>(\d{8})</DATE>", self.rawText)
        self.date = match.group(1)

    def setTime(self) -> None:
        """
        Set the document time.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<TIME>(\d{2}\.\d{2})</TIME>", self.rawText)
        self.time = match.group(1)

    def setSubCategory(self) -> None:
        """
        Set the document subcategory.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<SCATE>(.*?)</SCATE>", self.rawText)
        self.subCategory = match.group(1)

    def setFiles(self) -> None:
        """
        Set the document files.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<FICHEROS>(.*?)</FICHEROS>", self.rawText)
        self.files = match.group(1)

    def setDestination(self) -> None:
        """
        Set the document destination.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<DESTINO>(.*?)</DESTINO>", self.rawText)
        self.destination = match.group(1)

    def setCategory(self) -> None:
        """
        Set the document category.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<CATEGORY>(.*?)</CATEGORY>", self.rawText)
        self.category = match.group(1)

    def setKey(self) -> None:
        """
        Set the document key.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<CLAVE>(.*?)</CLAVE>", self.rawText)
        self.key = match.group(1)

    def setNumber(self) -> None:
        """
        Set the document number internal to the collection.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<NUM>(\d+)</NUM>", self.rawText)
        self.number = match.group(1)

    def setPriority(self) -> None:
        """
        Set the document priority.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<PRIORIDAD>(.*?)</PRIORIDAD>", self.rawText)
        self.priority = match.group(1)

    def setTitle(self) -> None:
        """
        Set the document title.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<TITLE>(.*?)</TITLE>", self.rawText, re.DOTALL)
        self.title = match.group(1)

    def setText(self) -> None:
        """
        Set the document text.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"<TEXT>(.*?)</TEXT>", self.rawText, re.DOTALL)
        self.text = match.group(1)

    def setKeywords(self) -> None:
        """
        Set the document keywords.

        TODO: Implement keyword extraction.

        Args:
            - None

        Returns:
            - None
        """
        self.keywords = None

    def getData(self) -> dict:
        """
        Get card data as a dictionary

        Args:
            - None

        Returns:
            - dict: Dictionary containing all card attributes
        """
        return {
            "documentNumber": self.documentNumber,
            "documentID": self.documentID,
            "date": self.date,
            "time": self.time,
            "subCategory": self.subCategory,
            "files": self.files,
            "destination": self.destination,
            "category": self.category,
            "key": self.key,
            "number": self.number,
            "priority": self.priority,
            "title": self.title,
            "text": self.text,
            "keywords": self.keywords,
        }
