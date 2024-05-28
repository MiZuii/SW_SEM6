import sys

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Invalid arguments", file=sys.stderr)
        print("Arg1: ID", file=sys.stderr)
        exit(1)

    print(f"The argument is {sys.argv[1]}")
    exit(0)