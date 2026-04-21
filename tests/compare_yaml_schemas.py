#!/usr/bin/env python3
"""
Compare two SDM schema YAML files and report differences in tables, columns
(optional), primary keys, and constraint definitions.

Usage:
    ./compare_yaml_schemas.py [--ignore-columns]
        path/to/schema_a.yaml path/to/schema_b.yaml
"""

import argparse
from dataclasses import dataclass
from enum import IntEnum
from pathlib import Path

import yaml


class ExitCode(IntEnum):
    SUCCESS = 0
    INVALID_INPUT = 1
    DIFFS_FOUND = 2


@dataclass(frozen=True)
class Constraint:
    name: str
    ctype: str
    columns: tuple[str, ...]
    referenced: tuple[str, ...]


@dataclass
class TableSummary:
    name: str
    primary: tuple[str, ...]
    columns: set[str]
    constraints: dict[str, Constraint]


def load_schema(path: Path) -> dict[str, TableSummary]:
    """Load a YAML schema file into table summaries keyed by table name."""
    data = yaml.safe_load(path.read_text())
    tables: dict[str, TableSummary] = {}
    for table in data.get("tables", []):
        name = table["name"]
        primary = tuple(table.get("primaryKey", []))
        columns = {col["name"] for col in table.get("columns", []) if isinstance(col, dict) and "name" in col}
        constraints = _build_constraints_dict(table.get("constraints", []))
        tables[name] = TableSummary(name=name, primary=primary, columns=columns, constraints=constraints)
    return tables


def _build_constraints_dict(constraints: list[dict]) -> dict[str, Constraint]:
    """Normalize constraint dictionaries into a name-keyed mapping."""
    normalized: dict[str, Constraint] = {}
    for con in constraints:
        name = con.get("name")
        if not name:
            continue
        ctype = con.get("@type", "")
        cols = tuple(con.get("columns", []))
        refs = tuple(con.get("referencedColumns", []))
        normalized[name] = Constraint(name=name, ctype=ctype, columns=cols, referenced=refs)
    return normalized


def compare_tables(
    left: dict[str, TableSummary], right: dict[str, TableSummary], *, ignore_columns: bool
) -> list[str]:
    """Compare two schema table mappings and return human-readable diffs."""
    messages: list[str] = []
    only_left = sorted(set(left) - set(right))
    only_right = sorted(set(right) - set(left))
    if only_left:
        messages.append(f"Tables only in A: {', '.join(only_left)}")
    if only_right:
        messages.append(f"Tables only in B: {', '.join(only_right)}")

    for name in sorted(set(left) & set(right)):
        a = left[name]
        b = right[name]
        if a.primary != b.primary:
            messages.append(f"{name}: primaryKey differs A={a.primary} B={b.primary}")
        if not ignore_columns:
            cols_left = a.columns - b.columns
            cols_right = b.columns - a.columns
            if cols_left:
                messages.append(f"{name}: columns only in A: {', '.join(sorted(cols_left))}")
            if cols_right:
                messages.append(f"{name}: columns only in B: {', '.join(sorted(cols_right))}")

        cons_left = set(a.constraints)
        cons_right = set(b.constraints)
        missing_in_b = cons_left - cons_right
        missing_in_a = cons_right - cons_left
        if missing_in_b:
            messages.append(f"{name}: constraints only in A: {', '.join(sorted(missing_in_b))}")
        if missing_in_a:
            messages.append(f"{name}: constraints only in B: {', '.join(sorted(missing_in_a))}")

        for cname in sorted(cons_left & cons_right):
            ac = a.constraints[cname]
            bc = b.constraints[cname]
            if (ac.ctype, ac.columns, ac.referenced) != (bc.ctype, bc.columns, bc.referenced):
                messages.append(
                    f"{name}:{cname} differs "
                    f"A=(type={ac.ctype}, cols={ac.columns}, refs={ac.referenced}) "
                    f"B=(type={bc.ctype}, cols={bc.columns}, refs={bc.referenced})"
                )
    return messages


def main() -> int:
    """CLI entry point for YAML schema comparison."""
    parser = argparse.ArgumentParser(description="Compare two SDM schema YAML files.")
    parser.add_argument("--ignore-columns", action="store_true", help="Ignore column list differences.")
    parser.add_argument("schema_a", type=Path)
    parser.add_argument("schema_b", type=Path)
    args = parser.parse_args()

    a_path = args.schema_a.expanduser()
    b_path = args.schema_b.expanduser()
    if not a_path.is_file() or not b_path.is_file():
        print(f"Both inputs must be files. Got: {a_path} and {b_path}")
        return ExitCode.INVALID_INPUT

    left = load_schema(a_path)
    right = load_schema(b_path)
    diffs = compare_tables(left, right, ignore_columns=args.ignore_columns)
    if diffs:
        print("Differences found:")
        for line in diffs:
            print(f"- {line}")
        return ExitCode.DIFFS_FOUND

    if args.ignore_columns:
        print("Schemas match on tables, primary keys, and constraints.")
    else:
        print("Schemas match on tables, columns, primary keys, and constraints.")
    return ExitCode.SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
