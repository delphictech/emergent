import random
import networkx as nx
import numpy as np
from typing import Generator, Callable


class AgentModel:
    def __init__(self):
        self.__parameters = {
            "num_nodes": 3,
            "graph_type": "complete",
            "convergence_data_key": None,
            "convergence_std_dev": 100,
        }
        self.__graph: nx.Graph = None
        self.initial_data_function = None
        self.timestep_function = None
        self.__MAX_TIMESTEPS = 100000

    def update_parameters(self, parameters: dict) -> None:
        """Takes a dictionary of the form {parameter: value} to update the parameters of the model."""
        self.__parameters.update(parameters)

    def delete_parameters(self, parameters: list = None) -> None:
        """Takes a list of parameter keys and deletes each key from the parameters dictionary.
        If no parameters are passed in, then this method will reset the model's parameters to its defaults.
        If a default parameter or non-existent parameter is passed in, this method will raise an exception.
        Returns true if the deletion was successful."""
        if not parameters:
            self.__parameters = {
                "num_nodes": 3,
                "graph_type": "complete",
                "convergence_data_key": None,
                "convergence_std_dev": 100,
            }
            return True

        for param in parameters:
            if param not in self.__parameters or param in {
                "num_nodes",
                "graph_type",
                "convergence_data_key",
                "convergence_std_dev",
            }:
                raise KeyError
            self.__parameters.pop(param)
        return True

    def list_parameters(self) -> list:
        """Returns a list of all the model's parameter keys."""
        return list(self.__parameters.keys())

    def change_max_timesteps(self, timesteps: int):
        self.__MAX_TIMESTEPS = timesteps

    def __getitem__(self, parameter):
        return self.__parameters[parameter]

    def __setitem__(self, parameter, value):
        self.__parameters[parameter] = value

    def set_graph(self, graph: nx.Graph):
        if graph and not isinstance(graph, nx.Graph):
            raise Exception("The passed parameter is not a graph object.")
        self.__graph = graph

    def get_graph(self):
        """Returns the networkx graph object representing the model's current graphical state."""
        return self.__graph

    def set_initial_data_function(self, initial_data_function: Callable):
        """Sets the function that the model will use to generate initial data."""
        self.initial_data_function = initial_data_function

    def set_timestep_function(self, timestep_function: Callable):
        """Sets the function that the model will use to timestep."""
        self.timestep_function = timestep_function

    def initialize_graph(self):
        """Initializes each node in the graph using the specified initial_data_function."""
        num_nodes = self["num_nodes"]
        graph_type = self["graph_type"]

        if graph_type == "complete":
            self.__graph = nx.complete_graph(num_nodes)
        elif graph_type == "cycle":
            self.__graph = nx.cycle_graph(num_nodes)
        else:
            self.__graph = nx.wheel_graph(num_nodes)

        for node in self.__graph.nodes():
            initial_data = self.initial_data_function(self)
            self.__graph.nodes[node].update(initial_data)

    def timestep(self):
        """Runs one timestep of the model, mutating the model by passing it to the user's specified timestep_generator function."""
        self.timestep_function(self)

    def run_to_convergence(self):
        """Timesteps the model until time == MAX_TIMESTEPS or the specified convergence_data_key variable
        has converged to within the specified convergence_std_dev for all nodes. Returns the timestep t of convergence.
        """
        time = 0
        data_key, std_dev = self["convergence_data_key"], self["convergence_std_dev"]

        if not data_key:
            raise Exception("No convergence data key specified")
        print("Before convergence:", self.__graph.nodes(data=True))
        while time < self.__MAX_TIMESTEPS and not self.is_converged(data_key, std_dev):
            self.timestep()
            time += 1
            print(
                f"After convergence at time t == {time}:", self.__graph.nodes(data=True)
            )
        return time

    def is_converged(self, data_key: str, std_dev: float):
        """Checks whether the specified data_key variable has converged to within the specified std_dev for all nodes.
        Returns true if the model has converged, and false if not."""
        nodes = np.array(
            [node_data[data_key] for _, node_data in self.__graph.nodes(data=True)]
        )
        print(nodes.std())
        return nodes.std() <= std_dev


def genInitialData(model: AgentModel):
    return {"id": random.randint(1, 100)}


def genTimestepData(model: AgentModel, nodeData: dict):
    nodeData["id"] = nodeData["id"] + 1
    return nodeData
