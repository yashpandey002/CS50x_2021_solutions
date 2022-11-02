import sys
from cs50 import get_float


def main():

    float_change = get_float("Enter change: ")
    coin_count = 0

    # Ensure correct input
    while float_change <= 0:
        float_change = get_float("Enter change: ")

    int_change = int(float_change * 100)  # convert the change into int datatype

    while(int_change >= 25):  # Always check if change is greater than 25
        int_change -= 25
        coin_count += 1   # add 1 count to the coin variable

    while(int_change >= 10 and int_change < 25):  # Always check if change is between 10 and 25
        int_change -= 10
        coin_count += 1

    while(int_change >= 5 and int_change < 10):  # Always check if change is between 5 and 10
        int_change -= 5
        coin_count += 1

    while(int_change >= 1 and int_change < 5):  # Always check if change is between 1 and 5
        int_change -= 1
        coin_count += 1

    print("Coins:", coin_count)


main()

