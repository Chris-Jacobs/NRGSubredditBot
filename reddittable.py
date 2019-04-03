class RedditTable:
    def __init__(self, columns, rows = None, prefix = None, suffix = None):
        """
        Constructor for RedditTable
        Args:
            columns: List of RedditColumn Objects
            rows: List of List of Strings or None if no rows upon initialization
            prefix: Any string to be inserted before the table
            suffix: Any string to be inserted after the table

        """
        self.columns = columns
        if rows is None:
            self.rows = []
        else:
            self.rows = rows
        self.prefix = prefix
        self.suffix = suffix
    def __str__(self):
        """
        Converts the object into a Markdown Table
        Returns:
            Markdown table with prefix and suffix's attached if present
        """
        if self.columns is None:
            return ""
        prefix = ""
        if self.prefix is not None:
            prefix = self.prefix + "\n\n"
        suffix = ""
        if self.suffix is not None:
            suffix = self.suffix + "\n\n"
        table = ""
        header = ""
        pipes = ""
        body = ""
        for column in self.columns:
            header += column.text + "|"
            if column.centered:
                pipes += ":-:|"
            else:
                pipes += "-|"
        for row in self.rows:
            for cell in row:
                body += str(cell) + "|"
            body += "\n"
        table = prefix + header + "\n" + pipes + "\n" + body + suffix
        return table
    def addRow(self, row):
        self.rows.append(row)
    def addRows(self, rows):
        self.rows.extend(rows)
    def clearRows(self):
        self.rows = []
class RedditColumn:
    def __init__(self, text, centered = False):
        self.text = text
        self.centered = centered
