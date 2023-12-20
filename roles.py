import json


def read_roles_file(filepath):
    try:
        found_user = False
        system_content = []
        user_content = []

        with open(filepath, 'r') as file:
            first_line = file.readline()
            if not first_line.startswith("system:"):
                raise Exception("Invalid file format: File must start with 'system:' section.")

            current_section = system_content

            for line in file:
                if line.startswith("system:"):
                    raise Exception("Invalid file format: 'system:' section is repeated.")
                elif line.startswith("user:"):
                    if found_user:
                        raise Exception("Invalid file format: 'user:' section is repeated.")
                    found_user = True
                    current_section = user_content
                    continue
                if current_section is not None:
                    current_section.append(line.strip())

        if not found_user:
            raise Exception("Invalid file format: Missing 'user:' section.")
        if not system_content or not user_content:
            raise Exception("Invalid file format: 'system' or 'user' section is empty.")

        return {
            "system": ' '.join(system_content),
            "user": ' '.join(user_content)
        }

    except FileNotFoundError:
        raise FileNotFoundError(f"The file path {filepath} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


if __name__ == "__main__":
    file_paths = [
        "roles/product_owner_architect.txt",
        "roles/team_lead.txt",
        "roles/developer.txt",
        "roles/validator.txt",
        "roles/developer_fixer.txt",
    ]

    try:
        for path in file_paths:
            print("Reading: ", path)
            role = read_roles_file(path)
    except Exception as e:
        print(e)
