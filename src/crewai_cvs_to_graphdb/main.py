#!/usr/bin/env python
import sys
from crewai_cvs_to_graphdb.crew import CrewaiCvsToGraphdbCrew
import os

from unstructured.partition.docx import partition_docx

def docx_to_text(docx_path):
    """
    Convert a .docx file to plain text using the unstructured library.
    """
    try:
        elements = partition_docx(filename=docx_path)
        # Combine the text from all elements
        text = '\n'.join([element.text for element in elements if element.text])
        print(text)
        return text
    except Exception as e:
        print(f"Error processing {docx_path}: {e}")
        return ""

def run():
    """
    Run the crew on all .docx files in the 'cvs' folder.
    """
    folder_path = 'cvs'  # Path to the folder containing the .docx files

    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            print(filename)
            docx_path = os.path.join(folder_path, filename)
            print(docx_path)
            # Convert .docx to plain text using unstructured lib
            cv_text = docx_to_text(docx_path)
            print(cv_text)

            # Inputs for the kickoff process
            inputs = {
                'CV_TEXT': cv_text
            }

            # Run the crew with the extracted CV text
            CrewaiCvsToGraphdbCrew().crew().kickoff(inputs=inputs)

run()
# def run():
#     """
#     Run the crew.
#     """
#     inputs = {
#         'CV_TEXT': 'AI LLMs'
#     }
#     CrewaiCvsToGraphdbCrew().crew().kickoff(inputs=inputs)


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiCvsToGraphdbCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        CrewaiCvsToGraphdbCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewaiCvsToGraphdbCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
