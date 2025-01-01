import unittest
import random
import numpy as np

from modelpy.main import AgentModel, MAX_TIMESTEPS


def genInitialZollmanData():
    initial_data = {
        "a_alpha": random.randint(1, 4),
        "a_beta": random.randint(1, 4),
        "b_alpha": random.randint(1, 4),
        "b_beta": random.randint(1, 4),
    }
    expectations = {
        "a_expectation": initial_data["a_alpha"]
        / (initial_data["a_alpha"] + initial_data["a_beta"]),
        "b_expectation": initial_data["b_alpha"]
        / (initial_data["b_alpha"] + initial_data["b_beta"]),
    }
    initial_data.update(expectations)
    return initial_data


def timestepFunction(model: AgentModel):
    graph = model.get_graph()

    for _node, node_data in graph.nodes(data=True):
        # agent pulls the "a" bandit arm
        if node_data["a_expectation"] > node_data["b_expectation"]:
            node_data["a_alpha"] += int(
                np.random.binomial(model["num_trials"], model["a_objective"], size=None)
            )
            node_data["a_beta"] += model["num_trials"]
            node_data["a_expectation"] = node_data["a_alpha"] / (
                node_data["a_alpha"] + node_data["a_beta"]
            )

        # agent pulls the "b" bandit arm
        else:
            node_data["b_alpha"] += int(
                np.random.binomial(model["num_trials"], model["b_objective"], size=None)
            )
            node_data["b_beta"] += model["num_trials"]
            node_data["b_expectation"] = node_data["b_alpha"] / (
                node_data["b_alpha"] + node_data["b_beta"]
            )

    model.set_graph(graph)


class testAgentModelPackage(unittest.TestCase):
    def testInit(self):
        """Test that the parameters of the AgentModel upon initialization are the same as Kekoa's ZollmanBandit."""
        agent = AgentModel()
        zollmanParameters = {
            "num_nodes": 3,
            "graph_type": "complete",
            "a_objective": 0.49,
            "b_objective": 0.51,
            "num_trials": 1,
        }
        self.assertIsInstance(agent, AgentModel)
        agent.update_parameters(
            {"a_objective": 0.49, "b_objective": 0.51, "num_trials": 1}
        )
        for parameter in agent.list_parameters():
            if parameter not in {"convergence_data_key", "convergence_std_dev"}:
                self.assertEqual(zollmanParameters[parameter], agent[parameter])

    def testParameterMethods(self):
        agent = AgentModel()
        self.assertListEqual(
            ["num_nodes", "graph_type", "convergence_data_key", "convergence_std_dev"],
            agent.list_parameters(),
        )
        self.assertEqual(agent["num_nodes"], 3)

    def testInitializeGraph(self):
        agent = AgentModel()
        agent.update_parameters(
            {"a_objective": 0.49, "b_objective": 0.51, "num_trials": 1}
        )
        agent.set_initial_data_function(genInitialZollmanData)
        agent.initialize_graph()
        graph_nodes = list(agent.get_graph().nodes)
        self.assertEqual(graph_nodes, [0, 1, 2])
        for _node, node_data in agent.get_graph().nodes(data=True):
            self.assertTrue(max(node_data.values()) <= 4, msg=node_data)
            self.assertTrue(min(node_data.values()) >= 0, msg=node_data)

    def testTimestep(self):
        agent = AgentModel()
        agent.update_parameters(
            {"a_objective": 0.49, "b_objective": 0.51, "num_trials": 1}
        )
        agent.set_initial_data_function(genInitialZollmanData)
        agent.initialize_graph()
        agent.set_timestep_function(timestepFunction)
        print("Before timestep:", agent.get_graph().nodes(data=True))
        agent.timestep()
        print("After timestep:", agent.get_graph().nodes(data=True))

    def testConvergence(self):
        agent = AgentModel()
        agent.update_parameters(
            {"a_objective": 0.49, "b_objective": 0.51, "num_trials": 1}
        )
        agent.set_initial_data_function(genInitialZollmanData)
        agent.initialize_graph()
        agent.set_timestep_function(timestepFunction)
        agent["convergence_data_key"] = "a_expectation"
        agent["convergence_std_dev"] = 0.05
        time = agent.run_to_convergence()
        self.assertTrue(time <= MAX_TIMESTEPS)


if __name__ == "__main__":
    unittest.main()
