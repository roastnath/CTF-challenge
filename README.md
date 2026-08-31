# Money Follows My Brothaa

A suspicious transaction statement from BrothaaPay has been recovered. The statement looks ordinary, but some information hidden inside the document may point toward something more interesting.

Investigate the provided artifact, follow the clues, and uncover what BrothaaPay's document viewer is hiding.

`difficulty: Medium` <br>
`author: Codenath`

## Flag

```text
FLAG{M0N3Y_D035'N7_F0LL0W5_BR07H44_K33PW0RK1NG}
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


##solution

## Solution

Run `exiftool` on the provided PDF to inspect its metadata and find the clue pointing to the BrothaaPay Static Viewer. Investigating the viewer reveals the `X-Statement-File` header used to retrieve documents.

A direct `../` path traversal is blocked, but URL-encoding the dots as `%2e%2e` bypasses the validation. This allows traversal to the hidden `private/archive/final.txt` file, which contains the flag.

```text
FLAG{M0N3Y_D035'N7_F0LL0W5_BR07H44_K33PW0RK1NG}
```
