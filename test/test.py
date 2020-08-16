from sbunit import TestCase
import tellurium as te
from functools import reduce
import os
import sys
import pandas as pd
import numpy as np

"""
There will be another layer in the class heirachy that implements 
a set of tests for checking things like no negative and no inf. 
Could also be implemented as mixin methods so users could 
choose which ones to use. Perhaps: 

Duplicate names in reaction ids - static check but more for antiomny than sbml

class TestSimpleModel(TestCase, TestNoNegative, TestNoInf):
    pass

or 

class TestSimpleModel(TestCase, VerificationTestsMixin):
    pass
    
VerificationTestsMixin - contains TestNoNegative, TestNoInf, etc. 
"""


class TelluriumBackendTests(TestCase):
    """
    This is an odd one because this testcase is both tests
    for sbunit and how I intend users to use sbunit.
    The setting up for this test means implementing
    TestCase.

    """
    maxDiff = None  # for comparing long strings

    def model_name(self):
        return "InfinityModel"

    def get_sbml(self):
        return te.antimonyToSBML(
            f"""
            model {self.model_name()}
                r1: -> S1 ; k;
                S1 = 0;
                k = 0.5
            end
            """
        )

    def phrasedml(self) -> str:
        def generate_report_line(task_name, output_variables):
            return "report " + reduce(lambda x, y: f"{task_name}.{x}, {task_name}.{y}",
                                      ["time"] + output_variables)

        if sys.platform == "win32":
            sbml_file = self.sbml_file.replace("\\", "/")
        else:
            sbml_file = self.sbml_file
        return f"""
                model1 = model "{sbml_file}"
                model2 = model model1 with k = 1
                timeseries_def = simulate uniform(0, 100, 10)
                simulate_model1 = run timeseries_def on model1
                simulate_model2 = run timeseries_def on model2
                {generate_report_line("simulate_model1", self.output_varaibles())}
                {generate_report_line("simulate_model2", self.output_varaibles())}
                """

    def working_directory(self):
        return os.path.dirname(__file__)

    def test_get_sedml(self):
        expected = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Created by phraSED-ML version v1.0.10 with libSBML version 5.18.1. -->
<sedML xmlns="http://sed-ml.org/sed-ml/level1/version3" level="1" version="3">
  <listOfSimulations>
    <uniformTimeCourse id="timeseries_def" initialTime="0" outputStartTime="0" outputEndTime="100" numberOfPoints="10">
      <algorithm kisaoID="KISAO:0000019"/>
    </uniformTimeCourse>
  </listOfSimulations>
  <listOfModels>
    <model id="model1" language="urn:sedml:language:sbml.level-3.version-1" source="D:/SBUnit/test/InfinityModel.xml"/>
    <model id="model2" language="urn:sedml:language:sbml.level-3.version-1" source="model1">
      <listOfChanges>
        <changeAttribute target="/sbml:sbml/sbml:model/sbml:listOfParameters/sbml:parameter[@id='k']/@value" newValue="1"/>
      </listOfChanges>
    </model>
  </listOfModels>
  <listOfTasks>
    <task id="simulate_model1" modelReference="model1" simulationReference="timeseries_def"/>
    <task id="simulate_model2" modelReference="model2" simulationReference="timeseries_def"/>
  </listOfTasks>
  <listOfDataGenerators>
    <dataGenerator id="report_0_0_0" name="simulate_model1.time">
      <listOfVariables>
        <variable id="simulate_model1_____time" symbol="urn:sedml:symbol:time" taskReference="simulate_model1"/>
      </listOfVariables>
      <math xmlns="http://www.w3.org/1998/Math/MathML">
        <ci> simulate_model1_____time </ci>
      </math>
    </dataGenerator>
    <dataGenerator id="report_0_0_1" name="simulate_model1.S1">
      <listOfVariables>
        <variable id="simulate_model1_____S1" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" taskReference="simulate_model1" modelReference="model1"/>
      </listOfVariables>
      <math xmlns="http://www.w3.org/1998/Math/MathML">
        <ci> simulate_model1_____S1 </ci>
      </math>
    </dataGenerator>
    <dataGenerator id="report_1_0_0" name="simulate_model2.time">
      <listOfVariables>
        <variable id="simulate_model2_____time" symbol="urn:sedml:symbol:time" taskReference="simulate_model2"/>
      </listOfVariables>
      <math xmlns="http://www.w3.org/1998/Math/MathML">
        <ci> simulate_model2_____time </ci>
      </math>
    </dataGenerator>
    <dataGenerator id="report_1_0_1" name="simulate_model2.S1">
      <listOfVariables>
        <variable id="simulate_model2_____S1" target="/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='S1']" taskReference="simulate_model2" modelReference="model2"/>
      </listOfVariables>
      <math xmlns="http://www.w3.org/1998/Math/MathML">
        <ci> simulate_model2_____S1 </ci>
      </math>
    </dataGenerator>
  </listOfDataGenerators>
  <listOfOutputs>
    <report id="report_0">
      <listOfDataSets>
        <dataSet id="report_0_0_0_dataset" label="simulate_model1.time" dataReference="report_0_0_0"/>
        <dataSet id="report_0_0_1_dataset" label="simulate_model1.S1" dataReference="report_0_0_1"/>
      </listOfDataSets>
    </report>
    <report id="report_1">
      <listOfDataSets>
        <dataSet id="report_1_0_0_dataset" label="simulate_model2.time" dataReference="report_1_0_0"/>
        <dataSet id="report_1_0_1_dataset" label="simulate_model2.S1" dataReference="report_1_0_1"/>
      </listOfDataSets>
    </report>
  </listOfOutputs>
</sedML>
"""
        actual = self.get_sedml()
        self.assertEqual(expected, actual)

    def test_get_sbml(self):
        expected = """<?xml version="1.0" encoding="UTF-8"?>
<!-- Created by libAntimony version v2.12.0 with libSBML version 5.18.1. -->
<sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" level="3" version="1">
  <model metaid="InfinityModel" id="InfinityModel">
    <listOfCompartments>
      <compartment sboTerm="SBO:0000410" id="default_compartment" spatialDimensions="3" size="1" constant="true"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="S1" compartment="default_compartment" initialConcentration="0" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="k" value="0.5" constant="true"/>
    </listOfParameters>
    <listOfReactions>
      <reaction id="r1" reversible="true" fast="false">
        <listOfProducts>
          <speciesReference species="S1" stoichiometry="1" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> k </ci>
          </math>
        </kineticLaw>
      </reaction>
    </listOfReactions>
  </model>
</sbml>
"""
        actual = self.get_sbml()
        print(actual)
        self.assertEqual(expected, actual)

    def test_report_mapping(self):
        expected = {'report_0_0_0_dataset': 'simulate_model1.time', 'report_0_0_1_dataset': 'simulate_model1.S1',
                    'report_1_0_0_dataset': 'simulate_model2.time', 'report_1_0_1_dataset': 'simulate_model2.S1'}
        actual = self.report_mapping()
        self.assertEqual(expected, actual)

    def test_get_list_of_tasks(self):
        actual = self.get_list_of_task_ids()
        self.assertEqual(4, len(actual))

    def test_simulate(self):
        df = self.simulate()
        actual = df["simulate_model1"].loc[10, "S1"]
        expected = 50.0
        self.assertEqual(actual, expected)

    def test_assert_unique(self):
        ser1 = pd.Series([0, 0, 0, 0, 0])
        ser2 = pd.Series([0, 0, 5, 0, 0])
        self.assertTrue(self.assertUnique(ser1))
        self.assertFalse(self.assertUnique(ser2))

    def test_assert_all_equal(self):
        ser1 = pd.Series([0, 0, 0, 0, 0])
        self.assertTrue(self.assertAllEqual(ser1, 0))
        self.assertFalse(self.assertAllEqual(ser1, 5))

    def test_assert_all_greater(self):
        ser2 = pd.Series([1, 1, 1, 1, 1])
        self.assertTrue(self.assertAllGreater(ser2, 0.5))
        self.assertFalse(self.assertAllGreater(ser2, 10))

    def test_assert_all_greater_equal(self):
        ser1 = pd.Series([1, 2, 3, 4, 5])
        self.assertTrue(self.assertAllGreaterEqual(ser1, 0))
        self.assertFalse(self.assertAllGreaterEqual(ser1, 3))
        self.assertTrue(self.assertAllGreaterEqual(ser1, -1))
        self.assertFalse(self.assertAllGreaterEqual(ser1, 5))

    def test_assert_all_less(self):
        ser1 = pd.Series([6, 7, 8, 9])
        self.assertTrue(self.assertAllLess(ser1, 15))
        self.assertFalse(self.assertAllLess(ser1, 5))
        self.assertFalse(self.assertAllLess(ser1, 9))

    def test_assert_all_less_equal(self):
        ser1 = pd.Series([6, 7, 8, 9])
        self.assertTrue(self.assertAllLessEqual(ser1, 15))
        self.assertFalse(self.assertAllLessEqual(ser1, 5))
        self.assertTrue(self.assertAllLessEqual(ser1, 9))

    def test_assert_all_x_greater_y(self):
        ser1 = pd.Series([0, 0, 0, 0, 0])
        ser2 = pd.Series([1, 1, 1, 1, 1])
        self.assertTrue(self.assertAllXGreaterY(ser2, ser1))
        self.assertFalse(self.assertAllXGreaterY(ser1, ser2))

    def test_assert_all_x_less_y(self):
        ser1 = pd.Series([0, 0, 0, 0, 0])
        ser2 = pd.Series([1, 1, 1, 1, 1])
        ser3 = pd.Series([1, 2, 1, 1, 1])
        self.assertTrue(self.assertAllXLessY(ser1, ser2))
        self.assertFalse(self.assertAllXLessY(ser2, ser1))
        self.assertFalse(self.assertAllXLessY(ser3, ser1))

    def test_assert_all_x_greater_equal_y(self):
        ser1 = pd.Series([1, 2, 3, 4, 5])
        ser2 = pd.Series([6, 7, 8, 9, 10])
        ser3 = pd.Series([10, 11, 12, 13, 14])
        self.assertTrue(self.assertAllXGreaterEqualY(ser2, ser1))
        self.assertFalse(self.assertAllXGreaterEqualY(ser1, ser2))
        self.assertTrue(self.assertAllXGreaterEqualY(ser3, ser2))

    def test_assert_all_x_less_equal_y(self):
        ser1 = pd.Series([0, 0, 0, 0, 0])
        ser2 = pd.Series([1, 1, 1, 1, 1])
        ser3 = pd.Series([1, 1, 2, 1, 1])
        self.assertTrue(self.assertAllXLessEqualY(ser1, ser2))
        self.assertFalse(self.assertAllXLessEqualY(ser2, ser1))
        self.assertFalse(self.assertAllXLessEqualY(ser3, ser1))


class SimpleModelTest(TestCase):

    def model_name(self):
        return "SimpleModel"

    def get_sbml(self):
        return te.antimonyToSBML(
            f"""
            model {self.model_name()}
                r1: S1 -> S2 ; k1*S1*Stim;
                r2: S2 -> S1 ; k2*S2;
                Stim = 0;
                S1 = 10;
                S2 = 0;
                k1 = 0.1
                k2 = 0.1
            end
            """
        )

    def phrasedml(self) -> str:
        def generate_report_line(task_name, output_variables):
            s = "report "
            for variable in output_variables:
                s += f"{task_name}.{variable},"
            return s[:-1]

        if sys.platform == "win32":
            sbml_file = self.sbml_file.replace("\\", "/")
        else:
            sbml_file = self.sbml_file
        return f"""
                NoStim = model "{sbml_file}"
                LowStim = model NoStim with Stim = 1
                HighStim = model NoStim with Stim = 10
                timeseries_def = simulate uniform(0, 100, 10)
                NoStim_timeseries = run timeseries_def on NoStim
                LowStim_timeseries = run timeseries_def on LowStim
                HighStim_timeseries = run timeseries_def on HighStim
                {generate_report_line("NoStim_timeseries", self.output_varaibles())}
                {generate_report_line("LowStim_timeseries", self.output_varaibles())}
                {generate_report_line("HighStim_timeseries", self.output_varaibles())}
                """

    def working_directory(self):
        return os.path.dirname(__file__)

    def test_null_condition(self):
        """
        Nothing should happen
        Returns:

        """
        # checks for identical identical values in a column
        self.assertUnique(self.NoStim_timeseries["S1"])

        # checks that all of S2 == 0
        self.assertAllEqual(self.NoStim_timeseries["S2"], 0)

    def test_low_stim(self):
        """
        Stimulate the network with small about of stim
        Returns:

        """

        self.assertAllXGreaterY(self.LowStim_timeseries["S1"], self.NoStim_timeseries["S1"])
        self.assertAllXLessY(self.LowStim_timeseries["S2"], self.NoStim_timeseries["S2"])

    def test_high_stim(self):
        """
        Stimulate the network with small about of stim
        Returns:

        """

        self.assertAllXGreaterY(self.HighStim_timeseries["S1"], self.LowStim_timeseries["S1"])
        self.assertAllXLessY(self.HighStim_timeseries["S2"], self.LowStim_timeseries["S2"])
