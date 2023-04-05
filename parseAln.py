# Read lines from a .aln file in which each line is either empty or contains name, sequence as a multiple space separated pair of strings
# Return a dictionary of name:sequence pairs
def readAln(alnFile, outFile):
    aln = {}
    with open(alnFile) as f:
        for line in f:
            if line.strip():
                name, seq = line.split()
                # If aln[name] is already defined, append seq to it
                if name in aln:
                    aln[name] += seq
                # Otherwise, define aln[name] as seq
                else:
                    aln[name] = seq
    
    # Write each sequence to outFile
    with open(outFile, 'w') as f:
        for name in aln:
            f.write(aln[name] + '\n')

if __name__ == "__main__":
    AlnFile = input("Enter the name of the alignment file: ")
    OutFile = input("Enter the name of the output file: ")
    readAln(AlnFile, OutFile)
