import itertools
import random
from copy import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count


    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # All cell are mined
        if len(self.cells) == self.count:
            return self.cells

        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # No cell are mined
        if self.count == 0:
            return self.cells
        
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # In Sentence
        if cell in self.cells:
           # Remove from sentence cell and count
           self.cells.remove(cell)
           self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # In Sentence
        if cell in self.cells:
            # Only remove cell from suspect mine count still the same
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        print("\n")
        # Mark as moved
        self.moves_made.add(cell)

        # Mark as safe
        self.mark_safe(cell)
        # Add sentence from cell (i, j) with count mine around
        i = cell[0]
        j = cell[1]
        cells = set()
        # Make square loop around (i, j)
        for h in range((i - 1), (i + 2)):
            for w in range((j - 1), (j + 2)):
                # Self Exclude
                if (h, w) != (i, j) and  (h, w) not in self.moves_made:
                    # Is is still on the board?
                    if h in range(self.height) and w in range(self.width):
                        # Is it already safe
                        if (h, w) not in self.safes:
                            # Is it already known mine on that point
                            if (h, w) in self.mines:
                                count -= 1
                            else:
                                # Add Cell to sentence
                                cells.add((h, w))

        # Create new sentence
        new_sentence = Sentence(cells, count)
        print("\n" * 100)
        print(f"New Clue: {new_sentence}")
        if len(self.knowledge) == 0:
            # Add Raw Sentence
            #print(f"Adding {new_sentence}")
            self.knowledge.append(new_sentence)

            # Check for mine and safe in sentence
            self.mark_new(new_sentence)

        elif len(self.knowledge) == 1:
            # Add new knowledge
            self.knowledge.append(new_sentence)
            self.mark_new(new_sentence)
            
            knowledges = []
            # Check Subset
            self.subset_check(self.knowledge[0], self.knowledge[1], knowledges)

            # Remove Blank Sentence
            self.rm_blank()

            
        else:
            # Add new knowledge
            self.knowledge.append(new_sentence)
            self.mark_new(new_sentence)
            # Remove Blank Sentence
            self.rm_blank()

            # New temp Knowledges
            knowledges = []
            # Loop for all sentence in knowledge check for subset
            for i in range(len(self.knowledge)):
                for j in range(i + 1, len(self.knowledge)):
                    # For Debug
                    #print(f"i = {i}, j = {j}, Total = {len(self.knowledge)}")
                    #print(f"Checking for {self.knowledge[i]}, {self.knowledge[j]}")
                    # Check Subset
                    self.subset_check(self.knowledge[i], self.knowledge[j], knowledges)


            # Get new knowledge
            self.knowledge = knowledges

            # Check for mine and safe in sentence
            for sentence in self.knowledge:
                self.mark_new(sentence)


        print("\n")
        self.rm_blank()
        print(f"Total Knowledge: {len(self.knowledge)}")
        for i in range(len(self.knowledge)):
            print(f"Knowledge {i + 1}: {self.knowledge[i]}")
        print(f"Known Mine: {self.mines}")
        print(f"Known Safe: {self.safes - self.moves_made}")
        
        



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Check for valid safe
        if len(self.safes) != 0:
            for cell in self.safes:
                # Not moved yet
                if cell not in self.moves_made:
                    return cell

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Check for valid cell and not mined
        for h in range(self.height):
            for w in range(self.width):
                if (h, w) not in self.moves_made:
                    if (h, w) not in self.mines:
                        random_cell = (h, w)

                        return random_cell

    def mark_new(self, sentence):
        if sentence.known_mines():
            new_mine = sentence.known_mines().copy()
            #print(f"New Mine: {new_mine}")
            for cell in new_mine:
                self.mark_mine(cell)

        if sentence.known_safes():
            new_safe = sentence.known_safes().copy()
            #print(f"New Safe: {new_safe}")
            for cell in new_safe:
                self.mark_safe(cell)


    def rm_blank(self):
        blank_sentence = Sentence(set(), 0)
        self.knowledge = list(filter(lambda a: a != blank_sentence, self.knowledge))


    def subset_check(self, sentence1, sentence2, knowledges):

        add_sentence = Sentence(set(), 0)

        if sentence1.cells.issubset(sentence2.cells):

            # Substract
            #print(f"{sentence1} is subset of {sentence2}")
            add_sentence.cells = sentence2.cells - sentence1.cells
            add_sentence.count = sentence2.count - sentence1.count
            #print(f"Remove {sentence2} Insert {add_sentence}")

            # Add to Knowledges
            knowledges.append(add_sentence)

            # Also Add Subset to Knowledges
            if sentence1 not in knowledges:
                knowledges.append(sentence1)

        elif sentence2.cells.issubset(sentence1.cells):

            # Substract
            #print(f"{sentence2} is subset of {sentence1}")
            add_sentence.cells = sentence1.cells - sentence2.cells
            add_sentence.count = sentence1.count - sentence2.count
            #print(f"Remove {sentence1} Insert {add_sentence}")

            # Add to Knowledges
            knowledges.append(add_sentence)

            # Also Add Subset to Knowledges
            if sentence2 not in knowledges:
                knowledges.append(sentence2)

        # Not Any subset then add it to place
        else:
            if sentence1 not in knowledges:
                knowledges.append(sentence1)
                #print(f"{sentence1} not any subset or superset.")

            if sentence2 not in knowledges:
                knowledges.append(sentence2)
                #print(f"{sentence2} not any subset or superset.")