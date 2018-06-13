from setuptools import setup

setup(name='vroom',
      license='MIT',
      version='1.0.0',
      description='License Plate Parser',
      author='Magdalena Nowak',
      author_email='magdanowak0804@gmail.com',
      url='https://github.com/magdanowak/vroom',
      install_requires=['pyyaml'],
      packages=['vroom'],
      package_data={'vroom': ['*.yml']},
      include_package_data=True
     )