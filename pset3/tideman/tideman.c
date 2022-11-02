#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];


// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;
// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;
int voter_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void record_winner(int winner, int loser, int place);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);


int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }

    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i; //at ranks[j] = fill with i
            return true;
        }
    }
    return false;
}


// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]] += 1;//at preferences[element ranks[i]index][element ranks[j]index]
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count - 1; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])//compare preference[i][j] with preference[j][i]
            {
                record_winner(i, j, pair_count);
                pair_count += 1;
            }
            else if (preferences[i][j] < preferences[j][i])//compare preference[j][i] with preference[i][j]
            {
                record_winner(j, i, pair_count);
                pair_count += 1;
            }
            else
            {
                pair_count += 0;
            }
        }
    }
    return;
}


void record_winner(int winner, int loser, int place)
{
    for (int i = place; i < place + 1; i++)
    {
        pairs[i].winner = winner;
        pairs[i].loser = loser;
    }
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    pair temp;
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = i + 1; j < pair_count; j++)
        {
            if ((preferences[pairs[j].winner][pairs[j].loser]) > (preferences[pairs[i].winner][pairs[i].loser]))
            {
                temp.winner = pairs[i].winner;
                temp.loser = pairs[i].loser;

                pairs[i].winner = pairs[j].winner;
                pairs[i].loser = pairs[j].loser;

                pairs[j].winner = temp.winner;
                pairs[j].loser = temp.loser;
            }
        }
    }
    return;
}

bool check_cycle(int first_winner, int winner, int loser)
{
    if (first_winner == loser)
    {
        return true;
    }
    else
    {
        for (int i = 0; i < pair_count; i++)
        {
            if (locked[loser][pairs[i].loser] == true)
            {
                if (check_cycle(first_winner, loser, pairs[i].loser))
                {
                    return true;
                }
            }
        }
    }
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        if (!check_cycle(pairs[i].winner, pairs[i].winner, pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}



// Print the winner of the election
void print_winner(void)
{
    int winner_count = 0;
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i] == false)
            {
                winner_count += 1;
            }
        }
        if (winner_count == candidate_count)
        {
            printf("%s\n", candidates[i]);
        }
        else
        {
            winner_count -= winner_count;

        }
    }
    return;
}


