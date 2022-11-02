from cs50 import get_int


def main():
    while(True):
        height = get_int("Height: ")

        if height > 0 and height <= 8:  # exiting the loop if condition satisfied
            break

    pyramid_maker(height)  # calling a function which makes and return the pattern


def pyramid_maker(h):
    for i in range(0, h):
        for j in range(0, h):
            if(j < (h - (i + 1))):  # condition for printing left pyramid with spaces
                print(' ', end='')
            else:
                print('#', end='')

        print("  ", end='')  # printing space between two columns

        for k in range(0, i+1):
            print('#', end='')  # printing right pyramid without spaces
        print()


main()