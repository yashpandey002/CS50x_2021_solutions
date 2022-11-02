from cs50 import get_string


def main():
    para = get_string("Text: ")
    para_lower = para.lower()  # converting text to lower case for easy comparison

    grade = coleman_liau(para_lower)

    if(grade >= 16):
        print("Grade 16+")
    elif(grade < 1):
        print("Before Grade 1")
    else:
        print("Grade ", grade)


def coleman_liau(text):

    letter_count = 0
    word_count = 1  # word_count = 1 because last word doesn't have space
    sent_count = 0

    # creating a list of letters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for character in text:
        if character in letters:  # if a character is in letters list
            letter_count += 1
        elif character == " ":  # condition for word
            word_count += 1
        elif character == "." or character == "!" or character == "?" or character == " ":  # condition for sentence
            sent_count += 1

    L = (letter_count / word_count) * 100  # Average letters per 100 words
    S = (sent_count / word_count) * 100  # Average sentences per 100 words
    index = round(0.0588 * L - 0.296 * S - 15.8)  # Index calculation

    return index


if __name__ == "__main__":
    main()