from setuptools import setup, find_packages

with open('README.md', 'r') as reader:
    readme = reader.read()

with open('LICENSE', 'r') as reader:
    license = reader.read()

setup(
    name='pyllery',
    version='1.0.0',
    description='A gallery app created in python for learning purposes.',
    long_description=readme,
    author='ryuvi',
    author_email='vicenters10@gmail.com',
    url='https://github.com/ryuvi/pyllery',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=["setuptools>=61.0", "altgraph>=0.17.2", "Pillow>=9.2.0", "Tcl>=0.2", "tk>=0.1.0"]
)