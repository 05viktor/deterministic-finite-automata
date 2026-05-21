def is_comment(line):
    return line.startswith("#")


def is_empty_line(line):
    return line == ""


def parse_sections(input_file):
    sections = {}
    current_section = None

    for raw_line in input_file.readlines():
        line = raw_line.strip()

        if is_empty_line(line) or is_comment(line):
            continue

        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            if current_section not in sections:
                sections[current_section] = []
            continue

        if line == "End":
            current_section = None
            continue

        if current_section is None:
            continue

        sections[current_section].append(line)

    return sections
