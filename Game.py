import time
import json
import os.path


class Game:
    def __init__(self, path):
        # Assert path variable is correct and make lowercase
        path = path.lower()
        assert isinstance(path, str), "[Game] Path should be of type \"string\", is " + str(type(path))
        assert os.path.isfile(path), "[Game] Path should point at an existing file"
        assert path.endswith(".json"), "[Game] Path should end with .json"

        # Set attributes
        self.field = {}
        self.timeEnded = None
        self.contaminatedCellCount = 0
        self.contaminatedCellsFound = 0
        self.wrongCellsFound = 0

        # Load file and set data
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        i = 0
        for column in data["columns"]:
            if column["contaminated"]:
                # If column is contaminated increase contaminatedCellCount by one
                self.contaminatedCellCount += 1

            cells = []
            for cell in column["cells"]:
                # If cell is contaminated increase contaminatedCellCount by one
                if cell["contaminated"]:
                    self.contaminatedCellCount += 1

                # Create a new cell object for every cell and append it to the list
                cells.append(Cell(cell["value"], cell["contaminated"], cell["message"]))

            # For every column create a new column object and add it to the dictionary
            self.field[i] = Column(column["name"], column["contaminated"], column["message"], cells)
            i += 1

    # Method for checking if the game is finished
    def isFinished(self):
        if self.contaminatedCellsFound >= self.contaminatedCellCount:
            self.timeEnded = time.time()
            return True
        else:
            return False

    # Method for playing a specific cell
    def playCell(self, x, y = -1):
        if y == -1:
            # Playing a column header
            cell = self.field[x]
        else:
            # Playing a cell
            cell = self.field[x].cells[y]

        if cell.played:
            raise ValueError("Deze cel is al eerder geprobeerd, probeer een andere!")
        else:
            cell.played = True
            if cell.contaminated:
                self.contaminatedCellsFound += 1
            else:
                self.wrongCellsFound += 1

    def getWrongAnswers(self):
        return str(self.wrongCellsFound)

    def getCellsFound(self):
        return str(self.contaminatedCellsFound) + " / " + str(self.contaminatedCellCount)

    def getColumnCount(self):
        return len(self.field)

    def getCellCount(self):
        return len(self.field[0].cells)

class Column:
    def __init__(self, name, contaminated, message, cells):
        # Assert all variables are correct
        assert isinstance(name, str), "[Column] Name should be of type \"string\", is " + str(type(name))
        assert len(name) > 0, "[Column] Name should have a length greater than 0 characters, is" + str(len(name))

        # Set attributes
        self.name = name
        self.contaminated = contaminated
        self.message = message
        self.played = False
        self.cells = {}

        # Assert all values are cells and insert list of cells into dictionary with index as key
        i = 0
        for cell in cells:
            assert isinstance(cell, Cell), "[Column] Cell should be of type \"Cell\", is " + str(type(cell))
            self.cells[i] = cell
            i += 1


class Cell:
    def __init__(self, value, contaminated, message):
        # Assert all variables are correct
        assert isinstance(value, str), "[Cell] Value should be of type \"string\", is " + str(type(value))
        assert isinstance(contaminated, bool), "[Cell] Contaminated should be of type \"bool\", is " + str(type(contaminated))
        assert isinstance(message, str), "[Cell] Message should be of type \"string\", is " + str(type(message))
        assert len(value) > 0, "[Cell] Value should have a length greater than 0 characters, is " + str(len(value))
        assert len(message) > 0, "[Cell] Message should have a length greater than 0 characters, is" + str(len(message))

        # Set attributes
        self.value = value
        self.contaminated = contaminated
        self.message = message
        self.played = False
