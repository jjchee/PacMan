# AI PAC-MAN GAME PLAYING AGENT

Using Artificial Intelligence, we developed a bot that plays Pac-Man. The bot has a 98% win rate and scores 83% more points than a reflex agent, on average. We implemented the minimax decision rule with six features and learned weights obtained from gradient descent.

![Pac-Man UI](https://i.imgur.com/PLyhLSZ.png)

## HOW TO RUN THE APPLICATION

Note: The program requires two modules (numpy and pylab) from the SciPy package to run. The SciPy package can found at https://www.scipy.org/. These are included with Canopy.

### Command Line

python pacman.py -p MinimaxAgent

### Canopy

We suggest that you first run the pacman.py file (as described below) to see the Minimax agent in action.

In Canopy (Windows): Open the pacman.py file in the project folder in Canopy. Right-click in the console window and select ‘Change to Editor Directory’. Then under the Run menu, select Run Configurations > Run Configurations…
Enter the following line into the Arguments field: -p MinimaxAgent. Then press Run File.

A demonstration game will run showing the MinimaxAgent in action. The weights for this agent were determined manually. The game will end and show the agent’s score and other statistics.

Note: On rare occasions the agent will get stuck and take a very long time to finish the game. If this happens we suggest quitting the current game using Run > Restart Kernel and running another game.

## TEAM MEMBERS

Jason Chee
Nicolas Mauthes
Shlomo Nazarian
Mahmood Abuzaina
