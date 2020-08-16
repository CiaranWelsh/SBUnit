from sbunit import TestCase
import tellurium as te
import sys, os


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
