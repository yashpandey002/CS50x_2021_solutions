#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <cs50.h>


int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover card_name");
        return 1;
    }

    FILE *card = fopen(argv[1], "r"); // Open Memory card


    if (card == NULL)
    {
        printf("Please use valid Memory card\n");
        return 2;
    }

    // Variables and Pointers
    typedef uint8_t byte;
    const int block = 512;
    byte buffer[block];
    bool jpg_indicator;
    int jpg_counter = 0;
    char filename[8];
    FILE *img = NULL;

    while (fread(&buffer, 512, 1, card) == 1) //Iterate over evry byte of memory card
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0) // Check if jpg
        {
            if (jpg_indicator == true) // Close previous jpg if found new
            {
                fclose(img);
            }

            jpg_indicator = true;
            sprintf(filename, "%03i.jpg", jpg_counter);
            img = fopen(filename, "w");
            jpg_counter++;
        }

        if (jpg_indicator == true) // Write to previous file if new jpg not found
        {
            fwrite(&buffer, 512, 1, img);
        }
    }
    fclose(card);
    fclose(img);

    return 0;
}