#include <stdio.h>
#include <cs50.h>

int main(void) {
    int height;
    do {
        height = get_int("Height: ");
    }
    while (height <= 0 || height >= 9); //Geting Height from user

    for (int i = 0; i < height; i++) { //Generating Rows 
        for (int j = 0; j < height; j++) { //Generating Columns
            if (height - (j + 1) > i) { //Printing Spaces
                printf(" ");
            }
            else {
                printf("#"); //Printing Hashes
            }
        }
        printf("\n"); //Printing New Line at the end of every line
    }
}
