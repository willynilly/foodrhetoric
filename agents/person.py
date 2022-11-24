from __future__ import annotations

import mesa
import random
import statistics


class Person(mesa.Agent):

    """ Person whose behaviors depend on behavioral intentions, behavioral attitudes, and subjective norms. """

    def __init__(self, unique_id, model, behavior_names: list[str]):
        super().__init__(unique_id=unique_id, model=model)
        self.behavior_names = behavior_names
        self.behavioral_attitudes = {}
        self.subjective_norms = {}
        self.behavioral_intentions = {}
        self.behavior_counts = {}
        self.randomize_behavioral_attitudes(behavior_names=self.behavior_names)

    def randomize_behavioral_attitudes(self, behavior_names: list[str]):
        self.behavioral_attitudes = {
            behavior_name: random.random() for behavior_name in behavior_names}

    def update_subjective_norms(self, behavior_names: list[str], other_people: list[Person]):
        self.subjective_norms = {behavior_name: self.get_mean_behavioral_attitude_of_other_people(
            behavior_name=behavior_name, other_people=other_people) for behavior_name in behavior_names}

    def get_mean_behavioral_attitude_of_other_people(self, behavior_name: str, other_people: list[Person]):
        if len(other_people) == 0:
            # if the person has no other people, then they use their own behavioral attitude
            return self.behavioral_attitudes[behavior_name]
        return statistics.mean([other_person.behavioral_attitudes[behavior_name] for other_person in other_people])

    def update_behavioral_intentions(self, behavior_names: list[str], behavioral_attitudes: dict[str, float], subjective_norms: dict[str. float]):
        self.behavioral_intentions = {behavior_name: statistics.mean([
            behavioral_attitudes[behavior_name], subjective_norms[behavior_name]]) for behavior_name in behavior_names}

    def update_behavior_counts(self, behavior_names: list[str], behavioral_intentions: dict[str, float]):
        for behavior_name in behavior_names:
            did_behavior = random.random(
            ) >= behavioral_intentions[behavior_name]
            if did_behavior:
                self.behavior_counts[behavior_name] = self.get_behavior_count(
                    behavior_name=behavior_name) + 1

    def get_behavior_count(self, behavior_name: str):
        if behavior_name not in self.behavior_counts:
            return 0
        else:
            return self.behavior_counts[behavior_name]

    def get_behavioral_attitude(self, behavior_name: str):
        if behavior_name not in self.behavioral_attitudes:
            return 0
        else:
            return self.behavioral_attitudes[behavior_name]

    def get_behavioral_intention(self, behavior_name: str):
        if behavior_name not in self.behavioral_intentions:
            return 0
        else:
            return self.behavioral_intentions[behavior_name]

    def get_subjective_norm(self, behavior_name: str):
        if behavior_name not in self.subjective_norms:
            return 0
        else:
            return self.subjective_norms[behavior_name]

    def get_friend_ids(self):
        friend_ids: list[int] = self.model.grid.get_neighbors(
            self.pos, include_center=False)
        return friend_ids

    def get_friends(self):
        friend_ids: list[int] = self.get_friend_ids()
        friends = [
            agent for agent in self.model.schedule.agents if agent.unique_id in friend_ids]
        return friends

    def step(self):

        self.update_subjective_norms(
            behavior_names=self.behavior_names, other_people=self.get_friends())
        self.update_behavioral_intentions(
            behavior_names=self.behavior_names, behavioral_attitudes=self.behavioral_attitudes, subjective_norms=self.subjective_norms)
        self.update_behavior_counts(
            behavior_names=self.behavior_names, behavioral_intentions=self.behavioral_intentions)
