# Test prompt templates and chaining
import langchain
#import prompts

from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

template1 = """
Your goal is to provide assistance on wardley maps and always give a verbose answer. The following explains how the wardley map is formatted:\n\n
Thank you for providing the detailed explanation of the Wardley Map formatting. Here is a summary of the elements in the format:\n
Title: The title of the Wardley Map.
Components: Name of the component. Component Name [Visibility, Maturity].
Market: Create a market with market Name [Visibility, Maturity].
Inertia: Indicate resistance to change with inertia.
Evolve: Evolution of a component. volve Name (X Axis).
Links: Link components with Start Component->End Component.
Flow: Indicate flow. Component->>Component.
Pipeline: Set a component as a pipeline with pipeline Component Name [X Axis (start), X Axis (end)].
Pioneers, Settlers, Townplanners area: Add areas to indicate the working approach with pioneers, settlers, and townplanners.
Build, buy, outsource: Indicate the method of execution with build, buy, or outsource.
Submap: Link a submap to a component with submap Component [visibility, maturity] url(urlName) and url urlName [URL].
Stages of Evolution: Customize the stages of evolution labels with evolution.
Y-Axis Labels: The visibility of the component
Notes: Notes about this Wardley Map.
Styles: The style of the Wardley Map.
This formatting makes it easy to create and modify Wardley Maps, and it's helpful for understanding the structure and connections between components.

X-axis: Evolution (from left to right)

Genesis (0.0 to 0.2): Novel, unique, and unproven components
Custom Built (0.21 to 0.4): Developed specifically for a particular use case or organization, less mature, and standardized
Product (0.41 to 0.7): More widely available, standardized, and mature components with multiple implementations or versions in the market
Commodity (0.71 to 1.0): Highly standardized, widely available, often provided as a utility or service, very mature, and little differentiation between offerings

Y-axis: Visibility (from bottom to top)

At the left side of the map (0.0), components are less visible to the user, meaning that they are more internal, hidden, or not directly related to user interactions.
At the right side of the map (1.0), components are more visible to the user, meaning that they are directly related to user interactions or are essential components that the user experiences.
"""

f = open('wardley_maps/prompt_engineering_wardley_map.txt', 'r')
wmmap = f.read()
f.close()

#prompt = PromptTemplate(
#    input_variables=["wardleymap"],
#    template=template1,
#)

#print (prompt)

system_message_prompt = SystemMessagePromptTemplate.from_template(template1)
human_template="What is this wardley mapp all about?"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

# get a chat completion from the formatted messages
chat_prompt.format_prompt(input_language="English", output_language="French", text="I love programming.").to_messages()

prompt=PromptTemplate(
    template="You are a helpful assistant that translates {input_language} to {output_language}.",
    input_variables=["input_language", "output_language"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

prompt = load_prompt("wmprompt_1.json")
print(prompt.format(adjective="Prompt Engineering", content="wmmap"))
