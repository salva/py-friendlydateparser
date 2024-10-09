from friendlydateparser import parse_date

def test_parser(input_text):

    result = parse_date(input_text)
    print(f"result: {result}")

    #tree.toStringTree(recog=parser))

if __name__ == "__main__":
    # Test inputs


    inputs = [
        "10/1045",
        "last sunday",
        "next monday",
        "next friday",
        "last tuesday",
        "next tue",
        "october/3/2017",
        "october/3",
        "3/october/2017",
        "3/october",
        "10/3/2017",
        "10/3",
        "october/2017",
        "10/2017",
        "october",
        "the 3rd of october, 2017",
        "the 3rd of october 2017",
        "the 3rd of october"
    ]

    for input_text in inputs:
        print(f"Testing input: {input_text}")
        test_parser(input_text)
        print()
