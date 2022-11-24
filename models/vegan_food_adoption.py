from mesa import Model, DataCollector
from mesa.time import RandomActivation
from mesa.space import NetworkGrid
from networkx import erdos_renyi_graph
from agents.person import Person


class VeganFoodAdoptionModel(Model):

    def __init__(self, N, average_friend_count_per_person):
        self.person_count = N
        self.average_friend_count_per_person = average_friend_count_per_person
        self.schedule = RandomActivation(model=self)
        self.setup_network_grid()

        self.behavior_names = ['eat_real_meat',
                               'eat_vegan_meat']

        for i, network_node_id in enumerate(self.network_graph.nodes()):
            person = Person(unique_id=i, model=self,
                            behavior_names=self.behavior_names)
            self.schedule.add(person)
            self.grid.place_agent(agent=person, node_id=network_node_id)

        self.datacollector = DataCollector(
            agent_reporters=self.create_agent_reporters())

    def create_agent_reporters(self):
        return self.create_agent_reporters_for_behavior_counts() | self.create_agent_reporters_for_behavioral_attitudes() | self.create_agent_reporters_for_behavioral_intentions() | self.create_agent_reporters_for_subjective_norms() | self.create_agent_reporters_for_friend_ids()

    def create_agent_reporters_for_behavior_counts(self):
        def get_behavior_count_lambda(behavior_name: str):
            return lambda person: person.get_behavior_count(behavior_name=behavior_name)

        return {"behavior_count_" + behavior_name: get_behavior_count_lambda(behavior_name=behavior_name) for behavior_name in self.behavior_names}

    def create_agent_reporters_for_behavioral_intentions(self):
        def get_behavioral_intention_lambda(behavior_name: str):
            return lambda person: person.get_behavioral_intention(behavior_name=behavior_name)

        return {"behavioral_intention_" + behavior_name: get_behavioral_intention_lambda(behavior_name=behavior_name) for behavior_name in self.behavior_names}

    def create_agent_reporters_for_behavioral_attitudes(self):
        def get_behavioral_attitude_lambda(behavior_name: str):
            return lambda person: person.get_behavioral_attitude(behavior_name=behavior_name)

        return {"behavioral_attitude_" + behavior_name: get_behavioral_attitude_lambda(behavior_name=behavior_name) for behavior_name in self.behavior_names}

    def create_agent_reporters_for_subjective_norms(self):
        def get_subjective_norms_lambda(behavior_name: str):
            return lambda person: person.get_subjective_norm(behavior_name=behavior_name)

        return {"subjective_norm_" + behavior_name: get_subjective_norms_lambda(behavior_name=behavior_name) for behavior_name in self.behavior_names}

    def create_agent_reporters_for_friend_ids(self):
        return {"friend_ids": lambda person: "-".join([str(friend_id) for friend_id in sorted(person.get_friend_ids())])}

    def setup_network_grid(self):
        network_edge_probability = self.average_friend_count_per_person / self.person_count
        self.network_graph = erdos_renyi_graph(
            n=self.person_count, p=network_edge_probability)
        self.grid = NetworkGrid(self.network_graph)

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
