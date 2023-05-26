import json
import os


def process_jsonl(jsonl_path, html_dir, prompt_path, output_path):
    with open(jsonl_path, "r") as jsonl_file, open(output_path, "w") as output_file:
        for i, line in enumerate(jsonl_file):
            # load the json line file
            json_line = json.loads(line.strip())
            # replace the {{content}} placeholder with actual content
            for entry in json_line["input"]:
                # load the prompt
                with open(prompt_path, "r") as prompt_file:
                    prompt = prompt_file.read()
                # add the html content into the prompt
                html_file_path = os.path.join(html_dir, f"html-{i+1}.txt")
                with open(html_file_path, "r") as html:
                    html_content = html.read()
                    prompt = prompt.replace("{web_content}", html_content)

                # replace the {{content}} placeholder with actual full content (prompt + html)
                if "{content}" in entry["content"]:
                    entry["content"] = entry["content"].replace("{content}", prompt)

            # write the updated line to the output file
            output_file.write(json.dumps(json_line) + "\n")


process_jsonl(
    "tgsetup/samples.jsonl",
    "tgsetup",
    "tgsetup/linkedin-prompt.txt",
    "evals/registry/data/tglist/samplesout.jsonl",
)
