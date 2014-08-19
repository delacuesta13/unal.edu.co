# -*- coding: iso-8859-1 -*-

import numpy as np

__author__ = "Jhon Adrián Cerón Guzmán"
__twitter__ = "jacerong"
__license__ = "GPL"
__version__ = "1.0.0"

TD = np.array([
        [2,3,0,3,7], 
        [0,5,5,0,3], 
        [5,0,7,3,3], 
        [3,1,0,9,9], 
        [0,0,7,1,3], 
        [6,9,4,6,0],
    ], dtype=float)
    
L = np.array([5,2,3,6,4,3])[:,np.newaxis]

# Vector P(D):
# A document is randomly chosen with uniform probability
vector_prob_D = np.ones(TD.shape[1], dtype=float).reshape(1, TD.shape[1]) / TD.shape[1]

# Conditional Probability Matrix of a term given a document P(T|D):
# A term Ti, present in the document Dj, is randomly chosen with a probability
# proportional to the frequency of Ti in Dj.
cond_prob_TD = TD / TD.sum(axis=0)

# Joint Probability P(T,D)=P(T and D):
# P(Ti and Dj)=P(Ti)*P(Dj|Ti)=P(Dj)*P(Ti|Dj)
joint_prob_TD = cond_prob_TD * vector_prob_D

# Vector P(T):
# The term Ti probability is equal to the sum of joint probability of 
# P(Ti and D1) up to P(Ti and Dn)
vector_prob_T = joint_prob_TD.sum(axis=1)[:,np.newaxis]

# Conditional Probability Matrix of a document given a term P(D|T):
# P(Dj|Ti)=P(Dj)P(Ti|Dj)/P(Ti)
cond_prob_DT = (vector_prob_D * cond_prob_TD) / vector_prob_T

# E[l]=l1*P(T1)+...+lm*P(Tm):
# The expected value of the random variable l is equal to the 
# length of a randomly chosen term by its probability.
expected_L = (L * vector_prob_T).sum(axis=0)

# Var(L): Variance of l
variance_l = (np.power(L - expected_L, 2) * vector_prob_T).sum(axis=0)

print "\n"
print "+"*63
print "Assignment 1 Results".center(63,"+")
print "\na. Matrix P(T,D):" 
print joint_prob_TD
print "\nb. Matrix P(T|D):"
print cond_prob_TD
print "\nc. Matrix P(D|T):"
print cond_prob_DT
print "\nd. Vector P(D):"
print vector_prob_D
print "\ne. Vector P(T):"
print vector_prob_T
print "\nf. E[l]=", expected_L[0]
print "\ng. Var(l)=", variance_l[0]
print "+"*63
print "\n"
