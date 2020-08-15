import unittest

"""
Background information
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
"""


class Backend:
    """
    abstract base class for simulation backends. Backends should
    conform to this interface by inheriting
    from backend and implementing the abstract methods. We will
    provide out of the box backends for tellurium and maybe pycotools.
    We will also document how users can implement their own backends.

    It would be prudent to consider using an ABC https://docs.python.org/3/library/abc.html


    """


class TelluriumBackend(Backend):
    """
    Concrete class of backend ABC. We need to be able to test
    simulation output. Specifically steady states and time series
    simulations. Are there usecases for sensitivities or MCA here?
    """


class SimulationTestSuite(unittest.TestSuite):

    def simulation_definition(self):
        pass

class TimeSeriesTestSuite(SimulationTestSuite):
    pass

class SteadyStateTestSuite(SimulationTestSuite):
    pass

