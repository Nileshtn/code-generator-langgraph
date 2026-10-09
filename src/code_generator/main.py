from code_generator.core import generator_graph_app
import argparse

def main():
    parser = argparse.ArgumentParser(
                description="A code writer for simple python programs!"
                )

    parser.add_argument("--prompt", "-p",
                        type= str,
                        help= "prompt to generate the code!")

    args = parser.parse_args()
    app = generator_graph_app()

    if args.prompt:
        app.invoke({"query": args.prompt,
                    "itr" : 0,
                    "max_itr" : 5,
                    "feedback_type" : "",
                    "itr_history" : []})