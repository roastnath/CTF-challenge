# Money Follows My Brothaa

A suspicious transaction statement from BrothaaPay has been recovered. The statement looks ordinary, but some information hidden inside the document may point toward something more interesting.

Investigate the provided artifact, follow the clues, and uncover what BrothaaPay's document viewer is hiding.

`difficulty: Medium` <br>
`author: Jai`

## Flag

```text
EH4X{money_follows_my_brothaa}
```

## Solution

Start by examining the provided PDF using a forensic metadata tool such as `exiftool`.

```bash
exiftool brothaa_statement.pdf
```

The PDF metadata contains a clue pointing toward the BrothaaPay Static Viewer.

The website contains a Statement Viewer that retrieves documents using the `X-Statement-File` HTTP header.

A normal request can be tested with:

```bash
curl.exe -H "X-Statement-File: notice.txt" http://127.0.0.1:5000/view
```

The application attempts to restrict access to files outside the public document directory.

Testing a normal path traversal such as:

```text
../private/archive/final.txt
```

is rejected.

The intended vulnerability is based around path validation and URL percent-encoding. Instead of sending the literal `..`, the dots can be represented as:

```text
%2e%2e
```

After URL decoding, this becomes:

```text
..
```

This can be used to traverse outside the intended public directory and reach the hidden file containing the flag.

The challenge therefore combines a small forensic investigation with a web path traversal vulnerability.

The forensic component provides the clue, while the web component provides the actual exploitation step.
