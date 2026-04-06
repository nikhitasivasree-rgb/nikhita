# G-Quadruplex Prediction Tool

import re

def analyze_sequence(sequence):
    sequence = sequence.upper().replace(" ", "")
    
    # G-quadruplex pattern
    pattern = r"G{3,}[ATGC]{1,7}G{3,}[ATGC]{1,7}G{3,}[ATGC]{1,7}G{3,}"
    
    matches = re.findall(pattern, sequence)
    
    # Sequence length
    length = len(sequence)
    
    # GC Content
    gc_count = sequence.count("G") + sequence.count("C")
    gc_content = (gc_count / length) * 100 if length > 0 else 0
    
    print("\n--- Analysis Result ---")
    print("Sequence Length:", length)
    print("GC Content: {:.2f}%".format(gc_content))
    
    if matches:
        print("\nG-Quadruplex Motifs Found:")
        for i, m in enumerate(matches, 1):
            print(f"{i}. {m}")
    else:
        print("\nNo G-Quadruplex motifs found.")


# User input
dna = input("Enter DNA Sequence: ")

analyze_sequence(dna)
