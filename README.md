Background information
----------------------
A small group of researchers have begal a project called km_test which is going to be a 
unittesting framework for models in systems biology. Instead of contributing directly to 
this project I am starting a new one under the name of SBUnit. The only reason I have 
done so is that km_test is essentially somebodies undergraduate project. I don't think 
its fair to them if I modify their work. 

This is a proof of principle project and its very early days. While this is a python library 
it is likely that future implementations will be C++ in order to port to other languages more 
readily. However, there are complications with this idea - in python we can inherit from unittest, 
in C++ we can internalize and extend gtest, BUT how does this work if we create Python bindings for the
C++ library? Does it mean we need to fully write our own testing framework ? 

Concepts
---------
#. Static analyzer - Is the model broken? A form of verification. 
#. Validation - Does the model do what the user thinks? Runs simulations. Tests for user defined behaviour. 


SEDML
-----
The best way I can see this module working is if we use SEDML to 
encode the simulations. 

Phrasedml should be used for the front end - both of these are already supported 
by tellurium but its important to support the principle of allowing other 
backend simulators. 

Test cases involving simulations will be encoded in sedml via phrasedml. It is up to 
tools to interpret sedml. 

Brainstorming about implementation ideas
----------------------------------------
- Can we make use of the decorator pattern to provide certain tests? 

@test_something
def my_user_defined_function():
    pass

numpy
-----
Numpy should be used to handle all simulation results because it is faster. 



Brainstorming about implementation ideas
----------------------------------------
- Can we make use of the decorator pattern to provide certain tests? 

@test_something
def my_user_defined_function():
    pass
    
    
Static type tests
------------------
- We can check to see which simulators the model will run with? 
    I.e. you might be able to run model stochastically as well as deterministically? 
- Time series has only 1 simulation interval. 
- Time series has too few intervals. 
- Tends to infinity
- Negative values. 


