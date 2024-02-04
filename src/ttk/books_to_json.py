import argparse

from ttk.file_parser import create_output_directory, read_file_list, process_files
from ttk.utils import setup_logging


def main():
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Convert a book into a JSON representation and chunk the text for metadata augmentation.")
    parser.add_argument("--input_list",
                        help="Name of the input text file that contains a list of all text files that should be split.")
    parser.add_argument("--input_dir",
                        help="Directory containing the text documents. Defaults to current directory.")
    parser.add_argument("--output_dir",
                        help="Directory where the new json documents will be written.")
    parser.add_argument("--chapter_prefix", default="=",
                        help="The prefix that defines the chapter title.")
    parser.add_argument("--section_prefix", default="==",
                        help="The prefix that defines the section title.")
    parser.add_argument("--sub_section_prefix", default="===",
                        help="The prefix that defines the sub-section title.")

    args = parser.parse_args()

    create_output_directory(args.output_dir)
    files = read_file_list(args.input_list)
    process_files(files, args.input_dir, args.output_dir)


if __name__ == "__main__":
    main()
