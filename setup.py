import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'pyaudio',
    'numpy',
    'matplotlib'
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(name='otoware',
      version='0.0.1',
      description='otoware',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
      ],
      author='maskuerade',
      author_email='k.kiyama117@gmail.com',
      url='https://ku-jinja.net',
      keywords='python',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points={
          'console_scripts': [
              'otowari = src.main:main',
          ],
      },
      )
