# splitter

    Usage: splitter [OPTIONS] [SPLITS]...

      Split a given file into distinct parts of given percentages.

              splitter -d my_file train:80 test:20

      This creates two new files: my_file.train, containing 80% of the lines of
      my_file, and my_file.test, containing the rest. When the fractions can't
      exactly divide the file properly, the remaining samples are given to (one
      of) the smaller split(s).

    Options:
      -d, --dataset FILENAME          Input file to split into sets  [required]
      -s, --standard-splits           Split preset for train:80 test:10 dev:10
      -m, --mode [line|paragraph|L|P]
                                      Mode of sample boundary detection. line
                                      means the samples are seperated by
                                      linebreaks. paragraph means the samples are
                                      seperated by empty lines.
      -t, --trim-empty-lines          In paragraph mode, get rid of the empty
                                      lines seperating the samples
      --shuffle / --no-shuffle        Whether to shuffle the samples. On by
                                      default.
      --help                          Show this message and exit.
