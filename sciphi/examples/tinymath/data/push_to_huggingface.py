from datasets import Dataset, load_dataset
import csv
import os
import glob


def load_tinymath():
    dataset = load_dataset("bhairavmehta95/tinymath")
    print(dataset)


def generate_csv():
    paths = []
    yamls = []

    for root, dirs, files in os.walk("."):
        # Check if "textbooks" directory exists within the current directory
        yamls += [x for x in files if x.endswith(".yaml")]
        if "textbooks" in dirs:
            # Create a path to the "textbooks" directory
            textbooks_dir = os.path.join(root, "textbooks")
            # Use glob to find all Markdown files within the "textbooks" directory
            markdown_files = glob.glob(os.path.join(textbooks_dir, "*.md"))

            # Process the found Markdown files
            for markdown_file in markdown_files:
                paths.append(markdown_file)

    data = []
    for file in paths:
        with open(file, "r") as f:
            contents = f.read()

        data.append(
            {
                "textbook": file.split("/")[-1].replace(".md", ""),
                "text": contents.replace("\n", "\\n"),
            }
        )

    print(files)
    print(
        f"Found {len(data)} textbooks",
        f"Found {len(yamls)} YAML files",
        sep="\n",
    )
    with open("test.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["textbook", "text"])
        writer.writeheader()
        writer.writerows(data)


generate_csv()
