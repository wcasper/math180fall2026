---
layout: page
title: Task 4
permalink: /inclass/task4
---



# Problem 1

Suppose you are conducting an experiment consisting of replaying the first roll of a round of Ready Set Bet.
* (a) What is the sample space?
* (b) What is the probability of each member of the sample space?
* (c) What is the expected position of every horse after the first roll?


# Problem 2
Suppose you are conducting an experiment consisting of replaying the first two rolls of a round of Ready Set Bet.
* (a) What is the sample space?
* (b) What is the probability of each member of the sample space?
* (c) What is the expected position of every horse after the second roll?

# Problem 3

Upload the Jupyter notebook
* [ReadySetBet.ipynb](python/ReadySetBet.ipynb)
to [Google Collab](https://colab.research.google.com/).
Then run all the fields to calculate the probability that each horse will win, place or show.

* (a) Write down the table of probabilities that the code obtained in a table, like the one below

|Horse        | 2/3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11/12 |
| ----------- | --- | - | - | - | - | - | - | -  | ----- |
| Win Prob.   |     |   |   |   |   |   |   |    |       |
| Place Prob. |     |   |   |   |   |   |   |    |       |
| Show Prob.  |     |   |   |   |   |   |   |    |       |
| ----------- | --- | - | - | - | - | - | - | -  | ----- |

* (b) If you were to place the $$5$$ token at the beginning of the game, before any horses move, what is the best position to put it in?  What is the expectation value of a bet there?  How does this expectation change if you instead place the $$2$$ token?
* (c) If you were to place the $$5$$ token and the $$4$$ token at the beginning of the game, before any horses move, what is the best position to put them in?
* (d) Suppose you wait until a few turns after which the $$11/12$$ horse is at the $$5$$'th position, both red horses are at the first position, the $$7$$ horse is at the first position, and all other horses are at the starting line.  How do the probabilities change?  Run a modified version of the code, and update the table.
* (e) At this stage of the game, what is the best place to put your $$5$$ token?  What is the expectation value of a bet there?

# Problem 4

As a group, come up with a question about Ready Set Bet that you can try to answer by playing (or simulating) a number of games.

For example, it might be "How long should I wait until I place my first bet?" or "How many rolls does it take on average before the game finishes?" or "On average, how far ahead is the first place horse from the second place horse?" or "What is the average position of each horse at the end of a race?"

* Think of a strategy you can use to answer the question.
* If you were playing a bunch of games, what data would you measure?
* After you make these measurements, what analysis do you need to perform to get your final answer?
* Can you modify the simulation code to measure this?  (If not, ask for help!)
* After running the simulation, what was the result?  Was it predictable or surprising?



