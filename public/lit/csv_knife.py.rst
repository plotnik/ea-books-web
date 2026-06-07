..  #!/usr/bin/env python3

CSV Knife
=========

A small command-line utility for applying focused CSV
transformations.

The script reads UTF-8 CSV data with Python's standard :mod:`csv` module.
Input can come from a file path or from standard input by passing ``-``.
Output is written to standard output unless ``--output`` is provided.

**Commands**

``reverse``
    Reverse CSV row order. By default, the first row is treated as a header
    and kept in place. Pass ``--no-header`` to reverse every row.

``remove-columns``
    Remove one or more columns by exact header name.

``truncate``
    Shorten values longer than a configured character limit and append a
    suffix showing how many characters were removed.

    For example, truncating ``"abcdefghijklmnopqrstuvwxyz"`` to ``10``
    characters produces:
    
    .. code-block:: text

        abcdefghij(...16 more)

    The command also prints the maximum value length found in the input.

**Usage**

.. code-block:: bash

    python csv_knife.py --help
    python csv_knife.py reverse input.csv --output reversed.csv
    python csv_knife.py remove-columns input.csv email phone --output public.csv
    python csv_knife.py truncate input.csv 80 --output shortened.csv

----

::

  from __future__ import annotations

  import argparse
  import csv
  import sys
  from pathlib import Path
  from typing import Iterable, TextIO


.. function:: open_input(path: str) -> TextIO

   Open a CSV input stream.

   :param path: File path to read, or ``"-"`` to use :data:`sys.stdin`.
   :returns: A readable text stream.

::

  def open_input(path: str) -> TextIO:
      if path == "-":
          return sys.stdin
      return Path(path).open("r", newline="", encoding="utf-8")


.. function:: open_output(path: str | None) -> TextIO

   Open a CSV output stream.

   :param path: File path to write, ``"-"`` for :data:`sys.stdout`, or
       :data:`None` to use :data:`sys.stdout`.
   :returns: A writable text stream.

::

  def open_output(path: str | None) -> TextIO:
      if path in (None, "-"):
          return sys.stdout
      return Path(path).open("w", newline="", encoding="utf-8")


.. function:: read_csv(path: str) -> list[list[str]]

   Read all rows from a CSV source.

   :param path: File path to read, or ``"-"`` to read from standard input.
   :returns: CSV rows as a list of string lists.

::

  def read_csv(path: str) -> list[list[str]]:
      with open_input(path) as file:
          return list(csv.reader(file))


.. function:: write_csv(rows: Iterable[Iterable[str]], output: str | None) -> None

   Write rows to a CSV destination.

   :param rows: Row values to write.
   :param output: File path to write, ``"-"`` for standard output, or
       :data:`None` for standard output.

::

  def write_csv(rows: Iterable[Iterable[str]], output: str | None) -> None:
      with open_output(output) as file:
          writer = csv.writer(file)
          writer.writerows(rows)


.. function:: reverse_csv(args: argparse.Namespace) -> None

   Run the ``reverse`` subcommand.

   The first row is preserved as a header unless ``args.no_header`` is true.

   :param args: Parsed command-line arguments with ``input``, ``output``, and
       ``no_header`` attributes.

::

  def reverse_csv(args: argparse.Namespace) -> None:
      print(
          f"Reversing CSV rows from {args.input} to {args.output or 'stdout'}",
          file=sys.stderr,
      )
      rows = read_csv(args.input)
      if args.no_header or not rows:
          write_csv(reversed(rows), args.output)
          return

      header, data_rows = rows[0], rows[1:]
      write_csv([header, *reversed(data_rows)], args.output)


.. function:: remove_columns(args: argparse.Namespace) -> None

   Run the ``remove-columns`` subcommand.

   Columns are matched by exact header name. Rows shorter than the header are
   padded with empty strings for any retained column positions they do not
   contain.

   :param args: Parsed command-line arguments with ``input``, ``output``, and
       ``columns`` attributes.
   :raises SystemExit: If any requested column is missing from the header.

::

  def remove_columns(args: argparse.Namespace) -> None:
      print(
          f"Removing columns {args.columns} from CSV "
          f"{args.input} to {args.output or 'stdout'}",
          file=sys.stderr,
      )
      rows = read_csv(args.input)
      if not rows:
          write_csv([], args.output)
          return

      header = rows[0]
      missing_columns = [column for column in args.columns if column not in header]
      if missing_columns:
          joined = ", ".join(missing_columns)
          raise SystemExit(f"Unknown column(s): {joined}")

      columns_to_remove = set(args.columns)
      kept_indexes = [
          index for index, column in enumerate(header) if column not in columns_to_remove
      ]
      filtered_rows = (
          [row[index] if index < len(row) else "" for index in kept_indexes]
          for row in rows
      )
      write_csv(filtered_rows, args.output)


.. function:: truncate_value(value: str, limit: int) -> str

   Return a value shortened to ``limit`` characters when needed.

   Values longer than ``limit`` are returned as ``value[:limit]`` followed by
   ``(...N more)``, where ``N`` is the number of omitted characters.

   :param value: Original CSV value.
   :param limit: Maximum number of original characters to keep.
   :returns: The original value or its truncated representation.

::

  def truncate_value(value: str, limit: int) -> str:
      remaining_chars = len(value) - limit
      if remaining_chars <= 0:
          return value
      return f"{value[:limit]}(...{remaining_chars} more)"


.. function:: truncate_csv(args: argparse.Namespace) -> None

   Run the ``truncate`` subcommand.

   The command prints the maximum value length found in the input to standard
   error, then writes the transformed CSV rows.

   :param args: Parsed command-line arguments with ``input``, ``output``, and
       ``limit`` attributes.

::

  def truncate_csv(args: argparse.Namespace) -> None:
      print(
          f"Truncating CSV values from {args.input} "
          f"to {args.output or 'stdout'} with limit {args.limit}",
          file=sys.stderr,
      )
      rows = read_csv(args.input)
      max_value_length = max((len(value) for row in rows for value in row), default=0)
      print(f"Maximum value length: {max_value_length}", file=sys.stderr)

      truncated_rows = (
          [truncate_value(value, args.limit) for value in row]
          for row in rows
      )
      write_csv(truncated_rows, args.output)


.. function:: build_parser() -> argparse.ArgumentParser

   Build the top-level argument parser and subcommand parsers.

   :returns: Configured :class:`argparse.ArgumentParser` instance.

::

  def build_parser() -> argparse.ArgumentParser:
      parser = argparse.ArgumentParser(
          description="Process CSV files with small command-line transformations."
      )
      subparsers = parser.add_subparsers(dest="command", required=True)

      reverse_parser = subparsers.add_parser(
          "reverse", help="Reverse the order of CSV data rows."
      )
      reverse_parser.add_argument("input", help="Input CSV path, or '-' for stdin.")
      reverse_parser.add_argument(
          "-o", "--output", help="Output CSV path. Defaults to stdout."
      )
      reverse_parser.add_argument(
          "--no-header",
          action="store_true",
          help="Reverse all rows instead of preserving the first row as a header.",
      )
      reverse_parser.set_defaults(func=reverse_csv)

      remove_parser = subparsers.add_parser(
          "remove-columns", help="Remove columns by header name."
      )
      remove_parser.add_argument("input", help="Input CSV path, or '-' for stdin.")
      remove_parser.add_argument(
          "columns", nargs="+", help="One or more column names to remove."
      )
      remove_parser.add_argument(
          "-o", "--output", help="Output CSV path. Defaults to stdout."
      )
      remove_parser.set_defaults(func=remove_columns)

      truncate_parser = subparsers.add_parser(
          "truncate", help="Truncate values longer than the specified limit."
      )
      truncate_parser.add_argument("input", help="Input CSV path, or '-' for stdin.")
      truncate_parser.add_argument(
          "limit", type=int, help="Maximum number of original characters to keep."
      )
      truncate_parser.add_argument(
          "-o", "--output", help="Output CSV path. Defaults to stdout."
      )
      truncate_parser.set_defaults(func=truncate_csv)

      return parser


.. function:: main() -> None

   Parse command-line arguments and dispatch to the selected subcommand.

::

  def main() -> None:
      parser = build_parser()
      args = parser.parse_args()
      if getattr(args, "limit", 0) < 0:
          parser.error("limit must be greater than or equal to 0")
      args.func(args)


  if __name__ == "__main__":
      main()
