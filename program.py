from parser_1 import Parser

if __name__ == "__main__":
    code = """
    int main () {
        int x = 10;
        if (x > 5) {
            printf("Hi");
        }
    }
    """

    parser = Parser()
    parser.load_tokens(code)
    parser.parse_program()

    if parser.errors:
        print("\nSyntax Errors Found:")
        for err in parser.errors:
            print(err)
    else:
        print("\nParsing Successful!")
