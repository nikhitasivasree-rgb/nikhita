import streamlit as st
import re

st.title("G-Quadruplex Prediction Tool")

dna = st.text_area("Enter DNA Sequence")

if st.button("Analyze"):
    if dna:
        sequence = dna.upper().replace(" ", "")

        pattern = r"G{3,}[ATGC]{1,7}G{3,}[ATGC]{1,7}G{3,}[ATGC]{1,7}G{3,}"
        matches = re.findall(pattern, sequence)

        length = len(sequence)

        gc_count = sequence.count("G") + sequence.count("C")
        gc_content = (gc_count / length) * 100 if length > 0 else 0

        st.subheader("Results")
        st.write("Sequence Length:", length)
        st.write(f"GC Content: {gc_content:.2f}%")

        if matches:
            st.write("### G-Quadruplex Motifs Found:")
            for i, m in enumerate(matches, 1):
                st.write(f"{i}. {m}")
        else:
            st.write("No G-Quadruplex motifs found.")
    else:
        st.warning("Please enter a DNA sequence")
