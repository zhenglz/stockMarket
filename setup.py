from setuptools import setup

"""
Description of how to make a python package

https://python-packaging.readthedocs.io/en/latest/command-line-scripts.html

"""

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='stockMarket',
      version='1.0',
      long_description=readme(),
      description='SHA stock market analysis tools and tutorials',
      url='https://github.com/zhenglz/stockMarket',
      author='zhenglz',
      author_email='zhenglz@outlook.com',
      license='GPL-3.0',
      packages=['stockMarket', ],
      install_requires=[
          'numpy',
          'pandas',
          'sklearn',
          'matplotlib',
          'tushare',
          'bs4',
          'scipy',
      ],
      include_package_data=True,
      zip_safe=False,
      )
