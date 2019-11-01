from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ehelply-generator',
    packages=find_packages(),  # this must be the same as the name above
    version='0.1.1',
    description='eHelply Generator',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/ehelply/Generator',
    keywords=[],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'pytest',
        'sqlalchemy',
        'pydantic',
        'python-slugify',
        'ehelply_bootstrapper',
        'click'
    ],
    entry_points={
        'console_scripts': [
            'ehelplygen=ehelply_generator.ehelply_gen:ehelplygen',  # command=package.module:function
        ],
    },

)
