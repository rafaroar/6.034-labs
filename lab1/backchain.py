from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):

    #print "\n", "HYPOTHESIS", hypothesis
    
    new_hypothesis = []
    variable = ""
    for rule in rules:
        for cons in rule.consequent():
            if match(cons, hypothesis) != None:
                new_hypothesis.append(rule.antecedent())
                variable = match(cons, hypothesis)
                #print "match!", cons, rule.antecedent()
                #print "variable", variable
                
    #print "new hypothesis", new_hypothesis

    if len(new_hypothesis) < 1:
        return hypothesis

    branches = [hypothesis]
    
    for antec in new_hypothesis:
        expr = populate(antec, variable)
        #print antec, variable, populate(antec, variable)
        
        if isinstance (expr, str):
            minitree = backchain_to_goal_tree(rules, expr)
            
        else:
            branchez = []
            for argg in expr:
                branchez.append(backchain_to_goal_tree(rules, argg))
            if isinstance (expr, OR):
                minitree = simplify(OR(branchez))
            elif isinstance (expr, AND):
                minitree = simplify(AND(branchez))
                
        branches.append(minitree)

    #print "  TREE", branches
    tree = simplify(OR(branches))

    return tree

# Here's an example of running the backward chainer - uncomment
# it to see it work:
# print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
