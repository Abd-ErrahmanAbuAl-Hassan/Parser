from parser_1 import Parser
from scanner25 import Scanner

if __name__ == "__main__":
    code = """
    int main () {
        int x = 10;
        if (x > 5) {
            printf("Hi");
        }
    }
    """

    scanner = Scanner()
    tokens = scanner.tokenize(code)

    print("*" * 50)
    print("Token List:")
    for t in tokens:
        print(t)
    print("*" * 50)

    parser = Parser()
    parser.load_tokens(code)
    parser.parse_program()

    if parser.errors:
        print("\nSyntax Errors Found:")
        for err in parser.errors:
            print(err)
    else:
        print("\nParsing Successful!")
