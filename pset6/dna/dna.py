import csv
import sys


def main():
    # Ensure correct usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    database = sys.argv[1]
    person_dna = sys.argv[2]

    strs_calculator(database, person_dna)


def strs_calculator(csv_database, dna):
    with open(csv_database, 'r') as csv_file:
        reader = csv.DictReader(csv_file)

        data = []  # Reading csv file into list of dict
        for row in reader:
            data.append(row)
            strs_list = list(row.keys())
            del strs_list[0]  # deleting name from strs list

    with open(dna, 'r') as txt_file:
        sequence = txt_file.read()

        string = ''
        for characters in sequence:
            string += characters

        strs_final = {}  # dict which will contain final strs eg {"Atgd": 45, "FGH": 75}

        for i in range(len(strs_list)):
            strs_len = len(strs_list[i])
            max_strs = []
            for j in range(len(string)):
                if strs_list[i] == string[j:j+strs_len]:  # if str found in sequence
                    position = 0
                    strs_count = 0

                    #  find how many times that strs come in current founding
                    while strs_list[i] == string[j + position:j + strs_len + position]:
                        strs_count += 1
                        position += strs_len
                    max_strs.append(strs_count)  # appending to list for current str

                if max_strs == []:
                    strs_final[strs_list[i]] = 0
                else:
                    strs_final[strs_list[i]] = max(max_strs)

    for i in range(len(data)):
        count = 0
        for j in range(len(strs_list)):
            if int(data[i][strs_list[j]]) == strs_final[strs_list[j]]:
                count += 1
                if(count == len(strs_list)):
                    print(data[i]['name'])
                    exit()
    print("No match")


if __name__ == "__main__":
    main()