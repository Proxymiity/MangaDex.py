# MangaDex.py

A kind of fork based on [Sybil666's pytmangadex](https://github.com/Sibyl666/pytmangadex) to get data from the MangaDex API, aiming to get every data that the API can offer, without having to manage requests.

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

# Get manga with id 24724. Setting full to True allows retrieving chapters associated to this Manga
manga = cli.get_manga(24724, full=True)

print("Latest manga's chapter volume:")
print(manga.chapters[0].volume)
print("Latest manga's chapter")
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