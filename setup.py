from setuptools import setup, find_packages
import os

version = '0.0.1'
here = os.path.abspath(os.path.dirname(__file__))
long_description = open(os.path.join(here, 'README.rst')).read()

setup(name='videoShot',
      version=version,
      description='Tool to segmentation video',
      long_description=long_description,
      classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Utilities'
      ],
      keywords='video segmentation',
      author='Dyogo Ribeiro Veiga, Fabio Duncan de Souza, Whanderley Souza Freitas',
      author_email='dyogo.nsi@gmail.com, fduncan.iff@gmail.com, whanderley.souza@gmail.com',
      url='http://github.com/Dyogo/videoShot',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      # install_requires=[
      #     ''
      # ],
      entry_points="""
      [console_scripts]
      videoShot = videoShot:vs
      """,
      )