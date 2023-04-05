import random

def symbolToNumber(symbol):
    if symbol == 'A':
        return 0
    elif symbol == 'R':
        return 1
    elif symbol == 'N':
        return 2
    elif symbol == 'D':
        return 3
    elif symbol == 'C':
        return 4
    elif symbol == 'Q':
        return 5
    elif symbol == 'E':
        return 6
    elif symbol == 'G':
        return 7
    elif symbol == 'H':
        return 8
    elif symbol == 'I':
        return 9
    elif symbol == 'L':
        return 10
    elif symbol == 'K':
        return 11
    elif symbol == 'M':
        return 12
    elif symbol == 'F':
        return 13
    elif symbol == 'P':
        return 14
    elif symbol == 'S':
        return 15
    elif symbol == 'T':
        return 16
    elif symbol == 'W':
        return 17
    elif symbol == 'Y':
        return 18
    elif symbol == 'V':
        return 19
    else:
        return 20


def numberToSymbol(number):
    if number == 0:
        return 'A'
    elif number == 1:
        return 'R'
    elif number == 2:
        return 'N'
    elif number == 3:
        return 'D'
    elif number == 4:
        return 'C'
    elif number == 5:
        return 'Q'
    elif number == 6:
        return 'E'
    elif number == 7:
        return 'G'
    elif number == 8:
        return 'H'
    elif number == 9:
        return 'I'
    elif number == 10:
        return 'L'
    elif number == 11:
        return 'K'
    elif number == 12:
        return 'M'
    elif number == 13:
        return 'F'
    elif number == 14:
        return 'P'
    elif number == 15:
        return 'S'
    elif number == 16:
        return 'T'
    elif number == 17:
        return 'W'
    elif number == 18:
        return 'Y'
    elif number == 19:
        return 'V'
    else:
        return '-'

# Take k as lenght of motif
# Take t as number of sequences
# Take sequences as a list of strings that are the sequences

# From each sequence, randomly select a k-mer
# Return a list of k-mers
def possibleMotifs(sequences, motifs, k):
    # If the motifs[i] for sequence[i] is empty then we randomly select a k-mer
    possMotifs = []
    for i in range(0, len(sequences)):
        if motifs[i] == -1:
            sequence = sequences[i]
            start = random.randint(0, len(sequence) - k)
            while 1:
                if sequence[start] == '-':
                    start = random.randint(0, len(sequence) - k)
                else:
                    break
            possMotifs.append(start)
        else:
            possMotifs.append(motifs[i])
    return possMotifs


# Now we make the profile matrix
def CreateprofileMatrix(sequences, motifs, k, t, b):
    possMotifs = possibleMotifs(sequences, motifs, k)
    # Create a table of probabilities
    table = []
    for i in range(0, 21):
        table.append([0] * (k+1))

    # For each sequence
    for i in range(0, t):
        start = possMotifs[i]
        end = start + k - 1
        sequence = sequences[i]
        for j in range(0, len(sequence)):
            if j >= start and j <= end:
                if sequence[j] != '-':
                    table[symbolToNumber(sequence[j])][j-start+1] += 1
            else:
                if sequence[j] != '-':
                    table[symbolToNumber(sequence[j])][0] += 1

    # Create new table of same dimensions for probabilities
    profileMatrix = []
    for i in range(0, 21):
        profileMatrix.append([0] * (k+1))

    # Calculate the probabilities as
    # nonMotifElems = sum(table[i][0])
    # B = sum(b)
    # P(i, 0) = (table(i,0) + b[i]) / (nonMotifElems + B)
    # P(i, j) = (table(i,j) + b[i]) / (t - 1 + B)
    nonMotifElems = 0
    B = 0
    for i in range(0, 21):
        nonMotifElems += table[i][0]
        B = B + b[i]

    
    for i in range(0, 21):
        profileMatrix[i][0] = (table[i][0] + b[i]) / (nonMotifElems + B)
        for j in range(1, k+1):
            profileMatrix[i][j] = (table[i][j] + b[i]) / (t - 1 + B)

    gapIndex = symbolToNumber('-')
    for i in range(0, k+1):
        profileMatrix[gapIndex][i] = 0

    return profileMatrix


def sampler(sequences, motifs, k, t, b, N):
    # Runs N iterations of Gibbs Sampler
    for i in range(0, N):
        # In each iteration we have to select a random sequence
        # and calculate the probability table for the remaining sequences
        # and then select a new motif for the selected sequence

        # Select a random sequence
        randomSequence = random.randint(0, t-1)
        # Create a list of sequences without the selected sequence
        remainingSequences = []
        for i in range(0, t):
            if i != randomSequence:
                remainingSequences.append(sequences[i])

        # Create a probability table for the remaining sequences
        profileMatrix = CreateprofileMatrix(remainingSequences, motifs, k, t-1, b)

        # Calculate the probability of each k-mer in the selected sequence
        # and select a new motif for the selected sequence
        probs = []
        for j in range(0, len(sequences[randomSequence]) - k + 1):
            prob = 1
            if sequences[randomSequence][j] == '-':
                prob = 0
            else:
                for l in range(0, k):
                    prob *= profileMatrix[symbolToNumber(sequences[randomSequence][j+l])][l+1]
            probs.append(prob)
        # Normalize the probabilities
        total = sum(probs)
        for j in range(0, len(probs)):
            probs[j] /= total
        # Now that we have the probs, we select a new motif start position for the selected sequence
        # We use the random.choices function to select a new motif start position
        motifStartPosition = random.choices(range(0, len(sequences[randomSequence]) - k + 1), weights=probs, k=1)[0]
        # set motifs[randomSequence] to motifStartPosition
        motifs[randomSequence] = motifStartPosition


if __name__ == "__main__":
    # Read sequences from the file sequences.txt
    sequences = []
    with open('sequences1.txt') as f:
        for line in f:
            sequences.append(line.strip())
    # We have a list of motifs for each sequence
    # Initially all motifs are empty
    motifs = []
    for i in range(0, len(sequences)):
        motifs.append(-1)
    # Call a function called sampler
    k = 15
    t = len(sequences)
    b = [50, 50, 200, 200, 400, 150, 200, 75, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 200, 50, 0]
    N = 10000
    sampler(sequences, motifs, k, t, b, N)
    with open("output.txt", "w") as f:
        for i in range(0, len(sequences)):
            # write sequences[i][motifs[i]:motifs[i]+k]
            f.write(sequences[i][motifs[i]:motifs[i]+k] + "\n")
