# splitter

splitter is a tiny tool to split a single-file dataset into several distinct parts, typically train, test, and dev.

## Dependencies

splitter requires Python 3, and the `click` library.

## Tutorial

    splitter -d dataset train:80 test:10 dev:10

This creates three new files: `dataset.train,` containing roughly 80% of the
lines from dataset, and `dataset.test`/`dataset.dev`, each containing about 10%
of the lines. Because this setting is so common, there's a shortcut:

    splitter -d dataset --standard-splits

You can make this even shorter by using the shorthand `-s`, so one could also
just write

    splitter -sd dataset

All the three above examples are equivalent.

### Splits

The names "test", "dev", and "train" are not special in any way (apart from
being used by `--standard-splits`); you can use any names. You are also not
limited to having three parts, you can specify two, or seven, or even one part
(although that doesn't make much sense).

The numbers have to sum up to 100. Because most datasets can't exactly be split
as per the split specification, we give extra examples to (one of) the smallest
dataset(s).


### Modes and Options


If your files aren't seperated by newlines but by _double newlines_ (i.e. empty
lines), you can switch the `--mode` to `paragraph` (the default being `line`):

    splitter -sd dataset --mode paragraph

Instead of `paragraph`, you can use `P`, instead of `line` `L`.

By default, examples are shuffled before being divided into parts. To disable
that, use the switch `--no-shuffle`:

    splitter -sd dataset --no-shuffle

Finally, when in paragraph mode, there's an option to `--trim-empty-lines`,
which will cause the output to remove the empty lines seperating examples.
