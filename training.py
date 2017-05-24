import random, subprocess, re

output_filename = 'new_training_data.txt'
# Agent args should always be specified last
run_params = 'python pacman.py -p MinimaxAgent -q -a '

num_runs = 2000
rand_range = (-4., 4.)

def run_training(wts):
    # The arguments (weights) to be passed to the agent constructor
    agent_args = 'w1={},w2={},w3={},w4={},w5={},w6={}'.format(wts[0], wts[1], wts[2], wts[3], wts[4], wts[5])
    run_cmd = run_params + agent_args

    out = subprocess.check_output(run_cmd) # Run the game
    
    search_key = 'Average Score: (.+?)\n'
    avg_score = float(re.findall(search_key, out)[0]) # Find the avg score by regex search in output
    
    return avg_score
    
weights = [1, 0, 0, 0, 0, 0]

for i in range(0, num_runs): # Run the game with random weights for specified num of runs
    print 'Currently running game #' + str(i + 1)
    
    w1 = random.uniform(rand_range[0], rand_range[1])
    w2 = random.uniform(rand_range[0], rand_range[1])
    w3 = random.uniform(rand_range[0], rand_range[1])
    w4 = random.uniform(rand_range[0], rand_range[1])
    w5 = random.uniform(rand_range[0], rand_range[1])
    w6 = random.uniform(rand_range[0], rand_range[1])

    weights = [w1, w2, w3, w4, w5, w6]
    game_score = run_training(weights)
    
    output_str = str(weights).strip('[').strip(']') + ', ' + str(game_score) + '\n'
    
    # Add the line to the file
    try:
        f = open(output_filename, 'a')
        f.write(output_str)
    finally:
        f.close()

    print 'Added line: ' + output_str