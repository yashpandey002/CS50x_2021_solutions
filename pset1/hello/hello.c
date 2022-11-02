#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("Enter your name: "); //geting user name
    printf("Hello, %s\n", name); //printing the name with hello
}