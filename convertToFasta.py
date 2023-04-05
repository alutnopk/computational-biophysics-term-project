from uniprotGet import getFasta

if __name__ == "__main__":
    filename = input("Enter name of file containing protein IDs: ")
    outFile = input("Enter name of output file: ")
    uniprotIDs = []
    with open(filename, "r") as f:
        for line in f:
            line = line[:-1]
            uniprotIDs.append(line)
    getFasta(uniprotIDs, outFile)