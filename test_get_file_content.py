from functions.get_file_content import get_file_content
from config import MAX_CHARS

def main():
    print("---- lorem.txt ----")
    lorem_content = get_file_content("calculator", "lorem.txt")
    print("Length:", len(lorem_content))
    print("Ends with truncation message:", lorem_content.endswith(
        f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    ))

    print("\n---- main.py ----")
    print(get_file_content("calculator", "main.py"))

    print("\n---- pkg/calculator.py ----")
    print(get_file_content("calculator", "pkg/calculator.py"))

    print("\n---- /bin/cat ----")
    print(get_file_content("calculator", "/bin/cat"))

    print("\n---- pkg/does_not_exist.py ----")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()