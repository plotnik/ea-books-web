Split Log
=========

This script splits a given log file into multiple output files based on a list
of signatures provided in the text file ``split_log.txt``.

**Behavior**

- The input log is processed line by line.
- Log contents are written to the current output file until a matching
  signature is found.
- When a signature is found:

    - the current output file is closed;
    - a new output file is created;
    - the line containing the signature is written as the first line of the new output file.

**Output Files**

Output files are named using a three-digit sequence number followed by the
original log file name:

.. code-block:: console

    001-{log_file}
    002-{log_file}
    003-{log_file}

For example, if the input log file is named ``application.log``, the generated
files will be:

.. code-block:: console

    001-application.log
    002-application.log
    003-application.log

**Signature File**

The list of signatures must be stored in a text file named ``split_log.txt``.

Each signature is used to determine where the log should be split.


----

::

  import argparse
  from pathlib import Path

.. function:: load_signatures(signature_file: Path) -> list[str]

::

  def load_signatures(signature_file: Path) -> list[str]:
    signatures = []

    with signature_file.open("r", encoding="utf-8") as f:
        for line in f:
            signature = line.rstrip("\n")
            if signature:
                signatures.append(signature)

    return signatures

.. function:: line_contains_signature(line: str, signatures: list[str]) -> bool

::

  def line_contains_signature(line: str, signatures: list[str]) -> bool:
    return any(signature in line for signature in signatures)

.. function:: output_path(output_dir: Path, index: int, log_file: Path) -> Path

::

  def output_path(output_dir: Path, index: int, log_file: Path) -> Path:
    return output_dir / f"{index:03d}-{log_file.name}"

.. function:: split_log(log_file: Path, signature_file: Path, output_dir: Path)

::

  def split_log(log_file: Path, signature_file: Path, output_dir: Path) -> None:
    signatures = load_signatures(signature_file)

    if not signatures:
        raise ValueError(f"No signatures found in {signature_file}")

    output_dir.mkdir(parents=True, exist_ok=True)

    part_index = 1
    current_output = output_path(output_dir, part_index, log_file)
    out = current_output.open("w", encoding="utf-8")
    print(current_output)

    try:
        with log_file.open("r", encoding="utf-8", errors="replace") as log:
            for line in log:
                if line_contains_signature(line, signatures):
                    out.close()

                    part_index += 1
                    current_output = output_path(output_dir, part_index, log_file)
                    print(current_output)
                    out = current_output.open("w", encoding="utf-8")

                out.write(line)
    finally:
        out.close()

.. function:: main()

::

  def main() -> None:
    parser = argparse.ArgumentParser(
        description="Split a log file into numbered parts using signatures from split_log.txt."
    )

    parser.add_argument(
        "log_file",
        help="Path to the log file to split.",
    )

    parser.add_argument(
        "-s",
        "--signatures",
        default="split_log.txt",
        help="Path to the signatures file. Default: split_log.txt",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        default=".",
        help="Directory where split files will be written. Default: current directory",
    )

    args = parser.parse_args()

    split_log(
        log_file=Path(args.log_file),
        signature_file=Path(args.signatures),
        output_dir=Path(args.output_dir),
    )


  if __name__ == "__main__":
    main()