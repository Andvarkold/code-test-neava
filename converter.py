#!/usr/bin/env python3

import argparse
from pathlib import Path
from dict2xml import dict2xml


def main(input: str, output: str) -> None:
    input_path = validate_input_argument(input)
    output_path = validate_output_argument(output)

    print(f"Started parsing input file at '{input}'")
    with input_path.open() as source, output_path.open("w") as target:
        target.write("<people>\n")
        person = []
        for raw_line in source:
            line = raw_line.strip()
            if line[0] == "P" and person:
                try:
                    person_data = parse_person(person)
                    target.write(
                        dict2xml(person_data, wrap="person", indent=" ") + "\n"
                    )
                except Exception as e:
                    print(
                        f"Failed to parse or write person {person} with exception: {e}"
                    )
                person = [line]
            else:
                person.append(line)

        # Handle last person
        try:
            if person:
                person_data = parse_person(person)
                target.write(dict2xml(person_data, wrap="person", indent=" ") + "\n")
        except Exception as e:
            print(f"Failed to parse or write person {person} with exception: {e}")
        target.write("</people>")

    print(f"Output created at '{output}'")


def validate_input_argument(input: str) -> Path:
    input_path = Path(input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input '{input}' is not an existing file!")

    return input_path


def validate_output_argument(output: str) -> Path:
    output_path = Path(output)
    if not output_path.parent.exists():
        raise FileNotFoundError(f"Output '{output}' parent directory does not exists!")

    return output_path


def parse_person(data: list[str]) -> dict:
    person_data = {}
    for line in data:
        raw_parts = line.split("|")
        parts = [part.strip() for part in raw_parts]

        match parts[0]:
            case "P":
                person_data.update(parse_p(parts[1:]))
                add_to_family_data = False
            case "T":
                temp_data = parse_t(parts[1:])

                if add_to_family_data:
                    person_data["family"][-1]["phone"] = temp_data
                else:
                    person_data["phone"] = temp_data
            case "A":
                temp_data = parse_a(parts[1:])

                if add_to_family_data:
                    person_data["family"][-1]["address"] = temp_data
                else:
                    person_data["address"] = temp_data
            case "F":
                temp_data = parse_f(parts[1:])
                if "family" in person_data:
                    person_data["family"].append(temp_data)
                else:
                    person_data["family"] = [temp_data]
                add_to_family_data = True
            case _:
                raise ValueError(
                    f"Incorrect format was '{parts[0]}', expected P, T, A or F"
                )

    return person_data


def parse_p(parts: list[str]) -> dict:
    if len(parts) != 2:
        raise ValueError(
            f"Incorrect length for format 'P' was {parts} expect [firstname, lastname]"
        )

    data = {"firstname": parts[0], "lastname": parts[1]}

    return data


def parse_t(parts: list[str]) -> dict:
    if len(parts) != 2:
        raise ValueError(
            f"Incorrect length for format 'T' was {parts} expect [mobile, landline]"
        )

    data = {"mobile": parts[0], "landline": parts[1]}

    return data


def parse_a(parts: list[str]) -> dict:
    if len(parts) != 3:
        raise ValueError(
            f"Incorrect length for format 'A' was {parts} expect [street, city, postcode]"
        )

    data = {"street": parts[0], "city": parts[1], "postcode": parts[2]}

    return data


def parse_f(parts: list[str]) -> dict:
    if len(parts) != 2:
        raise ValueError(
            f"Incorrect length for format 'F' was {parts} expect [name, born]"
        )

    data = {"name": parts[0], "born": parts[1]}

    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Convert row based file format to a XML structure. 
                File format:

                P|firstname|lastname
                T|mobile|landline
                A|street|city|postcode
                F|name|born
                P can be followed by T, A and F
                F can be followed by T and A
                """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--input",
        dest="input",
        help="Absolute or relative path to input file",
        required=True,
    )
    parser.add_argument(
        "--output",
        dest="output",
        help="Absolute or relative path to output file",
        required=True,
    )

    arguments = parser.parse_args()

    main(arguments.input, arguments.output)
