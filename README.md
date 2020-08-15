Background information
----------------------
I've started a new repository because I don't want to tread on somebodies undergraduate project. 

This will eventually be a C++ library with ports to other languages but for now its a python library. 

We use unittest as a base. In C++, we will use Gtest. 







Brainstorming about implementation ideas
----------------------------------------
- Can we make use of the decorator pattern to provide certain tests? 

@test_something
def my_user_defined_function():
    pass

SEDML
-----
The best way I can see this module working is if we use SEDML to 
encode the simulations. 

Phrasedml should be used for the front end - both of these are already supported 
by tellurium but its important to support the principle of allowing other 
backend simulators. 

Test cases involving simulations will be encoded in sedml via phrasedml. It is up to 
tools to interpret sedml. 