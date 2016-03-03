format\_collection\_sheets
==========================

Performs basic recoding of collection sheets to yield a standardized spreadsheet format.

Usage
-----

``` shell
Usage: format_collections [OPTIONS]

  Reformat and combine collection spreadsheets into a single standardized
  file.

Options:
  -s, --summary-sheet PATH   Paths to an excel sheets of field disecction
                             records. NOTE: may be used multiple times to
                             supply more than one input sheet.  [required]
  -o, --output PATH          Path to where you want the combined/standardized
                             output xls file.  [required]
  -v, --village-id-map PATH  Path to a comma separated file containing the
                             long village name to short village codes.
                             [required]
  --help                     Show this message and exit.
```

Installation
------------

For now just

1. download and expand the latest release from the [releases](https://github.com/CacconeLabYale/format-collection-sheets/releases) section of this site
2. open a terminal and enter the unzipped release folder
3. execute the following commands:

``` shell
pip install .
```

OR:

If you have conda there is no nee dto download anything before hand.  Simply execute the following:

```
conda install -c https://conda.anaconda.org/gusdunn format-collection-sheets
```



### Requirements

Compatibility
-------------
Only tested for Python 2.7.x

Licence
-------
MIT

Authors
-------

format\_collection\_sheets was written by [Gus Dunn].

  [Gus Dunn]: wadunn83@gmail.com
