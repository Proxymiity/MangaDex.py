[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ca6509334c4e425f8d9d61083715cacb)](https://www.codacy.com/gh/Proxymiity/MangaDex.py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Proxymiity/MangaDex.py&amp;utm_campaign=Badge_Grade)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Proxymiity_MangaDex.py&metric=alert_status)](https://sonarcloud.io/dashboard?id=Proxymiity_MangaDex.py)
[![MangaDex API Status](https://img.shields.io/website-up-down-green-red/https/api.mangadex.org?label=mangadex%20api%20status)](https://api.mangadex.org/)
[![MangaDex Website Status](https://img.shields.io/website-up-down-green-red/https/mangadex.org?label=mangadex%20website%20status)](https://mangadex.org/)

# MangaDex.py

An easy to use, MangaDex API Wrapper using Requests - aiming to be simple and efficient. 

# Installation
````
pip install --upgrade MangaDex.py 
````

# Quick start
### Example
Logging in and getting the latest chapter from a manga:
````python
# Import the MangaDexPy library
import MangaDexPy
cli = MangaDexPy.MangaDex()
cli.login("username", "password")

# Get manga with id b9797c5b-642e-44d9-ac40-8b31b9ae110a.
manga = cli.get_manga("b9797c5b-642e-44d9-ac40-8b31b9ae110a")

print(manga.title + "'s latest volume:")
print(manga.last_volume)
print(manga.title + "'s latest chapter:")
print(manga.last_chapter)
````
Here's the terminal output:  
![Quick start demo image](https://api.ayaya.red/github/Proxymiity/MangaDex.py/quick_start_demo.png)  
*You can find more examples on [this page](https://github.com/Proxymiity/MangaDex.py/wiki/Examples)*

### Explanation
``cli = MangaDexPy.MangaDex()`` returns the client object used to make calls.  
``cli.login(u ,p)`` logs in to MangaDex using credentials stored in variables.  
``manga = cli.get_manga("b9797c5b-642e-44d9-ac40-8b31b9ae110a", full=True)`` returns a `Manga` object, which contains the `last_volume` and `last_chapter` properties.

# Documentation
The full API documentation is available [in this repository's wiki](https://github.com/Proxymiity/MangaDex.py/wiki).
