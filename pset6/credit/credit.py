from cs50 import get_string
import sys


def main():
    card_num = get_string("Enter card number: ")  # Taking user input of card number

    if(luhn_validator(card_num) != 0):
        sys.exit("INVALID")  # Exit if last number of sum of card number is not 0

    card_len = len(card_num)

    # Conditions for AMEX card
    if(card_len == 15):
        if((card_num[0] == '3') and (card_num[1] == '4' or card_num[1] == '7')):
            print("AMEX")

    # Conditions for MASTERCARD card
    if(card_len == 16):
        mastercard_num = ['1', '2', '3', '4', '5']
        if(card_num[0] == '5'):
            if card_num[1] in mastercard_num:
                print("MASTERCARD")

    # Conditions for VISA card
    if(card_len == 13 or card_len == 16):
        if(card_num[0] == '4'):
            print("VISA")


def luhn_validator(num_string):

    card_length = len(num_string)
    sum1 = ""
    sum2 = 0
    final_sum = 0

    if(card_length % 2 == 0):
        for i in range(-2, -(card_length+1), -2):  # Starting from second last to first element
            sum1 += str(int(num_string[i]) * 2)  # multiplying each element by 2

        sum1_length = len(sum1)
        for i in range(sum1_length):  # Adding each elemnt of sum1
            sum2 += int(sum1[i])

        final_sum += sum2
        for i in range(-1, -(card_length), -2):  # Adding those which are not previously included
            final_sum += int(num_string[i])

        result = str(final_sum)

    else:
        for i in range(-2, -(card_length), -2):  # Starting from second last to first element
            sum1 += str(int(num_string[i]) * 2)  # multiplying each element by 2

        sum1_length = len(sum1)
        for i in range(sum1_length):  # Adding each elemnt of sum1
            sum2 += int(sum1[i])

        final_sum += sum2
        for i in range(-1, -(card_length+1), -2):  # Adding those which are not previously included
            final_sum += int(num_string[i])

        result = str(final_sum)

    if result[-1] == '0':
        return 0
    else:
        return 1


if __name__ == "__main__":
    main()