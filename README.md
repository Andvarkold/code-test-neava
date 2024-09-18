# code-test-neava
usage: converter.exe [-h] --input INPUT --output OUTPUT

Convert row based file format to a XML structure.
    File format:

    P|firstname|lastname
    T|mobile|landline
    A|street|city|postcode
    F|name|born
    P can be followed by T, A and F
    F can be followed by T and A


options:  
-h, --help       show this help message and exit  
--input INPUT    Absolute path to input file  
--output OUTPUT  Absolute path to input file

# Executable
See the latest [artifact](https://github.com/Andvarkold/code-test-neava/actions/workflows/artifact.yml) workflow run for a package with an executable created using PyInstaller