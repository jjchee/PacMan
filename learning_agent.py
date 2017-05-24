import os, subprocess
from numpy import ones, zeros, loadtxt
from pylab import plot, show, xlabel, ylabel, arange

filename = 'new_training_data.txt'

# Agent args should always be specified last
run_params = 'python pacman.py -p MinimaxAgent -a '

num_games = 50
show_graphics = False
print_chart = True
depth = 3

gd_iterations = 500
learning_rate = .01

def compute_cost(x_values, y_values, weights): # The function for determining cost (error) in the gradient descent function
    m = y_values.size
    predictions = x_values.dot(weights)
    sqErrors = (predictions - y_values)
    J = (1.0 / (2 * m)) * sqErrors.T.dot(sqErrors)
    
    return J # Goal is to minimize the error for function J
    
def gradient_descent(x_values, y_values, weights, learning_rate, gd_iterations): # Finds the set of weights that minimize the error (linear regression)
    m = y_values.size
    J_history = zeros(shape=(gd_iterations, 1))
 
    for i in range(gd_iterations):
        predictions = x_values.dot(weights)
        theta_size = weights.size

        for it in range(theta_size):
            temp = x_values[:, it]
            temp.shape = (m, 1)
            errors_x1 = (predictions - y_values) * temp
            weights[it][0] = weights[it][0] - learning_rate * (1.0 / m) * errors_x1.sum()
        J_history[i, 0] = compute_cost(x_values, y_values, weights)
        
    return weights, J_history

def get_training_data(path, num_weights = 6):
    # Load each line of comma-separated line of data
    data = loadtxt(path, delimiter = ',')
    
    # Load training data into numpy arrays
    x_values = data[:, :num_weights] # Random weights
    y_values = data[:, num_weights] # Game scores
    
    return x_values, y_values

x_values, y_values = get_training_data(filename) # Load the training data

m = y_values.size
y_values.shape = (m, 1)
it = ones(shape=(m, 7))
it[:, 1:7] = x_values

weights = zeros(shape=(7,1))

# Run gradient descent to find optimal weights
weights, J_history = gradient_descent(it, y_values, weights, learning_rate, gd_iterations)

wts = weights[1:]
wts = [a for b in wts for a in b] # Convert numpy array to 1D list

# The arguments (weights) to be passed to the agent constructor
agent_args = 'depth={},w1={},w2={},w3={},w4={},w5={},w6={}'.format(depth, wts[0], wts[1], wts[2], wts[3], wts[4], wts[5])
run_cmd = run_params + agent_args + ' -n ' + str(num_games)

if not show_graphics:
    run_cmd = run_cmd + ' -q'

print run_cmd
out = subprocess.check_output(run_cmd, shell=True) # Run the game
print out

if print_chart: # Print a graph showing the gradient descent
    plot(arange(gd_iterations), J_history)
    xlabel('Iterations')
    ylabel('Cost')
    show()
    