import streamlit as st
import re

# -------------------------------
# Functions
# -------------------------------

def validate_sequence(seq):
    return bool(re.fullmatch(r"[ATGCatgc]+", seq))


def gc_content(seq):
    gc = seq.count('G') + seq.count('C')
    return round((gc / len(seq)) * 100, 2)


def reverse_complement(seq):
    complement = str.maketrans("ATGC", "TACG")
    return seq.translate(complement)[::-1]


def find_g_quadruplex(seq):
    pattern = r"(G{3,}.{1,7}G{3,}.{1,7}G{3,}.{1,7}G{3,})"
    matches = [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, seq)]
    return matches


def highlight_sequence(seq, motifs):
    highlighted = seq
    offset = 0
    for start, end, motif in motifs:
        start += offset
        end += offset
        tag = f"<span style='background-color:yellow'>{motif}</span>"
        highlighted = highlighted[:start] + tag + highlighted[end:]
        offset += len(tag) - len(motif)
    return highlighted


# -------------------------------
# UI
# -------------------------------

st.set_page_config(page_title="G-Quadruplex Predictor", layout="centered")

st.title("🧬 G-Quadruplex Prediction Tool")

# Input
sequence = st.text_area("Enter DNA Sequence", height=150)

# File Upload
uploaded_file = st.file_uploader("Upload sequence file (.txt)", type=["txt"])

if uploaded_file:
    sequence = uploaded_file.read().decode("utf-8").replace("\n", "").upper()
    st.success("File uploaded successfully!")

# Example Button
if st.button("Use Example"):
    sequence = "GGGTTAGGGTTAGGGTTAGGG"
    st.rerun()

# Analyze
if st.button("Analyze"):

    if not sequence:
        st.error("Please enter a sequence")
    else:
        seq = sequence.upper().strip()

        if not validate_sequence(seq):
            st.error("Invalid DNA sequence (only A, T, G, C allowed)")
        else:
            length = len(seq)
            gc = gc_content(seq)
            rev = reverse_complement(seq)
            motifs = find_g_quadruplex(seq)

            st.subheader("📊 Results")

            col1, col2 = st.columns(2)
            col1.metric("Sequence Length", length)
            col2.metric("GC Content (%)", gc)

            st.write("🔁 Reverse Complement:")
            st.code(rev)

            if motifs:
                st.success(f"✅ Found {len(motifs)} G-Quadruplex motif(s)")
                highlighted = highlight_sequence(seq, motifs)
                st.markdown(highlighted, unsafe_allow_html=True)

                st.write("📍 Motif Positions:")
                for m in motifs:
                    st.write(f"Start: {m[0]}, End: {m[1]}, Motif: {m[2]}")
            else:
                st.warning("No G-Quadruplex motifs found.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit 🧬")
