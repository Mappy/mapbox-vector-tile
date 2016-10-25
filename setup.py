import io
from setuptools import setup, find_packages, Extension
from os.path import join


with io.open('README.md') as readme_file:
    long_description = readme_file.read()


def test_suite():
    try:
        import unittest2 as unittest
    except:
        import unittest

    suite = unittest.TestLoader().discover("tests")
    return suite


speedup_module = Extension(
                      "mapbox_vector_tile.speedups",
                      sources=[
                          join("mapbox_vector_tile", "speedups", "encode_py.cpp"),
                      ]
                  )

setup(name='mapbox-vector-tile',
      version='1.0.0',
      description=u"Mapbox Vector Tile",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Harish Krishna",
      author_email='harish.krsn@gmail.com',
      url='https://github.com/tilezen/mapbox-vector-tile',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite="setup.test_suite",
      install_requires=[
          "setuptools",
          "protobuf",
          "shapely",
          "future",
          "pyclipper"
      ],
      provides = ['speedups'],
      ext_modules=[speedup_module]
      )
