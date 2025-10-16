from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from whoosh import index
import numpy as np
import datetime


class IndexManager:
    """
    Class representing an index manager for whoosh.
    """

    def __init__(self, indexpath: str) -> None:
        """
        Initialize IndexManager object.

        Args:
            - indexpath (str): The folder containing the index

        Returns:
            - None
        """
        self.indexpath = indexpath
        self.idx = index.open_dir(indexpath)

    def showStats(self) -> None:
        """
        Show index statistics.

        Args:
            - None

        Returns:
            - None
        """
        self.showDateTime()
        self.showKeywords()
        plt.show()

    def showDateTime(self) -> None:
        """
        Show distribution of documents by time of day
        and by date.

        Args:
            - None

        Returns:
            - None
        """
        times = []
        dates = []

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                dtValue: datetime.datetime = doc.get("datetime")
                times.append(dtValue.hour + dtValue.minute / 60)
                dates.append(dtValue.date())

        angles = (np.array(times) / 24) * 2 * np.pi

        # Plot histogram in polar coordinates
        plt.figure(figsize=(6, 6))
        ax = plt.subplot(111, polar=True)
        ax.hist(angles, bins=24, color="blue", density=True)
        ax.hist(angles, bins=240, color="red", alpha=0.5, density=True)

        # Customize the radial plot
        ax.set_theta_zero_location("N")  # Midnight at the top
        ax.set_theta_direction(-1)  # Clockwise
        ax.set_xticks(np.linspace(0, 2 * np.pi, 24, endpoint=False))
        ax.set_xticklabels([f"{int(h)}:00" for h in range(24)])
        ax.set_title("Distribution of Time of Day", va="bottom")
        ax.set_yticks([])

        # Show the date graph
        plt.figure(figsize=(10, 4))
        uniqueDates, counts = np.unique(dates, return_counts=True)
        plt.plot(uniqueDates, counts, color="blue")
        plt.xlabel("Date")
        plt.ylabel("Number of Documents")
        plt.title("Distribution of Documents Over Time")

    def showKeywords(self) -> None:
        """
        Show all the keywords in the index.

        Args:
            - None

        Returns:
            - None
        """
        keywords = {}

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                for kw in doc.get("keywords", []):
                    if kw in keywords:
                        keywords[kw] += 1
                    else:
                        keywords[kw] = 1

        sortedKeywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)

        # Plot keywords
        plt.figure(figsize=(10, 6))
        plt.plot(
            [i for i in range(len(sortedKeywords))],
            [freq for kw, freq in sortedKeywords],
            color="blue",
        )
        plt.xlabel("Keywords")
        plt.ylabel("Frequency")
        plt.title("Keyword Frequency Distribution")

        # Eliminate the x-axis labels and ticks
        plt.xticks([])

        # Show top, middle (25%), and bottom keywords
        numberEach = 5
        n = len(sortedKeywords)

        # Create indices for each section
        topIndices = list(range(numberEach))
        middleIndices = [int(n // 4 - i) for i in range(numberEach, 0, -1)]
        bottomIndices = [n - i - 1 for i in range(numberEach)]

        # Create a figure with 3 subplots
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

        # Top keywords
        ax1.bar(
            [sortedKeywords[i][0] for i in topIndices],
            [sortedKeywords[i][1] for i in topIndices],
            color="blue",
        )
        ax1.set_xlabel("Keywords")
        ax1.set_ylabel("Frequency")
        ax1.set_title("Top Keywords")
        ax1.tick_params(axis="x", rotation=45)

        # Middle keywords
        ax2.bar(
            [sortedKeywords[i][0] for i in middleIndices],
            [sortedKeywords[i][1] for i in middleIndices],
            color="green",
        )
        ax2.set_xlabel("Keywords")
        ax2.set_ylabel("Frequency")
        ax2.set_title("Middle Keywords (around 25%)")
        ax2.tick_params(axis="x", rotation=45)
        ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

        # Bottom keywords
        ax3.bar(
            [sortedKeywords[i][0] for i in bottomIndices],
            [sortedKeywords[i][1] for i in bottomIndices],
            color="red",
        )
        ax3.set_xlabel("Keywords")
        ax3.set_ylabel("Frequency")
        ax3.set_title("Bottom Keywords")
        ax3.tick_params(axis="x", rotation=45)
        ax3.yaxis.set_major_locator(MaxNLocator(integer=True))

        plt.tight_layout()

        # Top 20 keywords
        plt.figure(figsize=(16, 4))
        topN = 20
        plt.bar(
            [sortedKeywords[i][0] for i in range(topN)],
            [sortedKeywords[i][1] for i in range(topN)],
            color="blue",
        )
        plt.xlabel("Keywords")
        plt.ylabel("Frequency")
        plt.title(f"Top {topN} Keywords")
        plt.xticks(rotation=45)
