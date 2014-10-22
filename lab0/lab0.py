# This is the file you'll use to submit most of Lab 0.

# Certain problems may ask you to modify other files to accomplish a certain
# task. There are also various other files that make the problem set work, and
# generally you will _not_ be expected to modify or even understand this code.
# Don't get bogged down with unnecessary work.


# Section 1: Problem set logistics ___________________________________________

# This is a multiple choice question. You answer by replacing
# the symbol 'fill-me-in' with a number, corresponding to your answer.

# You get to check multiple choice answers using the tester before you
# submit them! So there's no reason to worry about getting them wrong.
# Often, multiple-choice questions will be intended to make sure you have the
# right ideas going into the problem set. Run the tester right after you
# answer them, so that you can make sure you have the right answers.

# What version of Python do we *recommend* (not "require") for this course?
#   1. Python v2.3
#   2. Python v2.5, Python v2.6, or Python v2.7
#   3. Python v3.0
# Fill in your answer in the next line of code ("1", "2", or "3"):

ANSWER_1 = '2'


# Section 2: Programming warmup _____________________________________________

# Problem 2.1: Warm-Up Stretch

def cube(x):
    return x**3

def factorial(x):
    if x < 0:
        raise Exception, "factorial: input must not be negative"
    elif x == 0:
        return 1
    else:
        result = 1
        for i in xrange(1, x + 1):
            result = result * i
        return result

def count_pattern(pattern, lst):
    counter = 0
    for i in xrange(len(lst) - len(pattern) + 1):
        matches = 0
        for j in xrange(len(pattern)):
            if lst[i + j] == pattern[j]:
                if j == len(pattern) - 1:
                    counter += 1
                    matches = 0
                else:
                    matches += 1               
            else:
                matches = 0
                break
    return counter
            

# Problem 2.2: Expression depth

def depth(expr):
    #print expr
    if isinstance(expr, (list, tuple)):
        return checkDepth(expr)
    else:
        return 0

def checkDepth(expr):
    #print "checking", expr
    maxDepth = 0
    for element in expr:
        if isinstance(element, (list, tuple)):
            d = checkDepth(element)
        else:
            d = 0
        if d > maxDepth:
            maxDepth = d
    maxDepth += 1
    #print "depth", maxDepth
    return maxDepth


# Problem 2.3: Tree indexing

def tree_ref(tree, index):
    #print "index", index
    i = 0
    result = tree
    if isinstance(index, (list, tuple)):
        while i < len(index):
            result = result[index[i]]
            i += 1
    else:
        result = result[index]
    return result


# Section 3: Symbolic algebra

# Your solution to this problem doesn't go in this file.
# Instead, you need to modify 'algebra.py' to complete the distributer.

from algebra import Sum, Product, simplify_if_possible
from algebra_utils import distribution, encode_sumprod, decode_sumprod

# Section 4: Survey _________________________________________________________

# Please answer these questions inside the double quotes.

# When did you take 6.01?
WHEN_DID_YOU_TAKE_601 = "Fall 2012"

# How many hours did you spend per 6.01 lab?
HOURS_PER_601_LAB = "6"

# How well did you learn 6.01?
HOW_WELL_I_LEARNED_601 = "Very well"

# How many hours did this lab take?
HOURS = "2"
