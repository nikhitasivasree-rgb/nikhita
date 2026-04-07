from flask import Flask, render_template, request, jsonify, send_file
import re
import io
import csv

app = Flask(__name__)

# -------------------------------
# Utility Functions
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
    """
    Simple G4 motif pattern:
    G{3,}N{1,7}G{3,}N{1,7}G{3,}N{1,7}G{3,}
    """
    pattern = r"(G{3,}.{1,7}G{3,}.{1,7}G{3,}.{1,7}G{3,})"
    matches = [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, seq)]
    return matches


def highlight_sequence(seq, motifs):
    highlighted = seq
    offset = 0
    for start, end, motif in motifs:
        start += offset
        end += offset
        tag = f"<mark>{motif}</mark>"
        highlighted = highlighted[:start] + tag + highlighted[end:]
        offset += len(tag) - len(motif)
    return highlighted


# -------------------------------
# Routes
# -------------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    seq = request.form.get("sequence", "").upper().strip()

    if not seq:
        return jsonify({"error": "No sequence provided"})

    if not validate_sequence(seq):
        return jsonify({"error": "Invalid DNA sequence (only A, T, G, C allowed)"})

    length = len(seq)
    gc = gc_content(seq)
    rev_comp = reverse_complement(seq)
    motifs = find_g_quadruplex(seq)

    highlighted = highlight_sequence(seq, motifs) if motifs else seq

    return jsonify({
        "length": length,
        "gc_content": gc,
        "reverse_complement": rev_comp,
        "motifs": motifs,
        "highlighted_sequence": highlighted
    })


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"})

    content = file.read().decode("utf-8")
    seq = "".join(content.split()).upper()

    if not validate_sequence(seq):
        return jsonify({"error": "Invalid sequence in file"})

    return jsonify({"sequence": seq})


@app.route("/download", methods=["POST"])
def download():
    data = request.json

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["Metric", "Value"])
    writer.writerow(["Sequence Length", data["length"]])
    writer.writerow(["GC Content", data["gc_content"]])
    writer.writerow(["Reverse Complement", data["reverse_complement"]])
    writer.writerow(["Motif Count", len(data["motifs"])])

    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="results.csv"
    )


# -------------------------------
# Run App
# -------------------------------

if __name__ == "__main__":
    app.run(debug=True)
