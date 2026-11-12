#!/usr/bin/env python3
"""Verify this release offline with Python 3.9+ and the standard library.

Reads only this package. Does not write files or access the network or original
data. Hash consistency is not proof of scientific validity or authenticity:
SHA256SUMS.txt must itself come from a trusted copy of the release.
"""

import csv
import hashlib
import os
from pathlib import Path
import re
import stat
import sys
from decimal import Decimal, InvalidOperation


EXPECTED_DATASETS = 12
EXPECTED_OBSERVATIONS = 3190
EXPECTED_ALIASES = 3
CHECKSUM_FILE = "SHA256SUMS.txt"
IGNORED_NAMES = {".git", "__pycache__"}
HASH_PATTERN = re.compile(r"[0-9a-fA-F]{64}\Z")
ID_PATTERN = re.compile(r"[a-z0-9]+(?:_[a-z0-9]+)*\Z")
NUMBER_PATTERN = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?\Z")
MANIFEST_COLUMNS = [
    "dataset_id", "file", "source_groups", "algorithm_label", "label_basis",
    "rows", "first_step", "last_step", "step_interval", "elapsed_span_s",
    "value_min", "value_max", "metric_status", "source_sha256",
    "published_sha256",
]
ALIAS_COLUMNS = ["source_group_alias", "canonical_dataset_id", "evidence"]
DATA_COLUMNS = ["step", "value", "elapsed_wall_time_s"]
FILE_MANIFEST_COLUMNS = [
    "dataset_id", "file", "category", "rows", "columns", "source_files",
    "published_sha256",
]
CONDITIONS = {
    "2D Drawings",
    "MR Interface",
    "MR-Controlled Cable Robot",
    "MR-Controlled Cable Robot with ML Agents",
}
TASK_COLUMNS = [
    "condition", "record_index", "completion_time_min", "assistance_requests",
    "completion_time_source_cell", "assistance_source_cell",
]
ACCURACY_COLUMNS = [
    "condition", "record_index", "incorrect_placements", "total_components",
    "correct_placements", "accuracy_proportion", "incorrect_placements_source_cell",
    "accuracy_formula_source_cell",
]
QR_TRIAL_COLUMNS = [
    "source_block", "qr_side_length_cm", "trial_index", "recognition_time_s",
    "detection_distance_m", "time_source_cell", "distance_source_cell",
]
QR_RANGE_COLUMNS = [
    "qr_side_length_cm", "environment", "min_detectable_distance_m",
    "max_detectable_distance_m", "min_distance_source_cell", "max_distance_source_cell",
]


class VerificationError(Exception):
    """A package check failed."""


def require(condition, message):
    if not condition:
        raise VerificationError(message)


def safe_relative_path(value):
    """Accept portable relative file paths, never paths outside the package."""
    require(isinstance(value, str) and value, "Empty relative path")
    require(
        re.fullmatch(r"[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*", value) is not None,
        "Unsafe relative path: {!r}".format(value),
    )
    parts = value.split("/")
    require(
        all(part not in {".", ".."} | IGNORED_NAMES for part in parts),
        "Excluded or traversing path: {!r}".format(value),
    )
    require(
        all(not part.endswith(".") for part in parts),
        "Nonportable relative path: {!r}".format(value),
    )
    reserved = {"CON", "PRN", "AUX", "NUL"}
    reserved.update("COM{}".format(i) for i in range(1, 10))
    reserved.update("LPT{}".format(i) for i in range(1, 10))
    require(
        all(part.split(".", 1)[0].upper() not in reserved for part in parts),
        "Reserved device path: {!r}".format(value),
    )
    return value


def checked_entry(root, entry):
    info = entry.lstat()
    require(
        not stat.S_ISLNK(info.st_mode)
        and not (getattr(info, "st_file_attributes", 0) & 0x400),
        "Links or filesystem reparse points are not allowed: {}".format(entry.name),
    )
    try:
        entry.resolve().relative_to(root)
    except ValueError:
        raise VerificationError("Path escapes the package: {}".format(entry.name))
    require(
        stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode),
        "Unsupported filesystem entry: {}".format(entry.name),
    )


def package_members(root):
    members = set()
    folded = set()

    def walk_error(error):
        raise error

    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        dirs[:] = sorted(name for name in dirs if name not in IGNORED_NAMES)
        for name in dirs:
            entry = Path(directory) / name
            checked_entry(root, entry)
            safe_relative_path(entry.relative_to(root).as_posix())
        for name in sorted(files):
            if name in IGNORED_NAMES:
                continue
            entry = Path(directory) / name
            checked_entry(root, entry)
            relative = safe_relative_path(entry.relative_to(root).as_posix())
            require(relative.casefold() not in folded, "Case-colliding package path: " + relative)
            folded.add(relative.casefold())
            members.add(relative)
    return members


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def checksum_inventory(root, members):
    require(CHECKSUM_FILE in members, "Missing " + CHECKSUM_FILE)
    listed = {}
    folded = set()
    with (root / CHECKSUM_FILE).open(encoding="utf-8", newline="") as stream:
        for line_number, line in enumerate(stream, 1):
            line = line.rstrip("\r\n")
            if not line:
                continue
            match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](.+)", line)
            require(match is not None, "Malformed checksum line {}".format(line_number))
            digest, relative = match.groups()
            relative = safe_relative_path(relative)
            require(relative != CHECKSUM_FILE, "Checksum inventory must not hash itself")
            require(relative.casefold() not in folded, "Duplicate checksum path: " + relative)
            listed[relative] = digest.lower()
            folded.add(relative.casefold())
    expected = members - {CHECKSUM_FILE}
    missing = sorted(set(listed) - expected)
    unexpected = sorted(expected - set(listed))
    require(not missing, "Files listed but missing: " + ", ".join(missing))
    require(not unexpected, "Unexpected files not listed in checksums: " + ", ".join(unexpected))
    for relative, expected_hash in sorted(listed.items()):
        require(sha256(root / relative) == expected_hash, "SHA-256 mismatch: " + relative)
    return listed


def read_table(path, expected_columns, allow_empty=()):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader, None)
        require(header == expected_columns, "Unexpected columns: " + path.name)
        records = []
        for row in reader:
            location = "{} line {}".format(path.name, reader.line_num)
            require(len(row) == len(header), "Malformed row: " + location)
            require(all(cell != "" or column in allow_empty for column, cell in zip(header, row)),
                    "Empty cell: " + location)
            records.append(dict(zip(header, row)))
    require(records, "Empty table: " + path.name)
    return records


def integer(value, location):
    require(re.fullmatch(r"[0-9]+", value) is not None, "Invalid integer: " + location)
    return int(value)


def number(value, location):
    require(
        len(value) <= 1024 and NUMBER_PATTERN.fullmatch(value) is not None,
        "Invalid numeric value: " + location,
    )
    parsed = Decimal(value)
    require(parsed.is_finite(), "Non-finite value: " + location)
    return parsed


def verify_dataset(root, record, hashes):
    dataset_id = record["dataset_id"]
    require(ID_PATTERN.fullmatch(dataset_id) is not None, "Invalid dataset identifier")
    relative = safe_relative_path(record["file"])
    require(relative == "data/training/{}.csv".format(dataset_id), "Dataset path/identifier mismatch: " + dataset_id)
    require(relative in hashes, "Dataset missing from checksums: " + relative)
    for field in ("source_sha256", "published_sha256"):
        require(HASH_PATTERN.fullmatch(record[field]) is not None, "Malformed {}: {}".format(field, dataset_id))
    require(record["published_sha256"].lower() == hashes[relative], "Manifest hash mismatch: " + dataset_id)

    rows = read_table(root / relative, DATA_COLUMNS)
    count = integer(record["rows"], dataset_id + " rows")
    first_step = integer(record["first_step"], dataset_id + " first_step")
    last_step = integer(record["last_step"], dataset_id + " last_step")
    interval = integer(record["step_interval"], dataset_id + " step_interval")
    require(len(rows) == count, "Observation count mismatch: " + dataset_id)
    require(first_step == 50000 and interval == 50000, "Unexpected step grid: " + dataset_id)
    values = []
    last_elapsed = None
    for index, row in enumerate(rows):
        location = "{} row {}".format(dataset_id, index + 2)
        step = integer(row["step"], location + " step")
        value = number(row["value"], location + " value")
        elapsed = number(row["elapsed_wall_time_s"], location + " elapsed_wall_time_s")
        require(step == first_step + index * interval, "Nonuniform or duplicate step: " + location)
        require(elapsed >= 0, "Negative elapsed time: " + location)
        if index == 0:
            require(elapsed == 0, "First elapsed time is not zero: " + dataset_id)
        else:
            require(elapsed > last_elapsed, "Elapsed time does not increase: " + location)
        values.append(value)
        last_elapsed = elapsed
    require(first_step + (count - 1) * interval == last_step, "Last-step mismatch: " + dataset_id)
    require(last_elapsed == number(record["elapsed_span_s"], dataset_id + " elapsed_span_s"), "Elapsed-span mismatch: " + dataset_id)
    require(min(values) == number(record["value_min"], dataset_id + " value_min"), "Value-minimum mismatch: " + dataset_id)
    require(max(values) == number(record["value_max"], dataset_id + " value_max"), "Value-maximum mismatch: " + dataset_id)
    return len(rows)


def verify_training(root, hashes, manifest_files):
    manifest = read_table(root / "metadata/training_manifest.csv", MANIFEST_COLUMNS)
    require(len(manifest) == EXPECTED_DATASETS, "Expected exactly 12 training series")
    dataset_ids = {row["dataset_id"] for row in manifest}
    require(len(dataset_ids) == EXPECTED_DATASETS, "Duplicate training identifier")
    paths = {safe_relative_path(row["file"]) for row in manifest}
    require(len(paths) == EXPECTED_DATASETS, "Duplicate training file path")
    require(paths == manifest_files, "Training manifests disagree on file membership")
    for field in ("source_sha256", "published_sha256"):
        require(len({row[field].lower() for row in manifest}) == EXPECTED_DATASETS, "Duplicate training hash in " + field)
    observations = sum(verify_dataset(root, row, hashes) for row in manifest)
    require(observations == EXPECTED_OBSERVATIONS, "Expected 3,190 training observations")
    aliases = read_table(root / "metadata/duplicate_aliases.csv", ALIAS_COLUMNS)
    require(len(aliases) == EXPECTED_ALIASES, "Expected exactly 3 training aliases")
    alias_ids = set()
    for row in aliases:
        alias = row["source_group_alias"]
        require(ID_PATTERN.fullmatch(alias) is not None, "Invalid duplicate alias")
        require(alias not in alias_ids and alias not in dataset_ids, "Duplicate or colliding alias: " + alias)
        require(row["canonical_dataset_id"] in dataset_ids, "Unknown canonical series for alias: " + alias)
        require(row["evidence"].strip(), "Missing duplicate-alias evidence: " + alias)
        alias_ids.add(alias)
    return len(manifest), observations, len(aliases)


def nonnegative_number(value, location):
    result = number(value, location)
    require(result >= 0, "Negative measurement: " + location)
    return result


def numeric_count(value, location):
    """Source counts may retain an XML numeric string such as 6.0."""
    result = nonnegative_number(value, location)
    require(result == result.to_integral_value(), "Noninteger count: " + location)
    return int(result)


def source_cell(value, location):
    require(re.fullmatch(r"Sheet1![A-Z]+[1-9][0-9]*", value) is not None,
            "Invalid workbook cell reference: " + location)


def require_schema(rows, columns, count, label):
    require(len(rows) == count, "Unexpected row count: " + label)
    require(all(list(row) == columns for row in rows), "Unexpected experimental columns: " + label)
    require(all(all(value != "" for value in row.values()) for row in rows),
            "Unexpected missing cell: " + label)


def condition_grid(rows, label):
    keys = []
    for row in rows:
        condition = row["condition"]
        require(condition in CONDITIONS, "Unknown study condition: " + label)
        keys.append((condition, integer(row["record_index"], label + " record_index")))
    expected = {(condition, index) for condition in CONDITIONS for index in range(1, 11)}
    require(len(set(keys)) == len(keys) and set(keys) == expected,
            "Study condition/index grid mismatch: " + label)


def verify_experimental_tables(tables):
    """Check the documented structures without asserting scientific provenance."""
    task_path = "data/human_study/task_performance.csv"
    accuracy_path = "data/human_study/human_placement_accuracy.csv"
    block1_path = "data/qr_detection/recognition_trials_block_1.csv"
    block2_path = "data/qr_detection/recognition_trials_block_2.csv"
    ranges_path = "data/qr_detection/detection_ranges.csv"
    expected = {task_path, accuracy_path, block1_path, block2_path, ranges_path}
    actual = {path for path in tables if not path.startswith("data/training/")}
    require(actual == expected, "Experimental table membership differs from this release")

    task = tables[task_path]
    require_schema(task, TASK_COLUMNS, 40, task_path)
    condition_grid(task, task_path)
    for row in task:
        location = row["condition"] + " task record " + row["record_index"]
        nonnegative_number(row["completion_time_min"], location)
        numeric_count(row["assistance_requests"], location)
        source_cell(row["completion_time_source_cell"], location)
        source_cell(row["assistance_source_cell"], location)

    accuracy = tables[accuracy_path]
    require_schema(accuracy, ACCURACY_COLUMNS, 40, accuracy_path)
    condition_grid(accuracy, accuracy_path)
    for row in accuracy:
        location = row["condition"] + " placement record " + row["record_index"]
        incorrect = numeric_count(row["incorrect_placements"], location)
        total = numeric_count(row["total_components"], location)
        correct = numeric_count(row["correct_placements"], location)
        proportion = nonnegative_number(row["accuracy_proportion"], location)
        require(total == 49 and incorrect <= total and correct == total - incorrect,
                "Placement count arithmetic mismatch: " + location)
        require(proportion <= 1 and abs(proportion - Decimal(correct) / Decimal(total)) <= Decimal("1e-12"),
                "Placement accuracy arithmetic mismatch: " + location)
        source_cell(row["incorrect_placements_source_cell"], location)
        source_cell(row["accuracy_formula_source_cell"], location)

    sizes = {Decimal("2.5") * i for i in range(1, 9)}
    for path, block, allowed_sizes, count in [
        (block1_path, "block_1", sizes, 80),
        (block2_path, "block_2", {Decimal("2.5") * i for i in range(5, 9)}, 40),
    ]:
        rows = tables[path]
        require_schema(rows, QR_TRIAL_COLUMNS, count, path)
        keys = []
        for row in rows:
            require(row["source_block"] == block, "QR source-block mismatch: " + path)
            size = nonnegative_number(row["qr_side_length_cm"], path)
            trial = integer(row["trial_index"], path)
            keys.append((size, trial))
            nonnegative_number(row["recognition_time_s"], path)
            nonnegative_number(row["detection_distance_m"], path)
            source_cell(row["time_source_cell"], path)
            source_cell(row["distance_source_cell"], path)
        expected_keys = {(size, index) for size in allowed_sizes for index in range(1, 11)}
        require(len(set(keys)) == count and set(keys) == expected_keys, "QR size/trial grid mismatch: " + path)

    ranges = tables[ranges_path]
    require_schema(ranges, QR_RANGE_COLUMNS, 16, ranges_path)
    keys = []
    for row in ranges:
        size = nonnegative_number(row["qr_side_length_cm"], ranges_path)
        environment = row["environment"]
        keys.append((size, environment))
        minimum = nonnegative_number(row["min_detectable_distance_m"], ranges_path)
        maximum = nonnegative_number(row["max_detectable_distance_m"], ranges_path)
        require(maximum >= minimum, "QR range maximum is below minimum")
        source_cell(row["min_distance_source_cell"], ranges_path)
        source_cell(row["max_distance_source_cell"], ranges_path)
    expected_keys = {(size, environment) for size in sizes for environment in {"indoor", "outdoor"}}
    require(len(set(keys)) == 16 and set(keys) == expected_keys, "QR size/environment grid mismatch")
    return sum(len(tables[path]) for path in expected)


def verify(root):
    root = Path(root).resolve()
    require(root.is_dir(), "Package directory does not exist")
    members = package_members(root)
    hashes = checksum_inventory(root, members)
    required = {"README.md", "metadata/file_manifest.csv", "metadata/training_manifest.csv", "metadata/duplicate_aliases.csv"}
    require(required.issubset(hashes), "Required package metadata is missing")
    manifest = read_table(root / "metadata/file_manifest.csv", FILE_MANIFEST_COLUMNS)
    dataset_ids = {row["dataset_id"] for row in manifest}
    require(len(dataset_ids) == len(manifest), "Duplicate dataset identifier")
    paths = {safe_relative_path(row["file"]) for row in manifest}
    require(len(paths) == len(manifest), "Duplicate manifest file path")
    data_members = {name for name in members if name.startswith("data/")}
    require(data_members == paths, "Data directory and manifest membership differ")
    tables = {}
    for record in manifest:
        dataset_id = record["dataset_id"]
        require(ID_PATTERN.fullmatch(dataset_id) is not None, "Invalid dataset identifier")
        category = record["category"]
        require(category in {"training", "human_study", "qr_detection"}, "Unknown data category: " + category)
        relative = record["file"]
        require(relative == "data/{}/{}.csv".format(category, dataset_id), "Dataset path/identifier mismatch: " + dataset_id)
        require(HASH_PATTERN.fullmatch(record["published_sha256"]) is not None, "Malformed file manifest hash: " + dataset_id)
        require(record["published_sha256"].lower() == hashes[relative], "File manifest hash mismatch: " + dataset_id)
        columns = record["columns"].split(";")
        require(len(set(columns)) == len(columns) and all(ID_PATTERN.fullmatch(c) for c in columns), "Invalid manifest columns: " + dataset_id)
        source_names = record["source_files"].split(";")
        require(all(name and "/" not in name and "\\" not in name and ":" not in name and name not in {".", ".."} for name in source_names),
                "Source files must be plain basenames: " + dataset_id)
        tables[relative] = read_table(root / relative, columns, allow_empty=columns)
        require(len(tables[relative]) == integer(record["rows"], dataset_id + " rows"), "File manifest row count mismatch: " + dataset_id)
    training_paths = {r["file"] for r in manifest if r["category"] == "training"}
    training_count, training_rows, aliases = verify_training(root, hashes, training_paths)
    extra_rows = verify_experimental_tables(tables)
    return len(hashes), len(manifest), training_count, training_rows, extra_rows, aliases


def main():
    try:
        counts = verify(Path(__file__).resolve().parents[1])
    except (VerificationError, OSError, UnicodeError, csv.Error, InvalidOperation, ValueError) as error:
        print("FAIL: {}".format(error), file=sys.stderr)
        return 1
    print("PASS: {} files hashed; {} data tables; {} training series with {:,} rows; {} other data rows; {} training aliases.".format(*counts))
    print("Integrity and schema checks passed. Scientific validity and source provenance are not verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
