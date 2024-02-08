import argparse

from ttk.file_parser import create_output_directory, read_file_list, process_files
from ttk.utils import setup_logging


def main():
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Remove all llm request data from the JSON files in the directory.")
    parser.add_argument("--input_dir", help="The directory with JSON books.")

    args = parser.parse_args()

    create_output_directory(args.output_dir)
    files = read_file_list(args.input_list)
    process_files(files, args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
