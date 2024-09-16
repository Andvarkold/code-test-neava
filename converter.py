#!/usr/bin/env python3

import dict2xml
import argparse
from pathlib import Path


def main(input: str, output: str):
    input_path = _validate_input(input)
    output_path = _validate_output(output)


def _validate_input(input: str) -> Path:
    input_path = Path(input)
    if not input_path.is_absolute():
        raise ValueError(f"Input '{input}' has to be an absolute path!")
    elif not input_path.exists():
        raise FileNotFoundError(f"Input '{input}' is not an existing file!")

    return input_path


def _validate_output(output: str) -> Path:
    output_path = Path(output)
    if not output_path.is_absolute():
        raise ValueError(f"Output '{output}' has to be an absolute path!")
    if not output_path.parent.exists():
        raise FileNotFoundError(f"Output '{output}' parent directory does not exists!")

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Convert row based file format to a XML structure. 
                File format:

                P|firstname|lastname
                T|mobile|landline
                A|street|city|postcode
                F|name|born
                P (Person) can be followed by T (Telephone), A (Address) and F (Family)
                F (Family) can be followed by T (Telephone) and A (Address)
                """,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--input",
        dest="input",
        help="Absolute path to input file",
        required=True,
    )
    parser.add_argument(
        "--output",
        dest="output",
        help="Absolute path to input file",
        required=True,
    )

    arguments = parser.parse_args()

    main(arguments.input, arguments.output)
