# Imports
import os
import sys

# Options
argv = sys.argv[1:]
print(argv)
if argv[0] in ["-h", "--help"]:
    print("=== Objective x2 ===")
    print("Usage")
    if argv[1] in ["-l", "--long"]:
        pass
    else:
        print("hi")