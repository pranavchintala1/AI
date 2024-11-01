from crewai import Agent, Task, Crew
from crewai_tools import PDFSearchTool
import os

key_file = open("./api_key", "r")
api_key = key_file.read()
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o"

terms_tool = PDFSearchTool(pdf = "./Terms Summarizer/macOSSonoma.pdf")

legal_advisor = Agent(
    role = "Legal Advisor",
    goal = "Answer questions or fulfill requests relating to some legal documents",
    backstory = "An expert legal advisor that makes sure to give every piece of necessary legal advice",
    verbose = True,
    tools = [terms_tool]
)

summarize = Task(
    description = "Summarize the document with detail",
    expected_output = "A numbered list of sections each with some sub bullet points with summarized info",
    agent = legal_advisor,
)

crew = Crew(
    agents = [legal_advisor],
    tasks = [summarize],
    verbose = 1,
)

result = (crew.kickoff())

print("##################################")
print(result)