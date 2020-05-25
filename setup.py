from setuptools import setup
from pathlib import Path


# read the contents of README file
DIR = Path(__file__).parent
with open(DIR.joinpath('README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    use_scm_version=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
