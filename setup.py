import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'numpy',
    'matplotlib',
    'pyaudio'
]

tests_require = [
    'pytest',
    'pytest-cov',
]

setup(name='otoware',
      version='1.0.0',
      description='otoware',
      long_description=README,
      classifiers=[
          "Programming Language :: Python",
      ],
      author='kkiyama117',
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
              'otowari = otoware.api:main',
          ],
      },
      )
