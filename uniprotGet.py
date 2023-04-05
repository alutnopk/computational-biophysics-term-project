import requests as r


def getSequence(uniprotID):
    #get the sequence from the uniprot database
    url = "http://www.uniprot.org/uniprot/" + uniprotID + ".fasta"
    response = r.post(url)
    html = ''.join(response.text)
    html = html.splitlines()
    html = html[1:]
    html = ''.join(html)
    return html

def getFasta(uniprotIDs):
    # get the fasta file from the uniprot database
    url = "http://www.uniprot.org/uniprot/"
    for uniprotID in uniprotIDs:
        newUrl = url
        newUrl += uniprotID + ".fasta"
        print(newUrl)
        response = r.post(newUrl)
        html = ''.join(response.text)
        # Write to fasta file
        with open("insulins.fasta", "a") as file:
            file.write(html)
    
# Read the file "dataset" given as parameter
# For each line call the getSequence function
# Return a list of sequences
def readDataset(dataset):
    sequences = []
    with open(dataset, 'r') as file:
        for line in file:
            # remove linebreak which is the last character of the string
            line = line[:-1]
            sequence = getSequence(line)
            sequences.append(sequence)
    return sequences


if __name__ == "__main__":
    # Read uniport IDs from file
    uniprotIDs = []
    with open("insulin2.txt", "r") as file:
        for line in file:
            line = line[:-1]
            uniprotIDs.append(line)
    getFasta(uniprotIDs)
