def reverse_text(input_text):
    """
    Takes in some text and returns the text in reversed order
    (character by character)
    """
    for i in range(len(input_text), 0, -1):
        new_name += input_text[i]
    

def main():
    my_name = "whadya think?"
    print reverse_text(my_name)

if __name__ == "__main__":
    main()
