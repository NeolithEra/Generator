import click
from pathlib import Path
import json
import subprocess
import sys
from ehelply_generator.generator import Generator

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def ehelplygen():
    pass


@ehelplygen.command()
@click.argument('input', required=True)
@click.argument('output', required=True)
def generate(input=None, output=None):
    structure_path: Path = Path(input)
    output_path: Path = Path(output)

    generator = Generator(structure_path=structure_path, output_path=output_path)
    generator.run()


if __name__ == '__main__':
    ehelplygen()

