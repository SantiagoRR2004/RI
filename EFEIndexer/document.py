from datetime import datetime
from rake_nltk import Rake
import nltk
import re

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    print("Downloading punkt_tab...")
    nltk.download("punkt_tab", quiet=True)

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    print("Downloading stopwords...")
    nltk.download("stopwords", quiet=True)


class Document:
    """
    Class representing a document object.
    """

    rake = Rake(stopwords=nltk.corpus.stopwords.words("spanish"), language="spanish")

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
        self.setDatetime()
        self.setSubCategory()
        self.setFiles()
        self.setDestination()
        self.setCategory()
        self.setKey()
        self.setNumber()
        self.setPriority()
        self.setTitle()
        self.setText()
        self.setAuthor()
        self.setLocation()
        self.cleanText()
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

    def setDatetime(self) -> None:
        """
        Set the document datetime.

        Args:
            - None

        Returns:
            - None
        """
        matchDate = re.search(r"<DATE>(\d{8})</DATE>", self.rawText)
        matchTime = re.search(r"<TIME>(\d{2}\.\d{2})</TIME>", self.rawText)
        datePart = datetime.strptime(matchDate.group(1), "%Y%m%d").date()
        timePart = datetime.strptime(matchTime.group(1), "%H.%M").time()

        combined = datetime.combine(datePart, timePart)

        self.datetime = combined

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

    def setAuthor(self) -> None:
        """
        Set the document author.

        It is not always present inside of the text.
        To find it we look that the word "Por" is at
        the beginning of the whole text and get
        everything that comes after it until a line break.

        Args:
            - None

        Returns:
            - None
        """
        match = re.search(r"^\s*Por (.*?)\n", self.text)
        if match:
            self.author = match.group(1).strip()
            # Remove the author line from the text
            self.text = re.sub(r"^\s*Por .*?\n", "", self.text, count=1).strip()
        else:
            self.author = None

    def setLocation(self) -> None:
        """
        Set the document location.

        It is not always present inside of the text.
        To find it we look for "(EFE).-" and everything
        that came before it. If found, the location is all
        the text before a comma if the length is small
        enough.

        Everything in the match is removed from the text.

        Args:
            - None

        Returns:
            - None
        """
        pattern = r"^([\s\S]*?\(EFE\)\.-)"
        match = re.search(pattern, self.text)
        if match and len(match.group(1)) < 100:
            self.location = match.group(1).strip().split(",")[0]
            # Remove the location line from the text
            self.text = re.sub(pattern, "", self.text, count=1).strip()
        else:
            self.location = None

    def cleanText(self) -> None:
        """
        Clean the document text by removing extra whitespace
        and the author at the end.

        Because each text is very small, we do not need to
        keep line breaks.

        Args:
            - None

        Returns:
            - None
        """
        self.text = re.sub(r"\s+", r" ", self.text).strip()

        # This pattern matches the last 'EFE' and deletes everything after it
        self.text = re.sub(r"(.*)EFE.*", r"\1", self.text).strip()

    def setKeywords(self) -> None:
        """
        Set the document keywords.

        Args:
            - None

        Returns:
            - None
        """
        # Extract keywords
        self.rake.extract_keywords_from_text(self.text)

        # Get ranked phrases (keywords)
        keywords = self.rake.get_ranked_phrases()

        # Keep only the ones with one word
        keywords = [kw for kw in keywords if len(kw.split()) == 1]

        finalKeywords = set()

        while len(finalKeywords) < 3 and keywords:
            k = keywords.pop(0)
            if not k.isdigit():
                finalKeywords.add(k)

        self.keywords = list(finalKeywords)

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
            "datetime": self.datetime,
            "subCategory": self.subCategory,
            "files": self.files,
            "destination": self.destination,
            "category": self.category,
            "key": self.key,
            "number": self.number,
            "priority": self.priority,
            "title": self.title,
            "text": self.text,
            "author": self.author,
            "location": self.location,
            "keywords": self.keywords,
        }
