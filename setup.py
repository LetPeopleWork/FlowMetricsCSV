from setuptools import setup, find_packages

setup(
    name='flowmetricscsv',
    version='0.10.5',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'FlowMetricsCSV': ['ExampleFile.csv', 'logo.png', 'ExampleConfig.json'],
    },
    install_requires=[
        "argparse", "pandas", "numpy", "matplotlib", "adjustText"
    ],
    entry_points={
        'console_scripts': [
            'flowmetricscsv=FlowMetricsCSV.main:main',
        ],
    },
    author='Benjamin Huser-Berta',
    author_email='benj.huser@gmail.com',
    description='A package to generate flow metrics charts from CSV files.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://letpeople.work',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
