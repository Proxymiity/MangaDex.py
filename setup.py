from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(name='MangaDex.py',
      packages=[
          "MangaDexPy"
      ],
      version='2.0.8',
      description='An API wrapper for the MangaDexAPIv5.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Proxymiity/MangaDex.py',
      download_url='https://github.com/Proxymiity/MangaDex.py/releases',
      changelog='https://github.com/Proxymiity/MangaDex.py/releases',
      documentation='https://github.com/Proxymiity/MangaDex.py/wiki',
      source='https://github.com/Proxymiity/MangaDex.py/tree/main/MangaDexPy',
      author='Proxymiity',
      author_email='dev@ayaya.red',
      license='MIT',
      install_requires=[
            'requests>=2.25.0',
      ],
      classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Topic :: Internet',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Utilities',
            'Intended Audience :: Developers'
      ],
      zip_safe=False,
      python_requires='>=3.6'
      )
