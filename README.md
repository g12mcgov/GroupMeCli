GroupMeCli
=======
![Preview](http://i1158.photobucket.com/albums/p618/g12mcgov/Screenshot2014-08-14235846.png)

A command line client for GroupMe. 

Description
==========
This is a brief command client for GroupMe that allows (largely) the same features as the GroupMe app, except for preferences, etc... 

I wrote this client because while at college, a lot of my friends and I stay in contact via GroupMe, and, being a computer science student, a lot of my time is spent in front of a shell. Now I can run this client on another console tab and stay in the loop.

I looked around for existing clients and found 2. One written in Haskell and the other in Javascript, neither of which I wanted. 

So here's my go at it. It's not the prettiest, but it gets the job done. Took about a day and half worth of work, so not as much time as I'd like was spent on it.

I didn't look too deep in GroupMe's API, so I glanced over the fact that they have a Push service powered by Faye that uses web-sockets for live communication, so perhaps I'll change this client to include that. If you didn't notice already, this is entirely based on their RESTFUL API.


Requirements
==========
Python 2.7

Modules:
  - PrettyTable
  - Termcolor
  - Json
  - Requests
  - csv

Installation
==========
1. Clone this repository
2. Get a GroupMe Developer key here at https://dev.groupme.com/ (insert this in <b>keys.csv</b>)
3. Setup: <code>sudo python setup.py install </code> to install requirements.
4. Run: <code>python Main.py</code>


==========
