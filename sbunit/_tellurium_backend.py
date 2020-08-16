from abc import abstractmethod

import pandas as pd
import phrasedml
import tellurium as te
from lxml import etree

from ._backend import BackendBase


class TestCase(BackendBase):

    def __init__(self, methodName="runTest"):
        super().__init__(methodName=methodName)


    @abstractmethod
    def phrasedml(self) -> str:
        """
        simulation definition using phasedml. This method must be user
        defined. Phrasedml is then used to generate a SEDML document.
        Returns: str
        """
        pass

    def get_sedml(self):
        """
        Convert phrasedml into sedml. This method is concrete
        and prevents the need for the user to write their own
        sedml. Instead they provide theiry user input as phrasedml
        which this method automatically converts to sedml
        Returns: str SEDML string

        """
        sedml_str = phrasedml.convertString(self.phrasedml())
        if not sedml_str:
            raise ValueError(phrasedml.getLastError())
        return sedml_str

    def output_varaibles(self):
        return te.loads(self.get_sbml()).getFloatingSpeciesIds()

    def report_mapping(self):
        root = etree.fromstring(self.get_sedml().encode())
        ns = "http://sed-ml.org/sed-ml/level1/version3"
        dct = dict()
        for i in root.xpath("//sedml:dataSet", namespaces = {"sedml": ns}):
            dct[i.attrib["id"]] = i.attrib["label"]
        return dct

    def simulate(self):
        factory = te.sedml.tesedml.SEDMLCodeFactory(
            self.get_sedml(), workingDir=self.working_directory(),
            createOutputs=False,
        )
        results = factory.executePython()
        sim_data = results["dataGenerators"]
        sim_data = {self.report_mapping()[k+"_dataset"]: v for k, v in sim_data.items()}

        simulations_list = list(set([i.split(".")[0] for i in sim_data.keys()]))
        df_dct = {}
        for simulation_id in simulations_list:
            series_list = []
            for label, data in sim_data.items():
                simulation_id2, variable = label.split(".")
                if simulation_id == simulation_id2:
                    ser = pd.Series(data.flatten(), name=variable)
                    series_list.append(ser)
            df_dct[simulation_id] = pd.concat(series_list, axis=1)
        return df_dct






















