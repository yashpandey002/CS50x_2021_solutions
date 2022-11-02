#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int main(void)
{
    string text = get_string("TEXT: ");
    int text_length = strlen(text);
    int letter_count = 0;
    int word_count = 1; //the last word is not counted, thats why we started from 1
    int sent_count = 0;
    for (int i = 0; i < text_length; i++)
    {
        if (true) //always check this condition for counting letters
        {
            if ((text[i] >= 'a' || text[i] >= 'A') && (text[i] <= 'z' || text[i] <= 'Z')) //checking if the character is only alphabet or not
            {
                letter_count += 1;
            }
            else
            {
                letter_count += 0; //if letter is other than alphabet like(! . , % etc) then add nothing or 0
            }
        }
        if (true) //always check this condition for counting words
        {
            if (text[i] == ' ')
            {
                word_count += 1;
            }
        }
        if (true) //always check this condition for counting sentences
        {
            if (text[i] == '.' || text[i] == '!' || text[i] == '?')
            {
                sent_count += 1;
            }
        }
    }
    float l = ((float)letter_count / (float)word_count) * 100.0;
    float s = ((float)sent_count / (float)word_count) * 100.0;
    int index = round(0.0588 * l - 0.296 * s - 15.8);
    if (index > 1 && index < 16)
    {
        printf("Grade %i\n", index);
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index <= 1)
    {
        printf("Before Grade 1\n");
    }
}