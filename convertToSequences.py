from uniprotGet import readDataset

if __name__ == "__main__":
    dataset = input("Enter name of file containing protein IDs: ")
    outFile = input("Enter name of output file: ")
    readDataset(dataset, outFile)