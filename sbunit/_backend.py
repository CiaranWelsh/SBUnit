from abc import ABC, abstractmethod
import unittest
import os, sys
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import typing

import tellurium as te
import phrasedml


class BackendBase(unittest.TestCase, ABC):
    """
    An abstract layer that is designed to be subclassed
    by tools (i.e. simulators) that want to use sbunit. This class defines a
    set of methods that must be implemented.

    """

    __members__ = property(lambda self: self.__dir__())

    def __init__(self, methodName='runTest'):
        super().__init__(methodName=methodName)
        self.sbml_file = os.path.join(
            self.working_directory(), f"{self.model_name()}.xml")
        with open(self.sbml_file, "w") as f:
            f.write(self.get_sbml())
        self.data = self.simulate()
        for dataset_name, df in self.data.items():
            setattr(self, dataset_name, df)


    @abstractmethod
    def model_name(self):
        """
        Returns: the name of the model.

        """
        pass

    @abstractmethod
    def get_sbml(self):
        """
        get the sbml string for the model you are testing
        Returns: str sbml

        """
        pass

    @abstractmethod
    def get_sedml(self):
        """
        Returns: the sedml that defines the simulations you are testing

        """
        pass

    @abstractmethod
    def simulate(self):
        """
        Simulate the tasks defined by the sedml.

        Returns: Dict[:py:class:pd.DataFrame] A dictionary mapping
            sedml task names to pandas DataFrames containing the
            simulation data.

        """

    @abstractmethod
    def working_directory(self):
        pass

    def get_list_of_task_ids(self):
        soup = BeautifulSoup(self.get_sedml(), parser="lxml", features="lxml")
        ds = soup.findAll("dataset")
        return [ds[i]["id"] for i in range(len(ds))]
    
    @staticmethod
    def assertUnique(series: pd.Series):
        """
        Test that all values in series are unique

        Returns: true if all values are the same. False otherwise

        """
        assert isinstance(series, pd.Series), f"expected pd.Series but got \"{type(series)}\""
        arr = series.to_numpy()
        return (arr[0] == arr).all()

    @staticmethod
    def assertAllEqual(series: pd.Series, value: typing.Union[int, float]):
        """
        Test that all values in series are unique and have the value "value"

        Returns: true if all values are the same and equal value. False otherwise

        """
        assert isinstance(series, pd.Series), f"expected pd.Series but got \"{type(series)}\""
        assert isinstance(value, (int, float))
        arr = series.to_numpy()
        return np.all(arr == value)

    @staticmethod
    def assertAllGreater(series: pd.Series, value: typing.Union[int, float]):
        """
        Tests that all values in series are greater than value
        Args:
            series: The pandas.Series to test
            value: numeric value

        Returns: True when all values in series are greater than value

        """
        assert isinstance(series, pd.Series), f"expected pd.Series but got \"{type(series)}\""
        assert isinstance(value, (int, float))
        arr = series.to_numpy()
        return np.all(arr > value)

    @staticmethod
    def assertAllGreaterEqual(series: pd.Series, value: typing.Union[int, float]):
        """
        Tests that all values in series are greater than or equal to value
        Args:
            series: The pandas.Series to test
            value: numeric value

        Returns: True when all values in series are greater than or equal value

        """
        assert isinstance(series, pd.Series), f"expected pd.Series but got \"{type(series)}\""
        assert isinstance(value, (int, float))
        arr = series.to_numpy()
        return np.all(arr >= value)

    @staticmethod
    def assertAllLess(series: pd.Series, value: typing.Union[int, float]):
        """
        Tests that all values in series are less than value
        Args:
            series: The pandas.Series to test
            value: numeric value

        Returns: True when all values in series are less than value

        """
        assert isinstance(series, pd.Series), f"expected pd.Series but got \"{type(series)}\""
        assert isinstance(value, (int, float))
        arr = series.to_numpy()
        return np.all(arr < value)

    @staticmethod
    def assertAllLessEqual(series: pd.Series, value: typing.Union[int, float]):
        """
        Tests that all values in series are less than or equal value
        Args:
            series: The pandas.Series to test
            value: numeric value

        Returns: True when all values in series are less than or equal value

        """
        assert isinstance(series, pd.Series), f"expected pd.Series but got \"{type(series)}\""
        assert isinstance(value, (int, float))
        arr = series.to_numpy()
        return np.all(arr <= value)


    @staticmethod
    def assertAllXGreaterY(X: pd.Series, Y: pd.Series):
        """
        Tests that all values in X are greater than all values in Y
        Args:
            X: :py:class:`pd.series`
            Y: :py:class:`pd.series`

        Returns: True when all values in X are greater all values in Y
        """
        assert isinstance(X, pd.Series), f"expected pd.Series for argument \"X\" but got \"{type(X)}\""
        assert isinstance(Y, pd.Series), f"expected pd.Series for argument \"Y\" but got \"{type(Y)}\""
        x = X.to_numpy()
        y = Y.to_numpy()
        return np.all(x > y)

    @staticmethod
    def assertAllXGreaterEqualY(X: pd.Series, Y: pd.Series):
        """
        Tests that all values in X are greater than or equal to all values in Y
        Args:
            X: :py:class:`pd.series`
            Y: :py:class:`pd.series`

        Returns: True when all values in X are greater or equal to all values in Y
        """
        assert isinstance(X, pd.Series), f"expected pd.Series for argument \"X\" but got \"{type(X)}\""
        assert isinstance(Y, pd.Series), f"expected pd.Series for argument \"Y\" but got \"{type(Y)}\""
        x = X.to_numpy()
        y = Y.to_numpy()
        return np.all(x >= y)

    @staticmethod
    def assertAllXLessY(X: pd.Series, Y: pd.Series):
        """
        Tests that all values in X are less than all values in Y
        Args:
            X: :py:class:`pd.series`
            Y: :py:class:`pd.series`

        Returns: True when all values in X are less than all values in Y
        """
        assert isinstance(X, pd.Series), f"expected pd.Series for argument \"X\" but got \"{type(X)}\""
        assert isinstance(Y, pd.Series), f"expected pd.Series for argument \"Y\" but got \"{type(Y)}\""
        x = X.to_numpy()
        y = Y.to_numpy()
        return np.all(x < y)

    @staticmethod
    def assertAllXLessEqualY(X: pd.Series, Y: pd.Series):
        """
        Tests that all values in X are less than or equal to all values in Y
        Args:
            X: :py:class:`pd.series`
            Y: :py:class:`pd.series`

        Returns: True when all values in X are less than or equal to all values in Y
        """
        assert isinstance(X, pd.Series), f"expected pd.Series for argument \"X\" but got \"{type(X)}\""
        assert isinstance(Y, pd.Series), f"expected pd.Series for argument \"Y\" but got \"{type(Y)}\""
        x = X.to_numpy()
        y = Y.to_numpy()
        return np.all(x <= y)








