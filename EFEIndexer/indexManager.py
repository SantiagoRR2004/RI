import matplotlib.pyplot as plt
from whoosh import index
import numpy as np


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
        self.showTimeOfDay()
        plt.show()

    def showTimeOfDay(self) -> None:
        """
        Show distribution of documents by time of day.

        Args:
            - None

        Returns:
            - None
        """
        times = []

        with self.idx.searcher() as searcher:
            # Iterate over all documents in the index
            for docnum in range(searcher.doc_count()):
                doc = searcher.stored_fields(docnum)
                dtValue = doc.get("datetime")
                times.append(dtValue.hour + dtValue.minute / 60)

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
