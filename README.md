# CS50AI

## Project 0 Search Algorithm

### Degree
- Application of Node, Frontier and Search algorithm
- Find shortest related path of between any two actor by choosing a sequence of movies that connects them
- Using IMDB's database as reference.
- Command: $ python degrees.py large

### Tic-Tac-Toe
- Application of State, Action, Result, Terminal and Minimax
- Create an Tic-Tac-Toe AI that play against human
- AI will never lose to human
- Command: $ python runner.py

## Project 1 Knowledge

### Knights
- Application of Sentence and Logical operation
- Create an AI that play Knight/Knave Puzzle 
- Teaching Logical Knowledge to AI and let it solve Knight/Knave Puzzle
- More on Knight/Knave: https://en.wikipedia.org/wiki/Knights_and_Knaves

### Minesweeper
- Application of Set knowledge, Sentence and Logical operation
- Create an AI that play Minesweeper game
- Teach knowledge in set form to AI and compute the knowledge about mines & safe position on board
- Command: $ python runner.py

## Project 2 Uncertainty

### Pagerank
- Create an Algorithm to rank page base on link from another page
- PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named)
- Command: $ python pagerank.py corpus0

### Heredity
- Application of Probability knowledge
- Write an AI to assess the likelihood that a person will have a particular genetic trait
- Command: $ python heredity.py data/family0.csv

## Project 3 Optimization

### Crossword
- Application of Node Consistency, Arc Consistency(AC3) and Backtracking search algorithm
- Write an AI to generate crossword puzzles on various puzzle form and words choice
- Command: $ python generate.py data/structure1.txt data/words1.txt output.png

## Project 4 Learning

### Shopping
- Application of Supervised Machine Learning, KNN Classifier and scikit-learn
- Write an AI to predict whether online shopping customers will complete a purchase
- Command: $ python shopping.py shopping.csv

### Nim
- Application of Reinforcement Learning and Q-Learning 
- Create an AI that teaches itself to play Nim through reinforcement learning
- More on NIM: https://en.wikipedia.org/wiki/Nim
- Command: $ python play.py

## Project 5 Neural Network

### Traffic
- Application of Neural Network, Node Activation Method, Convolution Layers, Pooling Layers, TensorFLOW(keras), scikit-learn and Open-CV
- Create/Design Neural Network to classify 43 different traffic sign appears in photographs
- Command: $ python traffic.py gtsrb
- <a href="https://www.youtube.com/watch?v=AD0RTo5dkUE">Watch Program on Action</a>
- Using <a href="https://benchmark.ini.rub.de/?section=gtsrb&subsection=news"> German Traffic Sign Recognition Benchmark (GTSRB) dataset </a>
- Try <a href="https://playground.tensorflow.org/">TensorFlow Playground </a>

## Project 6 Language

### Parser
- Application of Natural Language Processing, Tokenization, Context-Free grammar and NLTK
- Write an AI to parse sentences and extract noun phrases
- Command: $ python parser.py
    
### Questions
- Application of Natural Language Processing, Tokenization, IDF(inverse document frequency), TF-IDF(term frequency–inverse document frequency) and NLTK
- Write an AI to answer questions base on given resources
- AI will select most related text file and search for answer in the file
- Command: $ python questions.py corpus
#### Example
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning , classification and regression.

Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.
