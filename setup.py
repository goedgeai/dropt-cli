from setuptools import setup


# read the contents of README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(
    use_scm_version=True,
    long_description=long_description,
    long_description_content_type='text/markdown'
)
