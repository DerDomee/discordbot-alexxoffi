"""
Create translation files from source.json.

This script reads and converts the contents in
resources/translations/source.json
and creates multiple files, one for every language, containing only the
key-translation pairs for this language.
"""
import sys
import json
import traceback


def _get_sourcedict():
    """Read source.json and return the dictionary formed from it."""
    print("Reading source.json ...")
    with open("resources/translations/source.json", 'r') as file:
        try:
            data = json.load(file)
            return data
        except json.JSONDecodeError as err:
            sys.stderr.write("\u001b[31m" + traceback.format_exc()
                             + "\u001b[0m\n")
            sys.stderr.write("\u001b[31mFailed to read source.json: "
                             + "Invalid JSON.\u001b[0m\n")
            sys.exit(1)
    sys.exit(1)


def _create_destination_dicts(source_dict):
    """Create a dict with key-value dicts for every language found."""
    destination_dict = {}
    errors = []
    warnings = []
    for key, values in source_dict.items():
        if 'en' not in values:
            errors.append(
                f"Key '{key}' does not contain mandatory english translation")
        for language, translation in values.items():
            if language not in destination_dict:
                destination_dict[language] = {}
            destination_dict[language][key] = translation
    return (destination_dict, warnings, errors)


def _print_failures(warnings, errors):
    if warnings:
        for warning in warnings:
            sys.stderr.write("\u001b[33m" + warning + "\u001b[0m\n")
    if errors:
        for error in errors:
            sys.stderr.write("\u001b[31m" + error + "\u001b[0m\n")
        sys.stderr.write("\n\u001b[31mTranslation failed, errors occured!"
                         + "\u001b[0m\n")
        sys.exit(1)


def _calculate_coverage(source_dict, destination_dicts):
    total_key_count = len(source_dict)
    language_key_counts = {}
    for language, keys in destination_dicts.items():
        total = len(destination_dicts[language])
        coverage = total / total_key_count
        language_key_counts[language] = {"total": total, "coverage": coverage}
        destination_dicts[language]['language.meta.coverage'] = coverage
    return (total_key_count, language_key_counts)


def _save_translations(destination_dicts):
    for language, translations in destination_dicts.items():
        with open(f"resources/translations/{language}.json", 'w') as file:
            json.dump(
                destination_dicts[language],
                file,
                indent=2,
                sort_keys=True)


def _get_format_sugar(coverage):
    ansicolor = "\u001b[31m"        # Dark Red
    emoji = "❌"
    if coverage['coverage'] > 0.5:
        ansicolor = "\u001b[31;1m"  # Bright Red
        emoji = "🙁"
    if coverage['coverage'] > 0.7:
        ansicolor = "\u001b[33m"    # Dark Yellow (Orange)
        emoji = "😐"
    if coverage['coverage'] > 0.9:
        ansicolor = "\u001b[33;1m"  # Bright Yellow (Yellow)
        emoji = "🙂"
    if coverage['coverage'] > 0.95:
        ansicolor = "\u001b[32m"    # Dark Green
        emoji = "😀"
    if coverage['coverage'] == 1:
        ansicolor = "\u001b[32;1m"  # Bright Green
        emoji = "😁"
    return (ansicolor, emoji)


def _print_coverages(total_key_count, coverages, destination_dicts):
    print(f"Total number of keys: {total_key_count}")
    coverages = {k: v for k, v in sorted(
        coverages.items(),
        key=lambda item: item[1]['coverage'],
        reverse=True)}
    for language, coverage in coverages.items():
        ansicolor, emoji = _get_format_sugar(coverage)
        formatted_coverage = format(coverage['coverage'] * 100, '.01f')
        print(
            emoji + ansicolor + " " + language + " ("
            + destination_dicts[language]['language.meta.name.unlocalized']
            + ", "
            + destination_dicts[language]['language.meta.name.localized']
            + ") " + str(coverage['total']) + "/" + str(total_key_count) + ": "
            + formatted_coverage + "%" + "\u001b[0m")


def main():
    """."""
    print("Generating translations from "
          + "resources/translations/source.json ...")

    source_dict = _get_sourcedict()
    destination_dicts, warnings, errors = _create_destination_dicts(
        source_dict)
    _print_failures(warnings, errors)
    total_key_count, coverage = _calculate_coverage(
        source_dict, destination_dicts)
    _save_translations(destination_dicts)
    _print_coverages(total_key_count, coverage, destination_dicts)
    print("\n\u001b[32mTranslation successful!\u001b[0m")
    sys.exit(0)

if __name__ == "__main__":
    main()
