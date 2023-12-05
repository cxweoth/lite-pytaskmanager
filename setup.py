from setuptools import setup, find_packages

setup(
    name='lite-pytaskmanager',
    version='0.1.0',
    description='A lite task manager for manage tasks in python',
    author='Tsung-Hsuan Hung',
    author_email="cxweoth@gmail.com",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=["schedule"],
)
