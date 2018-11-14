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

    print(f"")
    print(f"Budget Analysis")
    print(f"----------------------------------------")
    print(f"Total Months: {months}")
    print(f"Total Profit: ${profit}")
    print(f"Average Change: ${avchange}")
    print(f"Largest Change: {high_mon}:  (${high_chg})")
    print(f"Smallest Change: {low_mon}:  (${low_chg})")
    print(f"")
    print(f"")
    print(f"")

BudgetOutput = open("BudgetOutput.txt","w+")
BudgetOutput.write(f"Budget Analysis\n")
BudgetOutput.write(f"----------------------------------------\n")
BudgetOutput.write(f"Total Months: {months}\n")
BudgetOutput.write(f"Total Profit: ${profit}\n")
BudgetOutput.write(f"Average Change: ${avchange}\n")
BudgetOutput.write(f"Largest Change: {high_mon}:  (${high_chg})\n")
BudgetOutput.write(f"Smallest Change: {low_mon}:  (${low_chg})\n")
BudgetOutput.close()
##################################################################################

candlist = []
votelist = []
votecount = 0

with open("election_data.csv") as file:
    pollreader = csv.DictReader(file)

    next(pollreader, None)

    for row in pollreader:
        votecount +=1
        if row['Candidate'] not in candlist:
            candlist.append(row['Candidate'])
            votelist.append(0)
        votelist[candlist.index(row['Candidate'])] +=1
        #if votecount >= 100000: break

    print(f"Election Results")
    print(f"-------------------------------")
    print(f"total votes: {votecount}")
    print(f"-------------------------------")
    for i in range(0,len(candlist)):
        print(f"{candlist[i]}:  {round(votelist[i]*100/votecount,3)}%   ({votelist[i]})")
    mostvotes = max(votelist)
    ind = votelist.index(mostvotes)
    print(f"-------------------------------")
    print(f"Winner: {candlist[ind]} with {votelist[ind]} votes")
    print(f"-------------------------------")


    ElectOutput = open("ElectionOutput.txt","w+")
    ElectOutput.write(f"Election Results\n")
    ElectOutput.write(f"-------------------------------\n")
    ElectOutput.write(f"total votes: {votecount}\n")
    ElectOutput.write(f"-------------------------------\n")
    for i in range(0, len(candlist)):
        ElectOutput.write(f"{candlist[i]}:  {round(votelist[i]*100/votecount,3)}%   ({votelist[i]})\n")
    mostvotes = max(votelist)
    ind = votelist.index(mostvotes)
    ElectOutput.write(f"-------------------------------\n")
    ElectOutput.write(f"Winner: {candlist[ind]} with {votelist[ind]} votes\n")
    ElectOutput.write(f"-------------------------------")
    ElectOutput.close()