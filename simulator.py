import gpt
import roles
import json
import os


def generate_design_specs(requirements_filepath, design_specs_filepath):
    if os.path.exists(design_specs_filepath):
        print(f"Design Specification: {design_specs_filepath}  -> already exists.")
        return

    if not os.path.exists(requirements_filepath):
        print(f"Requirements: {requirements_filepath}  -> not found!")
        return

    roles_filepath = 'roles/product_owner_architect.txt'
    if not os.path.exists(roles_filepath):
        print(f"Role: {roles_filepath}  -> not found!")
        return

    with open(requirements_filepath, 'r') as f:
        requirements = f.read()
    print("Requirements:\n", requirements)

    prompt = roles.read_roles_file(roles_filepath)
    print("system:\n", prompt["system"])
    print("\nuser:\n", prompt["user"])

    user_prompt = "Requirements: " + requirements + " " + prompt["user"]
    print("\nUser Prompt:\n", user_prompt)

    prompt['user'] = user_prompt

    response = gpt.gpt(prompt)

    with open(design_specs_filepath, 'w') as json_file:
        json.dump(json.loads(response), json_file, indent=2)


def generate_developer_tasks(design_specs_filepath, developer_tasks_filepath):
    if os.path.exists(developer_tasks_filepath):
        print(f"Developer Tasks: {developer_tasks_filepath}  -> already exists.")
        return

    if not os.path.exists(design_specs_filepath):
        print(f"Design Specification: {design_specs_filepath}  -> not found!")
        return

    roles_filepath = 'roles/team_lead.txt'
    if not os.path.exists(roles_filepath):
        print(f"Role: {roles_filepath}  -> not found!")
        return

    with open(design_specs_filepath, 'r') as json_file:
        design_specs = json.load(json_file)

    print("Design Specifications:\n", json.dumps(design_specs, indent=2))

    prompt = roles.read_roles_file(roles_filepath)
    print("system:\n", prompt["system"])
    print("\nuser:\n", prompt["user"])

    user_prompt = "Design Specification: " + json.dumps(design_specs) +\
                  "\n " + prompt["user"]
    count = gpt.token_count(user_prompt)

    print(f"\nUser Prompt({count}):\n", user_prompt)

    prompt['user'] = user_prompt

    response = gpt.gpt(prompt)

    with open(developer_tasks_filepath, 'w') as json_file:
        json.dump(json.loads(response), json_file, indent=2)


def get_new_filename(filepath):
    base_directory, base_filename = os.path.split(filepath)
    filename, file_extension = os.path.splitext(base_filename)

    index = 0
    while True:
        if index == 0:
            new_filename = f"{base_directory}/{base_filename}"
        else:
            new_filename = f"{base_directory}/{filename}_{index}{file_extension}"

        if not os.path.exists(new_filename):
            return new_filename

        index += 1


def implement_tasks(source_code_filepath, design_specs_filepath, developer_task):
    source_code = ""
    if os.path.exists(source_code_filepath):
        with open(source_code_filepath, 'r') as f:
            source_code = f.read()
    print("Source Code:\n", source_code)

    if not os.path.exists(design_specs_filepath):
        print(f"Design Specification: {design_specs_filepath}  -> not found!")
        return

    roles_filepath = 'roles/developer.txt'
    if not os.path.exists(roles_filepath):
        print(f"Role: {roles_filepath}  -> not found!")
        return

    with open(design_specs_filepath, 'r') as json_file:
        design_specs = json.load(json_file)

    # print("Design Specifications:\n", json.dumps(design_specs, indent=2))

    prompt = roles.read_roles_file(roles_filepath)
    print("system:\n", prompt["system"])
    print("\nuser:\n", prompt["user"])

    user_prompt = f"Source Code from file {source_code_filepath}:" + source_code +\
                  "\nDesign Specification: " + json.dumps(design_specs) +\
                  "\nTask: " + developer_task +\
                  "\n" + prompt["user"]
    count = gpt.token_count(user_prompt)

    print(f"\nUser Prompt({count}):\n", user_prompt)

    prompt['user'] = user_prompt

    response = gpt.gpt(prompt)
    response = json.loads(response)

    new_source_code_filepath = get_new_filename(source_code_filepath)

    try:
        os.rename(source_code_filepath, new_source_code_filepath)
        print(f"Backed up code to: {new_source_code_filepath}")
    except OSError as e:
        print(f"Error: {e}")

    with open(source_code_filepath, 'w') as file:
        file.write(response["code"])


def review_and_fix(source_code_filepath, design_specs_filepath, review_finding):
    source_code = ""
    if os.path.exists(source_code_filepath):
        with open(source_code_filepath, 'r') as f:
            source_code = f.read()
    # print("Source Code:\n", source_code)

    if not os.path.exists(design_specs_filepath):
        print(f"Design Specification: {design_specs_filepath}  -> not found!")
        return

    roles_filepath = 'roles/developer_fixer.txt'
    if not os.path.exists(roles_filepath):
        print(f"Role: {roles_filepath}  -> not found!")
        return

    with open(design_specs_filepath, 'r') as json_file:
        design_specs = json.load(json_file)

    # print("Design Specifications:\n", json.dumps(design_specs, indent=2))

    prompt = roles.read_roles_file(roles_filepath)
    print("system:\n", prompt["system"])
    print("\nuser:\n", prompt["user"])

    user_prompt = f"Source Code from file {source_code_filepath}:" + source_code +\
                  "\nDesign Specification: " + json.dumps(design_specs) +\
                  "\nTask You Must Fix: " + review_finding +\
                  "\n" + prompt["user"]

    # user_prompt = f"Source Code from file {source_code_filepath}:" + source_code + "\n" + prompt["user"]

    count = gpt.token_count(user_prompt)

    print(f"\nUser Prompt({count}):\n", user_prompt)

    prompt['user'] = user_prompt

    print("\n---------------\nReview and fix: ", review_finding)

    response = gpt.gpt(prompt)
    response = json.loads(response)

    new_source_code_filepath = get_new_filename(source_code_filepath)

    try:
        os.rename(source_code_filepath, new_source_code_filepath)
        print(f"Backed up code to: {new_source_code_filepath}")
    except OSError as e:
        print(f"Error: {e}")

    with open(source_code_filepath, 'w') as file:
        file.write(response["code"])

    print(response["code"])


def development():
    with open('gen/developer_tasks.json', 'r') as json_file:
        developer_tasks = json.load(json_file)

    with open('gen/review_findings.json', 'r') as json_file:
        review_findings = json.load(json_file)
    '''
    for task in developer_tasks['steps']:
        # print(f"{task['id']} [{task['category']}] -> {task['description']}")
        if task['category'] == "coding" and task['id'] == 6:
            print(f"\nTask -> {task['id']}. {task['description']}")
            # implement_tasks('gen/chess.py', 'gen/design_specification.json', task['description'])

            review_and_fix('gen/chess.py', 'gen/design_specification.json', task['description'])
    '''
    for review_finding in review_findings['Findings']:
        print(f"{review_finding['Finding']} [{review_finding['Section']}] -> {review_finding['Details']}")
        review_and_fix('gen/chess.py', 'gen/design_specification.json', review_finding['Details'])


def simulator():
    generate_design_specs('requirements/chess_requirements.txt', 'gen/design_specification.json')
    generate_developer_tasks('gen/design_specification.json', 'gen/developer_tasks.json')

    development()


simulator()



