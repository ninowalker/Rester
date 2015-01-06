from setuptools import setup, find_packages

setup(name='Rester',
    version='1.0.1',
    author='Rajeev Chitamoor',
    author_email='rajeev@chitamoor.com',
    url='https://github.com/chitamoor/rester',
    license='LICENSE.txt',
    packages=find_packages(),
    package_data={'': ['README.md']},
    entry_points={
        'console_scripts': ['apirunner = rester.apirunner:run',
                            'resterunit = rester.unit:run']
    },
    test_suite="test",
    description='Rest API Testing',
    long_description=open('README.md').read(),
    install_requires=["requests", "PyYAML>=3.9", "docopt", "testfixtures"],
)
