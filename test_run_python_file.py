from functions.run_python_file import run_python_file

if __name__ == "__main__":
    print("Should print the calculator's usage instructions:")
    print (run_python_file("calculator", "main.py"))
    print("\nShould run the calculator:")
    print (run_python_file("calculator", "main.py", ["3 + 5"]))
    print("\nShould run the calculator's tests successfully:")
    print (run_python_file("calculator", "tests.py"))
    print ("\nshould return an error:")
    print (f"   {run_python_file("calculator", "../main.py")}")
    print ("\nshould return an error:")
    print (f"   {run_python_file("calculator", "nonexistent.py")}")
    print ("\nshould return an error:")
    print (f"   {run_python_file("calculator", "lorem.txt")}")
