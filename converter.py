#!/usr/bin/env python3

import dict2xml
import argparse
from pathlib import Path


def main(input_path, output_path):
    input_path = _validate_filepath(input_path)
    output_path = _validate_filepath(output_path)
    
    print(f"input: {str(input_path)}")
    print(f"output: {str(output_path)}")

def _validate_filepath(filepath):
    path = Path(filepath)

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
        dest="input_path",
        help="Input file path name",
        required=True,
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        help="Output file path name",
        required=True,
    )

    arguments = parser.parse_args()

    main(arguments.input_path, arguments.output_path)
