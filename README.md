<h3 align="center">CS 660 - Introduction to Database Systems<br>PA3: MongoDB and Twitter Analysis</h3>

<p align="right">Zuoqi Zhang</p>
<p align="right">U98670811</p>

---

#### 1. Basic Part

* File list
	* `zqzhang_pa3.txt` - Contains all the queries in MongoDB for the six questions.
	* `zqzhang_pa3.pdf` - Contains all the queries and the results from terminal.

#### 2. Extra Part

* File list
	* `pymongo_tweepy_keywords` - Mines tweets based on keywords.
	* `pymongo_tweepy_location` - Mines tweets based on location.
	* `pa3_extra_part1.py` - Answers the three questions in Part 1.
	* `pa3_extra_part2.py` - Answers the questions in Part 2 (only B and C).
	* `json_to_csv.py` - Save tweets in a csv file named `usa_tweets.csv`.
	* `draw_maps.py`- Draws two maps using Folium for the last two tasks of Part 2.
	* `map.html` - Map of tweets, the html code is automatically created by `draw_maps.py`.
	* `emoji_of_state.html` - Map of emojis, the html code is automatically created by `draw_maps.py`.
* Notes
	* The code is written in Python 3.6.
	* Please create a `keys.txt` file which contains the keys and access tokens before you run the first two code files.
	* For the map `emoji_of_state`, I draw a red icon for each state, if you click on it, you will see the top 2 emojis in this state.
	* Since `draw_maps.py` needs to read all tweets from database, and calculate the occurrence of each emoji in each state, the code may take a while to finish, please wait until you see '**Two maps have been created.**' in the output.