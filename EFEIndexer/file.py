from document import Document


class File:
    def __init__(self, path: str) -> None:
        """
        Initialize File object.

        Args:
            - path (str): The path to the file

        Returns:
            - None
        """
        self.path = path
        self.content = self._read_file()
        self.documents: list[Document] = self._parse_documents()

    def _read_file(self) -> str:
        with open(self.path, "r", encoding="iso-8859-1") as f:
            return f.read()

    def _parse_documents(self) -> list[Document]:
        # Get str text between <DOC> and </DOC>
        try:
            docs = self.content.split("<DOC>")
            docs = [doc.split("</DOC>")[0] for doc in docs if "</DOC>" in doc]
            return [Document(doc) for doc in docs]
        except Exception as e:
            print(f"Error parsing documents in file {self.path}: {e}")
            return []
        finally:
            self.content = ""  # Free memory
