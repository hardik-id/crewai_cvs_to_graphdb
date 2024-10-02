from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
load_dotenv()
# Uncomment the following line to use an example of a custom tool
from crewai_cvs_to_graphdb.tools.custom_tool import CypherExecutorTool


@CrewBase
class CrewaiCvsToGraphdbCrew():
	"""CrewaiCvsToGraphdb crew"""

	@agent
	def cv_parser(self) -> Agent:
		return Agent(
			config=self.agents_config['cv_parser'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			llm='azure/gpt-4o',
			verbose=False
		)

	@agent
	def cypher_query_validator(self) -> Agent:
		return Agent(
			config=self.agents_config['cypher_query_validator'],
			llm='azure/gpt-4o',
			verbose=True
		)

	@agent
	def cypher_query_executor(self) -> Agent:
		return Agent(
			config=self.agents_config['cypher_query_executor'],
			tools=[CypherExecutorTool()],
			llm='azure/gpt-4o',
			verbose=True
		)

	@task
	def extract_info(self) -> Task:
		return Task(
			config=self.tasks_config['extract_info'],
		)

	@task
	def execute_cypher(self) -> Task:
		return Task(
			config=self.tasks_config['validate_cypher'],
			output_file='report.md'
		)
	@task
	def execute_cypher(self) -> Task:
		return Task(
			config=self.tasks_config['execute_cypher'],
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the CrewaiCvsToGraphdb crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=False,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)