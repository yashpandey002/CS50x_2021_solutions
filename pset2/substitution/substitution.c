#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

    //Declaring normal variables
    string alpha_big = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    string alpha_small = "abcdefghijklmnopqrstuvwxyz";
    int key_length = strlen(argv[1]);
    char key[key_length]; //storing the key in new array
    printf("%i\n", argc);

    if (key_length != 26) //checking if the have 26 characters
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    for (int i = 0; i < key_length; i++) //checking if charcater are valid(other than alphabets)
    {
        if ((argv[1][i] >= 'a' || argv[1][i] >= 'A') && (argv[1][i] <= 'z' || argv[1][i] <= 'Z'))
        {
            key[i] = toupper(argv[1][i]); //convert key to capital
        }
        else
        {
            printf("Usage: ./substitution key\n");
            return 1;
        }
    }

    for (int j = 0; j < key_length; j++) //checking if charcater is reapeting
    {
        for (int k = j + 1; k <= key_length; k++)
        {
            if (key[j] == key[k])
            {
                printf("Don't enter duplicate key!\n");
                return 1;
            }
        }
    }

    string plaintext = get_string("plaintext: ");
    int length_plaintext = strlen(plaintext);
    
    printf("ciphertext: ");
    for (int l = 0; l < length_plaintext; l++)
    {
        if (plaintext[l] >= 'A' && plaintext[l] <= 'Z') //go to this condition if character is capital
        {
            for (int m = 0; m < key_length; m++)
            {
                if (plaintext[l] == alpha_big[m])
                {
                    printf("%c", key[m]);
                }
            }
        }
        else if (plaintext[l] >= 'a' && plaintext[l] <= 'z') //go to this condition if character is small
        {
            for (int m = 0; m < key_length; m++)
            {
                if (plaintext[l] == alpha_small[m])
                {
                    printf("%c", tolower(key[m]));
                }
            }
        }
        else
        {
            printf("%c", plaintext[l]);
        }
    }
    printf("\n");
    return 0;
}
