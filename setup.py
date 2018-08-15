
from setuptools import setup

setup(name='pandoc_avm',
      version='0.1',
      description='a pandoc filter for drawing construction grammar like box matrices (AVMs)',
      url='http://github.com/hrmJ/pandoc_avm',
      author='Juho Härme',
      author_email='juho.harme@gmail.com',
      license='MIT',
      packages=['pandoc_avm'],
      install_requires=[
          'pylatex',
          'pyparsing',
          'panflute',
          'dominate',
      ],
      entry_points={
          'console_scripts': [
              'pandoc_avm = pandoc_avm.pandoc_avm:main'
              ]
          },
      zip_safe=False)
