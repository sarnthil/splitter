#!/usr/bin/env python3
import re
import random
from operator import itemgetter
from math import floor
import click


def parse_splits(ctx, param, values):
    splits = {}
    if values and ctx.obj:
        raise click.BadParameter("Can't both specify a preset and splits")
    for value in values:
        try:
            name, size = value.split(":")
        except ValueError:
            raise click.BadParameter(
                "Splits have to be given in the format name:percentage ..."
            ) from None
        try:
            size = int(size)
        except ValueError:
            raise click.BadParameter(
                "Split values need to be integers"
            ) from None
        if not re.match(r"^[\w-]+$", name):
            raise click.BadParameter("Split names have to be reasonable")

        splits[name] = size
        ctx.obj = True
    if splits and sum(splits.values()) != 100:
        raise click.BadParameter("Splits need to sum up to 100")
    return splits


def parse_mode(ctx, param, value):
    if value == "L":
        return "line"
    elif value == "P":
        return "paragraph"
    return value


def parse_preset(ctx, param, value):
    if value and ctx.obj:
        raise click.BadParameter("Can't both specify a preset and splits")
    if value:
        ctx.obj = True
    if value and param.name == "standard_splits":
        return {"train": 80, "test": 10, "dev": 10}


seperators = {"line": "\n", "paragraph": "\n\n"}


@click.command(
    help="Split a given file into distinct parts of given percentages. \n\n"
    "\tsplitter -d my_file train:80 test:20\n\nThis creates two new "
    "files: my_file.train, containing 80% of the lines of my_file, and "
    "my_file.test, containing the rest. When the fractions can't exactly "
    "divide the file properly, the remaining samples are given to (one of) "
    "the smaller split(s)."
)
@click.option(
    "--dataset",
    "-d",
    type=click.File(),
    help="Input file to split into sets",
    required=True,
)
@click.option(
    "--standard-splits",
    "-s",
    is_flag=True,
    callback=parse_preset,
    help="Split preset for train:80 test:10 dev:10",
)
@click.option(
    "--mode",
    "-m",
    type=click.Choice(["line", "paragraph", "L", "P"]),
    default="line",
    help="Mode of sample boundary detection. "
    "line means the samples are seperated by linebreaks. "
    "paragraph means the samples are seperated by empty lines.",
    callback=parse_mode,
)
@click.option(
    "--trim-empty-lines",
    "-t",
    is_flag=True,
    help="In paragraph mode, get rid of the empty lines seperating the samples",
)
@click.option(
    "--shuffle/--no-shuffle",
    default=True,
    help="Whether to shuffle the samples. On by default.",
)
@click.argument("splits", nargs=-1, callback=parse_splits)
def cli(dataset, standard_splits, mode, trim_empty_lines, shuffle, splits):
    if standard_splits:
        splits = standard_splits
    splits = {k: v / 100 for k, v in splits.items()}
    samples = [
        sample for sample in dataset.read().split(seperators[mode]) if sample
    ]
    if trim_empty_lines:
        seperators["paragraph"] = "\n"
    total_size = len(samples)
    if shuffle:
        random.shuffle(samples)
    samples_iter = iter(samples)
    basename = f"{dataset.name}." if dataset.name != "-" else ""
    for index, (name, fraction) in enumerate(
        sorted(splits.items(), key=itemgetter(1), reverse=True)
    ):
        n_samples = floor(fraction * total_size)
        with open(f"{basename}{name}", "w") as f:
            for _ in range(n_samples):
                f.write(next(samples_iter))
                f.write(seperators[mode])
            if index == len(splits) - 1:
                for sample in samples_iter:
                    f.write(sample)
                    f.write(seperators[mode])
            if seperators[mode] == "\n\n":
                # If we are in paragraph mode, we will have _TWO_ newline
                # characters at the end of the file, which we don't want.
                # We want exactly one. We therefore seek backwards one
                # character and truncate the file.
                f.seek(f.tell() - 1)
                f.truncate()


if __name__ == "__main__":
    cli()
