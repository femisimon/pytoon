import argparse
from .api import encode, decode

def main():
    parser = argparse.ArgumentParser(description="PyTOON CLI")
    parser.add_argument("file", help="Input file (.json or .toon)")
    parser.add_argument("--decode", action="store_true", help="Decode TOON")
    parser.add_argument("--encode", action="store_true", help="Encode JSON")
    parser.add_argument("-o", "--out", help="Output file")

    args = parser.parse_args()

    with open(args.file) as f:
        text = f.read()

    if args.decode:
        result = decode(text)
    elif args.encode:
        import json
        obj = json.loads(text)
        result = encode(obj)
    else:
        raise SystemExit("Specify --encode or --decode")

    if args.out:
        with open(args.out, "w") as f:
            f.write(result)
    else:
        print(result)

if __name__ == "__main__":
    main()
