from flask import Flask, render_template, send_file, request
from urllib.parse import unquote
from io import BytesIO

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/transactions")
def transactions():
    transactions = [
        {
            "id": "TXN-1842",
            "description": "Brothaa Foods",
            "amount": "₹2,500",
            "status": "Completed"
        },
        {
            "id": "TXN-2917",
            "description": "Brothaa Enterprises",
            "amount": "₹8,200",
            "status": "Completed"
        },
        {
            "id": "TXN-4471",
            "description": "Unknown Transfer",
            "amount": "₹15,000",
            "status": "Completed"
        }
    ]

    return render_template(
        "transactions.html",
        transactions=transactions
    )

@app.route("/statement")
def statement():
    return send_file(
        "evidence/brothaa_statement.pdf",
        mimetype="application/pdf",
        as_attachment=True,
        download_name="brothaa_statement.pdf"
    )

@app.route("/api/document")
def document_api():

    encoded_file = request.headers.get("X-Document")

    if not encoded_file:
        return "Missing document", 400

    print("Raw:", repr(encoded_file))

    # Deliberately vulnerable CTF logic
    if ".." in encoded_file:
        return "Invalid document", 403

    decoded_file = unquote(encoded_file)

    print("Decoded:", repr(decoded_file))

    return send_file(
        f"public/{decoded_file}",
        mimetype="text/plain"
    )


@app.route("/viewer")
def viewer():
    return render_template("viewer.html")


@app.route("/view")
def view_file():
    from urllib.parse import unquote

    filename = request.headers.get("X-Statement-File")

    if not filename:
        return "Missing X-Statement-File header", 400

    print("Raw filename:", repr(filename))

    # Deliberately vulnerable:
    # Security check happens BEFORE decoding.
    if ".." in filename:
        return "Invalid filename", 403

    filename = unquote(filename)

    print("Decoded filename:", repr(filename))

    return send_file(
        f"public/{filename}",
        mimetype="text/plain"
    )
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )