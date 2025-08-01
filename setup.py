import io
from setuptools import setup, find_packages


with io.open('README.md') as readme_file:
    long_description = readme_file.read()


def test_suite():
    try:
        import unittest2 as unittest
    except:
        import unittest

    suite = unittest.TestLoader().discover("tests")
    return suite

# This setup.py is kept for backward compatibility
# The main configuration is now in pyproject.toml
setup(name='mapbox-vector-tile-mappy',
      version='1.0.10',
      description=u"Mapbox Vector Tile",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Harish Krishna",
      author_email='harish.krsn@gmail.com',
      packages=find_packages(),
      url='https://github.com/Mappy/mapbox-vector-tile',
      license='MIT',
      zip_safe=False,
      # test_suite="setup.test_suite",  # Moved to pyproject.toml
      install_requires=[
          "protobuf>=3.20.3",
          "shapely>=2.1.1",
          "pyclipper>=1.3.0.post6"
      ]
      )
