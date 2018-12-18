from setuptools import setup, find_packages

version = '0.0'

classifiers = """
Development Status :: 3 - Alpha
License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)
Operating System :: OS Independent
Programming Language :: JavaScript
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
""".strip().splitlines()

long_description = (
    open('README.rst').read()
    + '\n' +
    open('CHANGES.rst').read()
    + '\n')

setup(
    name='repodono.cellml',
    version=version,
    description="CellML integration for the repodono framework",
    long_description=long_description,
    classifiers=classifiers,
    keywords='',
    author='Tommy Yu',
    author_email='',
    url='https://github.com/repodono/repodono.cellml',
    license='gpl',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['repodono'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'cgrspy>=1.3.0',
        'requests',

        # development dependencies.
        'repodono.task'
        ' @ git+https://github.com/repodono/repodono.task.git@master',
    ],
    extras_require={
    },
    python_requires='>=3.4',
    entry_points={
    },
    test_suite="repodono.cellml.tests.make_suite",
)
