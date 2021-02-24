import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Check for each variable
        for var in self.domains:
            # Check for all word in variable
            for word in self.domains[var].copy():
                # Check for invalid length
                if len(word) != var.length:
                    # Remove invalid word
                    self.domains[var].remove(word)
        #print(f"Domain after enforce node: {self.domains}" )

    def overlap_word(self, x, x_word, y):
        """
        Checking for valid overlap word in x and y variable
        """
        if self.crossword.overlaps[x, y]:
            overlap_x = self.crossword.overlaps[x, y][0]
            overlap_y = self.crossword.overlaps[x, y][1]
            #print(f"Y: {self.domains[y]}")
            for y_word in self.domains[y]:
                #print(f"Compare: {overlap_x} index {x_word} with {overlap_y} index {y_word}")
                if x_word[overlap_x].lower() == y_word[overlap_y].lower():
                    #print(f"Overlap : {x_word[overlap_x].lower()} in {x_word} , {y_word[overlap_y].lower()} in {y_word} ")
                    return True

            return False

        return True

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        #print(f"Revising: {x}, {y}")
        for x_word in self.domains[x].copy():
            # No satisfied word in y
            #print(f"Checking: {x_word} in X")
            if not self.overlap_word(x, x_word, y):
                # Remove word from possible domain
                #print(f"Removing: {x_word} because {self.domains[y]}")
                self.domains[x].remove(x_word)
                revised = True
        
        #print(f"Domain after Revise: {self.domains[x]}")

        return revised
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Create empty queue
        queue = []
        # Making all possible (x, y)
        for var_x in self.crossword.variables:
            for var_y in self.crossword.variables:
                if var_x == var_y:
                    continue

                if (var_y, var_x) not in queue and (var_x, var_y) not in queue:
                    queue.append((var_x, var_y))
                    #print(f"{var_x}, {var_y}")
        while queue:
            # (X, Y) = DEQUEUE(queue)
            (x, y) = queue[0]
            queue = queue[1:]
            #print(f"b4 revise: {self.domains[x]} with {self.domains[y]}")
            # Revising word
            if self.revise(x, y):
                #print(self.domains[x])
                
                if len(self.domains[x]) == 0:
                    return False

                # Enqueue for Z in X.neighbor - {Y}
                for z in (self.crossword.neighbors(x)):
                    if z != y and (z, x) not in queue:
                        queue.append((z, x))

        #print(f"Domain after AC3: {self.domains}")
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if assignment.keys():

            for var in assignment:
                # Check for None value
                if not assignment[var]:
                    return False

            if len(assignment) != len(self.domains):
                return False

            return True

        return False

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        word_list = []
        #print(f"Consistence: {assignment}")
        for var in assignment:

            if assignment[var]:
                # Add word to word list for duplicate check
                word_list.append(assignment[var])

                # Checking length
                if len(assignment[var]) != var.length:
                    return False

                # Check for neightbor conflict
                neighbors = self.crossword.neighbors(var)

                for neighbor in neighbors:
                    overlap_var = self.crossword.overlaps[var, neighbor][0]

                    if neighbor in assignment:
                        #print(f"{neighbor} in {assignment.keys()}")
                        overlap_neighbor = self.crossword.overlaps[var, neighbor][1]

                        # Check for same alphabet at overlap
                        #print(f"Word in: {assignment[var]}")
                        if assignment[var][overlap_var] != assignment[neighbor][overlap_neighbor]: return False

        # Check for duplicate word            
        if len(word_list) != len(set(word_list)):
            return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Choosing one with fewest X.domains remove count
        def sort_key(var_word):
            # Count all word that not arc consistence with var word
            remove_count = 0 
            # Check for each neighbor variable
            for neighbor in neighbors.copy():
                # Specified the overlap index
                (var_index, neighbor_index) = self.crossword.overlaps[var, neighbor]
                # Check for each word in neigbor
                for neighbor_word in self.domains[neighbor]:
                    if var_word[var_index] != neighbor_word[neighbor_index]:
                        remove_count += 1
            #print(f"{var_word} remove {remove_count}")
            return remove_count

        #print(f"Assignment: {assignment}")
        #print(f"Ordering: {self.domains[var]}")

        # Check all var neighbor
        neighbors = self.crossword.neighbors(var)
        # Remove variable that already assign
        for neighbor in neighbors.copy():
            if neighbor in assignment:
                neighbors.remove(neighbor)
        #print(f"None Assign Neigbor: {neighbors}")

        # Sorting
        sorted_domains = list(self.domains[var])
        sorted_domains.sort(key=sort_key)
        #print(f"Ordered: {sorted_domains}")

        return sorted_domains


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Sort with NO of word and neigbor
        def sort_key(var):
            
            word_no = len(self.domains[var])

            # Reverse neighbor number
            neighbor_no = len(self.crossword.neighbors(var))
            max_neighbor = len(self.domains) - 1
            reverse_neighbor_no = max_neighbor - neighbor_no

            #print(f"Variable: {var}")
            #print(f"Word: {word_no}")
            #print(f"Neighbor: {neighbor_no}")

            return (word_no, reverse_neighbor_no)

        # Sorting variables
        var_list = list(self.domains)
        var_list.sort(key=sort_key)
        
        if assignment:
            #print(f"Assignment: {assignment}")
            # Remove Assign variable
            for var in var_list.copy():
                if var in assignment:
                    #print(f"Remove: {var} from {var_list}")
                    var_list.remove(var)
        #print(f"Remain: {var_list}")
        return var_list[0]
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            # Adding value to temp assignment to check consistence
            new_assignment = assignment.copy()
            new_assignment[var] = value

            if self.consistent(new_assignment):
                assignment[var] = value
                #print(f"Assign: {value} to {var}")
                result = self.backtrack(assignment)

                if result: return result
            if var in assignment:
                del assignment[var]

        return None
    


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
