from pathlib import Path

from lark import Lark

from ptf.files.fit import FitFileLoader
from ptf.grammar.transformer import PtfTransformer


def load_ptf(filename):
    # Create parser objects
    parser = Lark.open_from_package("ptf.grammar", "ptf.lark")
    transformer = PtfTransformer()

    # Load and parse ptf file data
    filepath = Path(filename).resolve()
    with filepath.open("r") as ptf_file:
        parsed_statements = transformer.transform(parser.parse(ptf_file.read()))

    # Find and process related files
    # TODO allow specifying files folder
    files_dir = Path(filename).resolve().parent / "files"
    for statement in parsed_statements:
        for related_file_path in statement.related_file_paths(files_dir):
            # TODO better file loader handling
            data, segments = FitFileLoader().load(related_file_path)
            for k, v in data.items():
                if k not in statement.data.keys():
                    statement.data[k] = v
            # TODO segments

    return parsed_statements
