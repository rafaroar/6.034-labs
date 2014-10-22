from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    X = state.get_current_variable()
    if not X:
        return True
    
    x = X.get_assigned_value()
    #i = 0
    constraints = state.get_constraints_by_name(X.get_name())
    
    for i in xrange(len(constraints)):
        constraint = constraints[i]
        #i += 1
        tempX = constraint.get_variable_i_name()
        tempY = constraint.get_variable_j_name()
        
        if tempX == X.get_name():
            Y = tempY
        else:
            Y = tempX
            
        Y = state.get_variable_by_name(Y)
        
        for y in Y.get_domain():
            if not constraint.check(state, x, y):
                Y.reduce_domain(y)
                
        if not Y.get_domain():
            return False

    return True
    # Add your forward checking logic here.
    
    #raise NotImplementedError

# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    singleton_queue = []
    
    for v in state.get_all_variables():
        if len(v.get_domain()) == 1:
             singleton_queue.append(v)

    visited_singletons = {}
    
    while singleton_queue:
        X = singleton_queue.pop()
        visited_singletons[X] = True
        x = X.get_domain()[0]
        
        for constraint in state.get_constraints_by_name(X.get_name()):
            if constraint.get_variable_j_name() == X.get_name():
                Y = constraint.get_variable_i_name()
            else:
                Y = constraint.get_variable_j_name()
                
            Y = state.get_variable_by_name(Y)
            
            for y in Y.get_domain():
                if not constraint.check(state, x, y):
                    Y.reduce_domain(y)
                    
 #           new_domain_length = len(Y.get_domain())
            if len(Y.get_domain()) <= 0:
                return False
            elif len(Y.get_domain()) <= 1 and Y not in visited_singletons:
                singleton_queue.append(Y)
                
    return True

    #raise NotImplementedError

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 1), senate_group1, senate_group2, verbose=1)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    dist = 0
    for i in xrange(len(list1)):
        dist += (list1[i] - list2[i])**2
        
    return dist**(0.5)

    #return hamming_distance(list1, list2)

#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 1), senate_group1, senate_group2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(euclidean_distance, 5)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print CongressIDTree(senate_people, senate_votes, homogeneous_disorder)

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def compute_log(data, length):
	if homogeneous_value(data):
		return 0

	groups = {}	
	for point in data:
		if point in groups:
			groups[point] += 1
		else:
			groups[point] = 1

	total = 0
	for point, count in groups.iteritems():
		prob = float(count)/length
		total += -prob * math.log(prob, 2)
	
	return total
    

def information_disorder(yes, no):
    
    n_yes = float(len(yes))
    n_no = float(len(no))
    n = n_yes + n_no
    
    return (n_yes/n)*compute_log(yes, n_yes) + (n_no/n)*compute_log(no, n_no)

#yay desorder reduced
#print CongressIDTree(senate_people, senate_votes, information_disorder)
#evaluate(idtree_maker(senate_votes, homogeneous_disorder), senate_group1, senate_group2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = False):
    house_limited, house_limited_votes = limit_votes(house_people,
    house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print "ID tree for first group:"
        print CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder)
        print
        print "ID tree for second group:"
        print CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder)
        print
        
    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2)

                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 44
rep_classified = limited_house_classifier(house_people, house_votes, N_1)
#print 'rep_classified', rep_classified

## Find a value of n that classifies at least 90 senators correctly.
N_2 = 67
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2)
#print 'senator_classified', senator_classified

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3)
#print 'old_senator_classified', old_senator_classified

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = "3"
WHAT_I_FOUND_INTERESTING = "I liked the forward checking and the singleton"
WHAT_I_FOUND_BORING = "I didn't like the stuff with the information disorder"


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception, "Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn

    
