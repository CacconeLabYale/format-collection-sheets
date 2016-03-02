import setuptools

setuptools.setup(
    name="format_collection_sheets",
    version="0.0.1",
    url="package_url",

    author="Gus Dunn",
    author_email="wadunn83@gmail.com",

    description="Performs basic recoding of collection sheets to yield a standardized spreadsheet format.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],

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
