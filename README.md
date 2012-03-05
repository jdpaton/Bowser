Bowser
------

(WIP, potentially insecure) Simple HTTP based file browser, with file previewing and syntax highlighting
support.

![image](http://i.imgur.com/c51gL.png)


**Install**

Requires Python 2.5> (no 3.x yet)

* install pygments `pip install -r requirements.txt` (optional)
* set the root directory to serve in `bowser.py`
* run `./bowser.py`
  * or `./bowser -p <PORT> -d <base dir>`
  * see `./bowser -h` for more options
* visit `http://localhost:8080`


**TODO**

* Add a table sorting plugin to the browser
* Move static HTML to bottle .tpl files
* Audit security
* Add download option to preview link


