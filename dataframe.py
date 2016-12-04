import pandas  as pd

# Product_DF = pd.read_csv("Final.csv")
list = [[]]
i, j = 0,0
with open("Final.csv", "r")as f:
    for line in f:

        line = line.split(",")

        for point in line:
            list[i].append(point)

    i += 1


print(list)