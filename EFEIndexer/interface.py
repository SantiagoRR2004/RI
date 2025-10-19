import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import scrolledtext
from datetime import datetime

from whoosh import index

import efe_query


class EFEQueryUI:
    DEFAULT_FIELDS = ["title", "text"]

    def __init__(self) -> None:
        """
        Initialize the EFE Query UI application.

        Sets up the initial state, creates the window and widgets,
        and starts the main event loop.

        Args:
            - None

        Returns:
            - None
        """
        self.initState()
        self.createWindow()
        self.createWidgets()
        self.window.mainloop()

    def initState(self) -> None:
        """
        Initialize the application state variables.

        Sets default values for index directory and top results limit.

        Args:
            - None

        Returns:
            - None
        """
        currentDir = os.path.dirname(os.path.abspath(__file__))
        self.indexDir = os.path.join(currentDir, "indexdir")
        self.topResults = getattr(efe_query, "LIMIT", 5)

    def createWindow(self) -> None:
        """
        Create and configure the main application window.

        Sets up the window title, size, minimum size, and grid layout.

        Args:
            - None

        Returns:
            - None
        """
        self.window = tk.Tk()
        self.window.title("EFE Query Interface")
        self.window.geometry("900x700")
        self.window.minsize(900, 650)
        for i in range(0, 12):
            self.window.grid_rowconfigure(i, weight=0)
        self.window.grid_rowconfigure(12, weight=1)
        self.window.grid_columnconfigure(0, weight=0)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=0)

    def createWidgets(self) -> None:
        """
        Create all widgets for the user interface.

        Calls individual methods to create each section of the UI.

        Args:
            - None

        Returns:
            - None
        """
        self.createIndexDir()
        self.createQueryText()
        self.createFieldSelection()
        self.createCategories()
        self.createKeywords()
        self.createLocations()
        self.createAuthors()
        self.createDateFrom()
        self.createDateToAndTopResults()
        self.createActionButtons()
        self.createResultsBox()

    def createIndexDir(self) -> None:
        """
        Create the index directory selection widgets.

        Includes a label, entry field, and browse button.

        Args:
            - None

        Returns:
            - None
        """
        r = 0
        tk.Label(self.window, text="Index directory:").grid(
            row=r, column=0, padx=8, pady=8, sticky="w"
        )
        self.indexDirVar = tk.StringVar(value=self.indexDir)
        self.indexEntry = tk.Entry(
            self.window, textvariable=self.indexDirVar, width=60, state="readonly"
        )
        self.indexEntry.grid(row=r, column=1, padx=8, pady=8, sticky="we")
        tk.Button(self.window, text="Browse...", command=self.browseIndexDir).grid(
            row=r, column=2, padx=8, pady=8, sticky="e"
        )

    def createQueryText(self) -> None:
        """
        Create the query text input field.

        Args:
            - None

        Returns:
            - None
        """
        r = 1
        tk.Label(self.window, text="Query:").grid(
            row=r, column=0, padx=8, pady=8, sticky="w"
        )
        self.queryVar = tk.StringVar()
        tk.Entry(self.window, textvariable=self.queryVar, width=60).grid(
            row=r, column=1, columnspan=2, padx=8, pady=8, sticky="we"
        )

    def createFieldSelection(self) -> None:
        """
        Create checkboxes for selecting which fields to search in.

        Default fields are 'title' and 'text'.

        Args:
            - None

        Returns:
            - None
        """
        r = 2
        tk.Label(self.window, text="Search fields:").grid(
            row=r, column=0, padx=8, pady=8, sticky="nw"
        )
        fieldsFrame = tk.Frame(self.window)
        fieldsFrame.grid(row=r, column=1, columnspan=2, padx=8, pady=8, sticky="w")
        self.fieldVars = {}
        for i, field in enumerate(
            ["title", "text", "category", "location", "author", "keywords"]
        ):
            var = tk.BooleanVar(value=(field in self.DEFAULT_FIELDS))
            self.fieldVars[field] = var
            cb = tk.Checkbutton(fieldsFrame, text=field, variable=var)
            cb.grid(row=0, column=i, padx=(0, 12), sticky="w")

    def createCategories(self) -> None:
        """
        Create the categories input field for filtering by categories.

        Args:
            - None

        Returns:
            - None
        """
        r = 3
        tk.Label(self.window, text="Categories (comma-separated):").grid(
            row=r, column=0, padx=8, pady=4, sticky="w"
        )
        self.categoriesVar = tk.StringVar()
        tk.Entry(self.window, textvariable=self.categoriesVar).grid(
            row=r, column=1, columnspan=2, padx=8, pady=4, sticky="we"
        )

    def createKeywords(self) -> None:
        """
        Create the keywords input field for filtering by keywords.

        Args:
            - None

        Returns:
            - None
        """
        r = 4
        tk.Label(self.window, text="Keywords (comma-separated):").grid(
            row=r, column=0, padx=8, pady=4, sticky="w"
        )
        self.keywordsVar = tk.StringVar()
        tk.Entry(self.window, textvariable=self.keywordsVar).grid(
            row=r, column=1, columnspan=2, padx=8, pady=4, sticky="we"
        )

    def createLocations(self) -> None:
        """
        Create the locations input field for filtering by locations.

        Args:
            - None

        Returns:
            - None
        """
        r = 5
        tk.Label(self.window, text="Locations (comma-separated):").grid(
            row=r, column=0, padx=8, pady=4, sticky="w"
        )
        self.locationsVar = tk.StringVar()
        tk.Entry(self.window, textvariable=self.locationsVar).grid(
            row=r, column=1, columnspan=2, padx=8, pady=4, sticky="we"
        )

    def createAuthors(self):
        """
        Create the authors input field for filtering by authors.

        Args:
            - None

        Returns:
            - None
        """
        r = 6
        tk.Label(self.window, text="Authors (comma-separated):").grid(
            row=r, column=0, padx=8, pady=4, sticky="w"
        )
        self.authorsVar = tk.StringVar()
        tk.Entry(self.window, textvariable=self.authorsVar).grid(
            row=r, column=1, columnspan=2, padx=8, pady=4, sticky="we"
        )

    def createDateFrom(self) -> None:
        """
        Create the 'date from' input field for date range filtering.

        Args:
            - None

        Returns:
            - None
        """
        r = 7
        tk.Label(self.window, text="Date from (YYYYMMDD):").grid(
            row=r, column=0, padx=8, pady=4, sticky="w"
        )
        self.dateFromVar = tk.StringVar()
        tk.Entry(self.window, textvariable=self.dateFromVar, width=20).grid(
            row=r, column=1, padx=8, pady=4, sticky="w"
        )
        tk.Label(self.window, text="Date to (YYYYMMDD):").grid(
            row=r, column=2, padx=8, pady=4, sticky="w"
        )

    def createDateToAndTopResults(self) -> None:
        """
        Create the 'date to' input field and top results spinbox.

        Args:
            - None

        Returns:
            - None
        """
        r = 8
        self.dateToVar = tk.StringVar()
        tk.Entry(self.window, textvariable=self.dateToVar, width=20).grid(
            row=r, column=2, padx=8, pady=(0, 8), sticky="w"
        )
        tk.Label(self.window, text="Top results:").grid(
            row=r, column=0, padx=8, pady=(0, 8), sticky="w"
        )
        self.topResultsVar = tk.IntVar(value=self.topResults)
        tk.Spinbox(
            self.window, from_=1, to=1000, width=6, textvariable=self.topResultsVar
        ).grid(row=r, column=1, padx=8, pady=(0, 8), sticky="w")

    def createActionButtons(self) -> None:
        """
        Create the Search and Reset buttons.

        Args:
            - None

        Returns:
            - None
        """
        r = 9
        buttonsFrame = tk.Frame(self.window)
        buttonsFrame.grid(row=r, column=0, columnspan=3, padx=8, pady=8, sticky="we")
        tk.Button(buttonsFrame, text="Search", command=self.onSearch).pack(
            side=tk.RIGHT, padx=(4, 0)
        )
        tk.Button(buttonsFrame, text="Reset", command=self.onReset).pack(
            side=tk.RIGHT, padx=(4, 0)
        )

    def createResultsBox(self) -> None:
        """
        Create the scrolled text widget for displaying search results.

        Args:
            - None

        Returns:
            - None
        """
        r = 10
        tk.Label(self.window, text="Results:").grid(
            row=r, column=0, padx=8, pady=4, sticky="nw"
        )
        self.results = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, height=20)
        self.results.grid(row=r, column=1, columnspan=2, padx=8, pady=4, sticky="nsew")
        self.writeResult("Ready. Select parameters and click Search.")

    def writeResult(self, text: str, clear: bool = False) -> None:
        """
        Write text to the results box.

        Args:
            - text: The text to write to the results box.
            - clear: If True, clear the results box before writing.

        Returns:
            - None
        """
        if clear:
            self.results.configure(state="normal")
            self.results.delete("1.0", tk.END)
        self.results.configure(state="normal")
        self.results.insert(tk.END, text + "\n")
        self.results.see(tk.END)
        self.results.configure(state="disabled")

    def browseIndexDir(self) -> None:
        """
        Open a folder dialog to select the Whoosh index directory.

        Args:
            - None

        Returns:
            - None
        """
        folder = filedialog.askdirectory(title="Select Whoosh index directory")
        if folder:
            self.indexDirVar.set(folder)

    def onReset(self) -> None:
        """
        Reset all input fields to their default values.

        Args:
            - None

        Returns:
            - None
        """
        self.queryVar.set("")
        self.categoriesVar.set("")
        self.keywordsVar.set("")
        self.locationsVar.set("")
        self.authorsVar.set("")
        self.dateFromVar.set("")
        self.dateToVar.set("")
        for f, var in self.fieldVars.items():
            var.set(f in self.DEFAULT_FIELDS)
        self.topResultsVar.set(getattr(efe_query, "LIMIT", 5))
        self.writeResult("Fields reset.", clear=True)

    def parseDate(self, s: str) -> datetime | None:
        """
        Parse a date string in YYYYMMDD format.

        Args:
            - s: Date string to parse.

        Returns:
            - datetime object or None if empty string.

        Raises:
            - ValueError: If date format is invalid.
        """
        if not s:
            return None
        try:
            return datetime.strptime(s, "%Y%m%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYYMMDD.")

    def splitList(self, s: str, toLower: bool = False) -> list[str] | None:
        """
        Split a comma-separated string into a list of items.

        Args:
            - s: Comma-separated string to split.
            - toLower: If True, convert all items to lowercase.

        Returns:
            - List of strings or None if empty.
        """
        if not s:
            return None
        items = [item.strip() for item in s.split(",") if item.strip()]
        if not items:
            return None
        if toLower:
            items = [i.lower() for i in items]
        return items

    def onSearch(self) -> None:
        """
        Handle the search button click event.

        Validates all input fields, opens the index, and performs the search
        using the efe_query module. Displays results in the results box.

        Args:
            - None

        Returns:
            - None
        """
        queryText = (self.queryVar.get() or "").strip()
        if not queryText:
            messagebox.showerror("Missing query", "Please enter a query text.")
            return
        fields = [name for name, var in self.fieldVars.items() if var.get()]
        if not fields:
            messagebox.showerror(
                "Missing fields", "Please select at least one field to search."
            )
            return
        indexDir = self.indexDirVar.get()
        if not indexDir or not os.path.isdir(indexDir):
            messagebox.showerror(
                "Index directory", "Please select a valid index directory."
            )
            return
        try:
            dateFrom = self.parseDate(self.dateFromVar.get().strip())
            dateTo = self.parseDate(self.dateToVar.get().strip())
        except ValueError as e:
            messagebox.showerror("Date error", str(e))
            return
        categories = self.splitList(self.categoriesVar.get(), toLower=True)
        keywords = self.splitList(self.keywordsVar.get(), toLower=True)
        locations = self.splitList(self.locationsVar.get(), toLower=True)
        authors = self.splitList(self.authorsVar.get(), toLower=False)
        try:
            topLimit = int(self.topResultsVar.get())
            if topLimit < 1:
                raise ValueError
        except Exception:
            messagebox.showerror(
                "Top results", "Top results must be a positive integer."
            )
            return
        efe_query.LIMIT = topLimit
        ix = None
        buf = None
        try:
            ix = index.open_dir(indexDir)
        except Exception as e:
            messagebox.showerror(
                "Open index failed", f"Could not open index at {indexDir}:\n{e}"
            )
            return
        import io
        from contextlib import redirect_stdout

        self.writeResult("Running search...", clear=True)
        buf = io.StringIO()
        search_error = None
        try:
            with redirect_stdout(buf):
                efe_query.search(
                    ix,
                    query_text=queryText,
                    fields=fields,
                    categories=categories,
                    keyword=keywords,
                    location=locations,
                    author=authors,
                    date_from=dateFrom,
                    date_to=dateTo,
                )
        except Exception as e:
            search_error = e
        if ix is not None:
            try:
                ix.close()
            except Exception:
                pass
        if search_error is not None:
            messagebox.showerror(
                "Search error", f"An error occurred during search:\n{search_error}"
            )
            return
        output = buf.getvalue().strip() if buf is not None else ""
        if not output:
            output = "No output."
        self.writeResult(output, clear=True)


if __name__ == "__main__":
    EFEQueryUI()
