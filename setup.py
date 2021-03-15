from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='MangaDex.py',
      packages=[
          "MangaDexPy"
      ],
      version='1.0.1',
      description='An API wrapper for MangaDex.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Proxymiity/MangaDex.py',
      download_url='https://github.com/Proxymiity/MangaDex.py/releases',
      author='Proxymiity',
      author_email='commits@proxymiity.fr',
      license='MIT',
      install_requires=[
          'requests>=2.25.0',
      ],
      zip_safe=False
      )
