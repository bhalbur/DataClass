import os
import csv

months = 0
profit = 0
current = 0
prev = 867884
change = 0
totchange = 0
avchange = 0
high_chg = -999999
low_chg = 999999


with open("budget_data.csv") as f:
    reader = csv.reader(f)

    next(reader, None)

    for line in reader:
        months += 1
        profit += int(line[1])
        current = int(line[1])
        change = current - prev
        totchange += change
        if change > high_chg:
            high_chg = change
            high_mon = line[0]
        if change < low_chg:
            low_chg = change
            low_mon = line[0]

        prev = int(line[1])

    avchange = round(totchange/(months-1), 2)

    print(f"Budget Analysis")
    print(f"---------------------------")
    print(f"Total Months: {months}")
    print(f"Total Profit: ${profit}")
    print(f"Average Change: {avchange}")
    print(f"Largest Change: {high_mon}: ${high_chg}")
    print(f"Smallest Change: {low_mon}: ${low_chg}")

##################################################################################


cand_list = []
cand_votes = 0
votecount = 0


with open("election_data.csv") as file:
    pollreader = csv.DictReader(file)

    next(pollreader, None)

    for row in pollreader:
        votecount +=1
        if row['Candidate'] not in cand_list:
            cand_list.append(row['Candidate'])


    print(f"total votes: {votecount}")
    print(cand_list)