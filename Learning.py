import subprocess, re, random
import multiAgents

# this script generates a training set of pacman runs. 
# it randomly generates a coefficient between -4 and 4 
# for each feature. 

destfile = "output.txt"
def runPacman(c):
    "runs pacman with the given constants, returns the score #"
    # the coefficients are sent in as additional arguments to the eval
    # function
    betterArg = "evalFn=better,a={},b={},c={},d={},e={},f={}".format(c[0], c[1], c[2], c[3], c[4], c[5])
    output = subprocess.check_output(["python", "pacman.py", "-l", "smallClassic", "-p", "MinimaxAgent", "-a", betterArg, "-n", "1", "-q"])
    # regex = "Pacman emerges victorious! Score: (.+?)\n "
    # winningScores =  map(int,re.findall(regex, output))
    # if winningScores:
    #     averageWinningScore = sum(winningScores)/len(winningScores)
    # else:
    #     averageWinningScore = 0
    # return averageWinningScore
    regex = "Average Score: (.+?)\n"
    averageScore = float(re.findall(regex, output)[0])
    return averageScore

def saveScore(constants, score):
    line = str(tuple(constants)).strip(")").strip("(") + str(score) + "\n"
    with open(destfile, 'a') as outfile:
        outfile.write(line)

constants = [1, 0, 0, 0, 0, 0]

# score = runPacman(constants)
# saveScore(constants, score)

#runPacman(constants)
i = 0
while i < 1:
    multiAgents.w1 = random.uniform(1.0, 1.5)
    multiAgents.w2 = random.uniform(-1.0, -30.0)
    multiAgents.w3 = random.uniform(-0.1, -5.0)
    multiAgents.w4 = random.uniform(-0.1, -5.0)
    multiAgents.w5 = random.uniform(-0.1, -5.0)
    multiAgents.w6 = random.uniform(-0.1, -5.0)
    constants = [multiAgents.w1, multiAgents.w2, multiAgents.w3, multiAgents.w4, multiAgents.w5, multiAgents.w6]
    score = runPacman(constants)
    saveScore(constants, score)
    i = 1+i

#i = 0
#while i < 1:
#    multiAgents.w1 = 1
#    multiAgents.w2 = -20
#    multiAgents.w3 = -4
#    multiAgents.w4 = -1.5
#    multiAgents.w5 = -2
#    multiAgents.w6 = -2
#    constants = [multiAgents.w1, multiAgents.w2, multiAgents.w3, multiAgents.w4, multiAgents.w5, multiAgents.w6]
#    score = runPacman(constants)
#    saveScore(constants, score)
#    i = 1+i