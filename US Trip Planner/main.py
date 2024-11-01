from crewai import Crew, Agent, Task
from crewai_tools import PDFSearchTool, CSVSearchTool
import os

key_file = open("./Us Trip Planner/api_key", "r")
api_key = key_file.read()

os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

#tools
top_attractions = PDFSearchTool(pdf = "./US Trip Planner/top_100_attractions.pdf")
travel_guide = PDFSearchTool(pdf = "./US Trip Planner/travel_guide_usa.pdf")

criteria_organizer = Agent(
    role = "Criteria Organizer",
    goal = "Organize information from requests to be easy to understand",
    backstory = "You are an organizer that breaks down requests into a clear and concise list of requirements",
    verbose = True,
)

national_rep = Agent(
    role = "State Selector",
    goal = "You need to pick out states that are relevant to the criteria.",
    backstory = "You are a travel representative of the United States that is knowledgable about states that are popular tourist attractions",
    verbose = True,
    tools = [top_attractions, travel_guide]
)

state_rep = Agent(
    role = "City Selector",
    goal = "You need to pick out cities within the given states that are relevant to the users criteria",
    backstory = "You are a travel representative for your state that has extensive knowledge about tourist attractions among all your cities",
    verbose = True,
    tools = [top_attractions, travel_guide],
)

trip_planner = Agent(
    role = "Route Planner",
    goal = "Create an itinerary for the trip",
    backstory = "You are a knowledgable expert in trip routing and can plan out transportation requirements for a trip",
    verbose = True,
)

#create first task for handling the list of requirements
def create_list_task(request):
    return 

request = input("Describe your ideal trip: ")

create_list = Task(
    description = "Take the user input and parse their request for any necessary information or criteria that they need fulfilled for their destinations. The user request is: " + request,
    expected_output = "A bulleted list of criteria",
    agent = criteria_organizer,
    )

#create second task for finding relevant states (pass list of requirements as well), make sure they are within reasonable distance of each other
find_states = Task(
    description = "Using the list of criteria find 2 or 3 states that have the best activitites that the user may enjoy. Make sure to include all the activities that are a good fit",
    expected_output = "A full paragraph for each state",
    agent = national_rep,
)

#create third task for finding relevant citites within those states
find_cities = Task(
    description = "Using the information about the best states and the relevant activities as well, find the best cities for the user to travel to to get the best travel experience. You may also list out the names of restaurants, resorts, and hotels that the user can also visit",
    expected_output = "Organized list of states and the relevant activities",
    agent = state_rep,
)

plan_route = Task(
    description = "Using the list of planned destinations, figure out an optimal itinerary to travel between them in any order that is necessary. You may decide if the locations are within drivable distance or a flight is necessary (typically for several states over)",
    expected_output = "A list of the destinations with their activities with the travel information listed between them",
    agent = trip_planner,
)

crew = Crew(
    agents = [criteria_organizer, national_rep, state_rep, trip_planner],
    tasks = [create_list, find_states, find_cities, plan_route],
    verbose = 2,
)

result = crew.kickoff()
print("--------------------------------------")
print(result)