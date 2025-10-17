from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from collections import Counter
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
        self.showIDUniqueness()
        self.showDateTime()
        self.showCategory()
        self.showTitle()
        self.showText()
        self.showAuthor()
        self.showLocation()
        self.showKeywords()
        plt.show()

    @staticmethod
    def autopct_big_only(pct: float) -> str:
        # Show percentage only if it's above 5%
        return f"{pct:.1f}%" if pct > 5 else ""

    def showIDUniqueness(self) -> None:
        """
        Show if all document IDs are unique
        with a bar chart.

        Args:
            - None

        Returns:
            - None
        """
        ids = []

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                ids.append(doc.get("id", ""))

        # Count how many times each ID appears
        idCounts = Counter(ids)

        # Count how many times each ID count appears
        repetitions = Counter(idCounts.values())

        y = sorted(repetitions.keys())
        x = [repetitions[k] for k in y]

        # Plot results
        plt.figure(figsize=(6, 4))
        plt.bar(
            x,
            y,
        )
        plt.title("Distribution of ID Repetitions")
        plt.ylabel("Number of IDs")
        plt.xlabel("Number of times an ID appears")

        # No decimals on x-axis
        plt.xticks(x)

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

    def showCategory(self) -> None:
        """
        Show all the categories in the index.

        Args:
            - None

        Returns:
            - None
        """
        categories = {}

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                cat = doc.get("category", "")
                if cat in categories:
                    categories[cat] += 1
                else:
                    categories[cat] = 1

        # Need to sort categories by frequency
        categories = dict(sorted(categories.items(), key=lambda x: x[1], reverse=True))

        # Plot categories
        plt.figure(figsize=(9, 7))
        # No labels on the pie chart
        wedges, _, _ = plt.pie(
            [freq for freq in categories.values()],
            autopct=IndexManager.autopct_big_only,
        )
        plt.title("Category Frequency")
        plt.legend(
            wedges,
            [cat for cat in categories.keys()],
            loc="center left",
            bbox_to_anchor=(-0.3, 0.5),
        )

    def showTitle(self) -> None:
        """
        Show different statistics about titles in the index.

        Args:
            - None

        Returns:
            - None
        """
        titles = []

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                title = doc.get("title", "")
                titles.append(title)

        # Show the titles that are repeated
        repeatedTitles = {
            title: count for title, count in Counter(titles).items() if count > 1
        }

        # Sort by count
        repeatedTitles = dict(
            sorted(repeatedTitles.items(), key=lambda x: x[1], reverse=True)
        )
        maxLen = len(str(max(repeatedTitles.values())))

        print("Repeated Titles:")
        for title, count in repeatedTitles.items():
            print(f"{count:>{maxLen}}\t - {title}")

        # Get the list of word counts
        wordCounts = dict(Counter([word for title in titles for word in title.split()]))
        wordCounts = sorted(wordCounts.items(), key=lambda x: x[1], reverse=True)

        # Plot the frequency
        plt.figure(figsize=(10, 6))
        plt.plot(
            [i for i in range(len(wordCounts))],
            [freq for kw, freq in wordCounts],
            color="blue",
        )
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title("Words in Titles Frequency Distribution")
        # Eliminate the x-axis labels and ticks
        plt.xticks([])

        # Sow topN words in titles
        plt.figure(figsize=(16, 4))
        topN = 20
        plt.bar(
            [wordCounts[i][0] for i in range(topN)],
            [wordCounts[i][1] for i in range(topN)],
            color="blue",
        )
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title(f"Top {topN} Words in Titles")
        plt.xticks(rotation=45, ha="right", rotation_mode="anchor")

        # Raise the plot to make room for x labels
        plt.subplots_adjust(bottom=0.3)

    def showText(self) -> None:
        """
        Show statistics about the text in the index.

        Args:
            - None

        Returns:
            - None
        """
        texts = []

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                text = doc.get("text", "")
                texts.append(text)

        # Print if any document has repeated text
        textCounts = Counter(texts)
        repeatedTexts = {text: count for text, count in textCounts.items() if count > 1}
        if repeatedTexts:
            print("Repeated Texts:")
            for text, count in repeatedTexts.items():
                print(f"Count: {count}\n{text[:100]}\n{'-'*40}")
        else:
            print("No repeated texts found.")

        # Get the list of word counts
        wordCounts = [len(text.split()) for text in texts]

        # Plot the distribution of word counts
        plt.figure(figsize=(10, 6))
        plt.hist(wordCounts, bins=50, color="blue", alpha=0.7)
        plt.xlabel("Number of Words")
        plt.ylabel("Number of Documents")
        plt.title("Distribution of Document Lengths (in words)")

        # List of repeated words
        wordCounts = dict(Counter([word for text in texts for word in text.split()]))
        wordCounts = sorted(wordCounts.items(), key=lambda x: x[1], reverse=True)

        # Plot the frequency
        plt.figure(figsize=(10, 6))
        plt.plot(
            [i for i in range(len(wordCounts))],
            [freq for kw, freq in wordCounts],
            color="blue",
        )
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title("Words in Text Frequency Distribution")
        # Eliminate the x-axis labels and ticks
        plt.xticks([])

        # Show top N words
        plt.figure(figsize=(16, 4))
        topN = 20
        plt.bar(
            [wordCounts[i][0] for i in range(topN)],
            [wordCounts[i][1] for i in range(topN)],
            color="blue",
        )
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title(f"Top {topN} Words in Text")
        plt.xticks(rotation=45, ha="right", rotation_mode="anchor")

    def showAuthor(self) -> None:
        """
        Show the authors in the index
        as a pie chart.

        Args:
            - None

        Returns:
            - None
        """
        authors = {}

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                author = doc.get("author", "")
                if author in authors:
                    authors[author] += 1
                else:
                    authors[author] = 1

        sortedAuthors = dict(sorted(authors.items(), key=lambda x: x[1], reverse=True))

        # Plot authors
        plt.figure(figsize=(9, 7))
        # No labels on the pie chart
        wedges, _, _ = plt.pie(
            [freq for freq in sortedAuthors.values()],
            autopct=IndexManager.autopct_big_only,
        )
        plt.title("Author Frequency")
        plt.legend(
            wedges,
            [author for author in sortedAuthors.keys()],
            loc="center left",
            bbox_to_anchor=(-0.3, 0.5),
        )

        # Show top topN authors without "" (author unknown)
        del sortedAuthors[""]

        plt.figure(figsize=(10, 4))
        topN = 20
        plt.bar(
            [author for author in list(sortedAuthors.keys())[:topN]],
            [freq for freq in list(sortedAuthors.values())[:topN]],
            color="blue",
        )
        plt.xlabel("Authors")
        plt.ylabel("Frequency")
        plt.title(f"Top {topN} Authors")
        plt.xticks(rotation=45, ha="right", rotation_mode="anchor")

        # Move the plot up to make room for x labels
        plt.subplots_adjust(bottom=0.3)

    def showLocation(self) -> None:
        """
        Show the locations in the index
        as a bar chart.

        Args:
            - None

        Returns:
            - None
        """
        locations = {}

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                location = doc.get("location", "")
                if location in locations:
                    locations[location] += 1
                else:
                    locations[location] = 1

        sortedLocations = dict(
            sorted(locations.items(), key=lambda x: x[1], reverse=True)
        )

        # Show top topN locations
        plt.figure(figsize=(10, 4))
        topN = 20
        plt.bar(
            [loc for loc in list(sortedLocations.keys())[:topN]],
            [freq for freq in list(sortedLocations.values())[:topN]],
            color="blue",
        )
        plt.xlabel("Locations")
        plt.ylabel("Frequency")
        plt.title(f"Top {topN} Locations")
        plt.xticks(rotation=45, ha="right", rotation_mode="anchor")

        # Move the plot up to make room for x labels
        plt.subplots_adjust(bottom=0.3)

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
