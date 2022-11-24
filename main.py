from models.vegan_food_adoption import VeganFoodAdoptionModel
from datetime import datetime

PEOPLE_COUNT: int = 10
AVERAGE_FRIENDS_PER_PERSON: int = 5
TIME_STEPS: int = 100

if __name__ == '__main__':
    model = VeganFoodAdoptionModel(
        N=PEOPLE_COUNT, average_friend_count_per_person=AVERAGE_FRIENDS_PER_PERSON)
    for i in range(TIME_STEPS):
        model.step()
        df = model.datacollector.get_agent_vars_dataframe()
        print(df)
    filepath: str = "data/output" + datetime.utcnow().strftime("%Y-%m-%d-%H%MZ") + ".csv"
    df.to_csv(path_or_buf=filepath, sep=",")
