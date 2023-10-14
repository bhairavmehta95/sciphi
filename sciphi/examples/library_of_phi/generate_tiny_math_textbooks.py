# type: ignore
"""
YAML Table of Contents to Textbook Generator

WARNING - This script is very rough and needs significant enhancements to fully productionize
Description:
    This script processes YAML files and generates a detailed Table of Contents for a new textbook accompanying the course.

Usage:
    Command-line interface:
        $ python sciphi/examples/library_of_phi/generate_textbook.py run
Parameters:
    provider (str): 
        The provider to use. Default is 'openai'.
    model (str): 
        The model name to use. Default is 'gpt-3.5-turbo-instruct'.
    parsed_dir (str): 
        Directory containing parsed data. Default is 'raw_data'.
    toc_dir (str): 
        Directory for the table of contents. Default is 'table_of_contents'.
    output_dir (str): 
        Directory for the output. Default is 'output_step_4'.
      (str): 
        Name of the textbook. Default is 'Introduction_to_Deep_Learning'.
    max_related_context_to_sample (int): 
        Maximum context to sample. Default is 2000.
    max_prev_snippet_to_sample (int): 
        Maximum previous snippet to sample. Default is 2000.
    do_wiki (bool): 
        Whether to use Wikipedia. Default is True.
    wiki_server_url (str): 
        Wikipedia server URL. Uses environment variable "WIKI_SERVER_URL" if not provided.
    wiki_username (str): 
        Wikipedia username. Uses environment variable "WIKI_SERVER_USERNAME" if not provided.
    wiki_password (str): 
        Wikipedia password. Uses environment variable "WIKI_SERVER_PASSWORD" if not provided.
    log_level (str): 
        Logging level. Can be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL. Default is 'INFO'.
"""
import os

import fire
import logging

from sciphi.core.utils import get_data_dir
from sciphi.examples.library_of_phi.gen_step_5_draft_book import (
    TextbookContentGenerator,
)


def setup_logging(log_level="INFO"):
    """Set up logging."""
    logging.basicConfig(level=log_level.upper())
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level.upper())
    return logger


class TextbookContentGeneratorSimplified:
    def __init__(self) -> None:
        pass

    def run(
        self,
        provider="hugging-face",
        model_name="open-phi/instruct-textbook-beta",
        max_related_context_to_sample=2_000,
        max_prev_snippet_to_sample=2_000,
        do_wiki=True,
        wiki_server_url=None,
        wiki_username=None,
        wiki_password=None,
        log_level="INFO",
    ):
        logger = setup_logging(log_level)
        """Runs the generation process to create a textbook from the YAML table of contents."""

        for grade in os.listdir(
            os.path.join("sciphi", "examples", "tinymath", "data")
        ):
            toc_dir = os.path.join(
                "sciphi", "examples", "tinymath", "data", grade
            )

            if not os.path.isdir(toc_dir):
                continue

            output_dir = os.path.join(
                "sciphi",
                "examples",
                "tinymath",
                "data",
                grade,
                "textbooks",
            )

            os.makedirs(
                output_dir,
                exist_ok=True,
            )

            for textbook_yml in os.listdir(toc_dir):
                if not textbook_yml.endswith(".yaml"):
                    continue
                textbook = textbook_yml.split(".")[0]

                # if os.path.exists(
                #     os.path.join(
                #         "sciphi",
                #         "examples",
                #         "tinymath",
                #         "data",
                #         grade,
                #         "textbooks",
                #         textbook + ".md",
                #     )
                # ):
                #     logger.warn(f"Skipping {textbook} as it already exists")
                #     continue

                TextbookContentGenerator(
                    provider,
                    model_name,
                    data_dir=os.path.join(
                        "sciphi", "examples", "tinymath", "data"
                    ),
                    toc_dir=grade,
                    output_dir=os.path.join(grade, "textbooks"),
                    textbook=textbook,
                    max_related_context_to_sample=max_related_context_to_sample,
                    max_prev_snippet_to_sample=max_prev_snippet_to_sample,
                    do_wiki=do_wiki,
                    wiki_server_url=wiki_server_url,
                    wiki_username=wiki_username,
                    wiki_password=wiki_password,
                    log_level=log_level,
                    prompt_kwargs={"level": grade},
                ).run()

                # TEMPORARY
                # return


if __name__ == "__main__":
    fire.Fire(TextbookContentGeneratorSimplified)
