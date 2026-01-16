> [!warning]
> This library is not updated anymore. This project is now over, please see other alternatives such as [EMACC99/mangadex](https://github.com/EMACC99/mangadex). You can also read the API docs [here](https://api.mangadex.org/docs/) and get yourself familiar with them.  
> The use of this library is discouraged. Packages from PyPI may be removed at any given time.  
> **As a reminder, I was never affiliated with MangaDex by any means.**

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
