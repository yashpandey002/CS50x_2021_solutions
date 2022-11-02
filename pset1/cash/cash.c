#include <stdio.h>
#include <cs50.h>
#include <math.h>

int main(void)
{
    float change;
    int coin = 0;
    
    do
    {
        change = round(get_float("Enter change: ") * 100); //round the input to the nearest penny
    }
    while (change < 0.100); //Cheking if input is negative number
    
    if (change >= 25) //Always check if change is greater than 25
    {
        do
        {
            coin++; //add 1 count to the coin variable
            change -= 25;
        }
        while (change >= 25);
    }
    
    if (change >= 10) //Always check if change is greater than 10
    {
        do
        {
            coin++;
            change -= 10;
        }
        while (change >= 10);
    }
    
    if (change >= 5) //Always check if change is greater than 5
    {
        do
        {
            coin++;
            change -= 5;
        }
        while (change >= 5);
    }
    
    if (change >= 1) //Always check if change is greater than 1
    {
        do
        {
            coin++;
            change -= 1 ;
        }
        while (change >= 1);
    }
    printf("%i \n", coin);
}