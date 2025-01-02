import random
import networkx as nx
import numpy as np
from typing import Generator, Callable

class AgentModel:
    def __init__(self):
        """Initializes the AgentModel with default parameters and an uninitialized graph."""
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
        """Takes a dictionary of the form {parameter: value} to update the parameters of the model.

        Args:
            parameters (dict): A dictionary where keys are parameter names and values are the updated values.
        """
        self.__parameters.update(parameters)

    def delete_parameters(self, parameters: list = None) -> None:
        """Deletes specified parameter keys from the model's parameters or resets them to defaults if no parameters are specified.

        Args:
            parameters (list, optional): List of parameter keys to delete. Defaults to None.

        Raises:
            KeyError: If a default or non-existent parameter is passed in.

        Returns:
            bool: True if the deletion was successful.
        """
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
        """Returns a list of all the model's parameter keys.

        Returns:
            list: A list of parameter names.
        """
        return list(self.__parameters.keys())

    def change_max_timesteps(self, timesteps: int):
        """Changes the maximum number of timesteps for the model.

        Args:
            timesteps (int): The new maximum number of timesteps.
        """
        self.__MAX_TIMESTEPS = timesteps

    def __getitem__(self, parameter):
        """Gets the value of a parameter by key.

        Args:
            parameter (str): The parameter key.

        Returns:
            The value of the specified parameter.
        """
        return self.__parameters[parameter]

    def __setitem__(self, parameter, value):
        """Sets the value of a parameter by key.

        Args:
            parameter (str): The parameter key.
            value: The new value to set.
        """
        self.__parameters[parameter] = value

    def set_graph(self, graph: nx.Graph):
        """Sets the graph object for the model.

        Args:
            graph (nx.Graph): A networkx graph object.

        Raises:
            Exception: If the provided parameter is not a graph object.
        """
        if graph and not isinstance(graph, nx.Graph):
            raise Exception("The passed parameter is not a graph object.")
        self.__graph = graph

    def get_graph(self):
        """Returns the networkx graph object representing the model's current graphical state.

        Returns:
            nx.Graph: The current graph object.
        """
        return self.__graph

    def set_initial_data_function(self, initial_data_function: Callable):
        """Sets the function that the model will use to generate initial data.

        Args:
            initial_data_function (Callable): A function that generates initial data for nodes.
        """
        self.initial_data_function = initial_data_function

    def set_timestep_function(self, timestep_function: Callable):
        """Sets the function that the model will use to execute timesteps.

        Args:
            timestep_function (Callable): A function that processes a timestep for the model.
        """
        self.timestep_function = timestep_function

    def initialize_graph(self):
        """Initializes the graph and its nodes using the specified initial_data_function.

        Raises:
            Exception: If initial_data_function is not set.
        """
        num_nodes = self["num_nodes"]
        graph_type = self["graph_type"]

        if graph_type == "complete":
            self.__graph = nx.complete_graph(num_nodes)
        elif graph_type == "cycle":
            self.__graph = nx.cycle_graph(num_nodes)
        else:
            self.__graph = nx.wheel_graph(num_nodes)

        if not self.initial_data_function:
            raise Exception("Initial data function is not set.")

        for node in self.__graph.nodes():
            initial_data = self.initial_data_function(self)
            self.__graph.nodes[node].update(initial_data)

    def timestep(self):
        """Executes one timestep of the model by applying the timestep_function.

        Raises:
            Exception: If timestep_function is not set.
        """
        if not self.timestep_function:
            raise Exception("Timestep function is not set.")
        self.timestep_function(self)

    def run_to_convergence(self):
        """Runs timesteps until convergence or the maximum number of timesteps is reached.

        Raises:
            Exception: If convergence_data_key is not specified.

        Returns:
            int: The timestep at which the model converged.
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
        """Checks whether a specified data_key variable has converged within the given standard deviation.

        Args:
            data_key (str): The key of the data to check for convergence.
            std_dev (float): The threshold standard deviation for convergence.

        Returns:
            bool: True if the model has converged, False otherwise.
        """
        nodes = np.array(
            [node_data[data_key] for _, node_data in self.__graph.nodes(data=True)]
        )
        print(nodes.std())
        return nodes.std() <= std_dev


def genInitialData(model: AgentModel):
    """Generates initial data for a node.

    Args:
        model (AgentModel): The model instance.

    Returns:
        dict: Initial data for the node.
    """
    return {"id": random.randint(1, 100)}


def genTimestepData(model: AgentModel, nodeData: dict):
    """Generates data for a node during a timestep.

    Args:
        model (AgentModel): The model instance.
        nodeData (dict): Current data of the node.

    Returns:
        dict: Updated data for the node.
    """
    nodeData["id"] = nodeData["id"] + 1
    return nodeData