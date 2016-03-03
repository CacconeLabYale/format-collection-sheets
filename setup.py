"""Set up the package for installation."""

import setuptools

setuptools.setup(
    name="format_collection_sheets",
    version="0.0.1",
    url="https://github.com/CacconeLabYale/format-collection-sheets",

    author="Gus Dunn",
    author_email="wadunn83@gmail.com",

    description="Performs basic recoding of collection sheets to yield a standardized spreadsheet format.",
    long_description=open('README.md').read(),

    packages=setuptools.find_packages(),

    install_requires=["pandas",
                      "numpy",
                      "munch",
                      "xlrd",
                      "xlwt"
                     ],
     entry_points='''
             [console_scripts]
             format_collections=format_collection_sheets.main:cli
             ''',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
