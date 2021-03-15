[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ca6509334c4e425f8d9d61083715cacb)](https://www.codacy.com/gh/Proxymiity/MangaDex.py/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Proxymiity/MangaDex.py&amp;utm_campaign=Badge_Grade)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Proxymiity_MangaDex.py&metric=alert_status)](https://sonarcloud.io/dashboard?id=Proxymiity_MangaDex.py)

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

# Get manga with id 24724. Setting full to True allows retrieving the list of chapters associated to this Manga
manga = cli.get_manga(24724, full=True)

print(manga.title + "'s latest volume:")
print(manga.chapters[0].volume)
print(manga.title + "'s latest chapter:")
print(manga.chapters[0].chapter)
````
Here's the terminal output:  
![Quick start demo image](https://api.proxymiity.fr/github/Proxymiity/MangaDex.py/quick_start_demo.png)

### Explanation
``cli = MangaDexPy.MangaDex()`` returns the client object used to make calls.  
``cli.login(u ,p)`` logs in to MangaDex using credentials stored in variables.  
``manga = cli.get_manga(24724, full=True)`` returns a `Manga` object.  
This Manga object has a ``.chapters`` property, which returns a List of `PartialChapter`. A partial Chapter is a chapter with no information about its pages nor the server it is server from, unlike `Chapter`.  
We could retrieve the entire ``Chapter`` using `cli.get_chapter(manga.chapters[0].id)`, but this isn't needed as we're just requesting `volume` and `chapter` properties of this chapter, which is included in the `PartialChapter`.

# Documentation

The full API documentation is available [in this repository's wiki](https://github.com/Proxymiity/MangaDex.py/wiki).