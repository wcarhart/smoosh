# smoosh 
### /smo͞oSH/ (verb) to squash, crush, or flatten

This is a short program that summarizes (smooshes) text files, either locally or from the web. For example, this simple script can take any New York Times, CNN, or Fox News article and _smoosh_ it down by ~70-80% on average. This means that most news articles can be read in just a few sentences!

The current implementation only works from the command line (although `utf-8` encodings are now supported 🎉), but the goal is to host it somewhere in the near future!

Currently runs successfully on **Python 3.6.5**. _`smoosh` will not work with Python 2.x_ (the last working commit with Python 2.x can be found [here](https://github.com/wcarhart/smoosh/tree/02b4b31a93fc0626170aa3773ef20c37f37b5aa6)).

## Installation

This uses [Python](https://www.python.org/), and few different libraries for web-scraping and parsing. To install all of the dependencies, use:
```
pip install -r requirements.txt
```
Then just clone and run!

## Usage

`python3 smoosh.py [-h] [-n NUM_SENTENCES] [-f] [-o] [-v] [-i] article`

Use `python3 smoosh.py -h` to pull up the help menu and get a summary of the command line arguments:
```
positional arguments:
  article               the URL of the target article (if -i is included, the name of the .txt file)

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_SENTENCES, --num-sentences NUM_SENTENCES
                        the number of sentences that will be used to describe the text (default is 7)
  -f, --file            if included, output will be written to 'output.txt'
  -o, --omit-metrics    if included, metric summary will be ommitted
  -v, --verbose         if included, metric summary will be verbose
  -i, --input           if included, input will be as a .txt file rather than a URL
```

## Examples

You can run `smoosh` on a webpage:
```
python3 smoosh.py https://www.npr.org/2018/06/10/618660184/trump-and-kim-arrive-in-singapore-for-unprecedented-summit
```
Or on a local text file (see the `articles` folder for a few test article `.txt` files):
```
python3 smoosh.py -i articles/article1.txt
```
Output shows the summary and some metrics, which you can omit with the `-o` flag or make verbose with the `-v` flag.
```
The expansion would enable SpaceX to store and refurbish large numbers of Falcon rocket boosters and nose cones at the operations center down the road from NASA's Vehicle Assembly Building.  "As SpaceX's launch cadence and manifest for missions from Florida continues to grow, we are seeking to expand our capabilities and streamline operations to launch, land and re-fly our Falcon family of rockets," said James Gleeson, a SpaceX spokesman. Here's what SpaceX has in mind to start:  The most eye-catching feature would be a 32,000-square-foot tower standing up to 300 feet tall, housing a "world-class, architecturally distinctive" launch and landing control center.  The site would replace or add to SpaceX's current launch and landing control center, which is tucked in a small office space outside the south gate to Cape Canaveral Air Force Station near Port Canaveral.  After landing on Cape Canaveral pads or SpaceX's "drone ship" at sea, recovered Falcon 9 and Falcon Heavy boosters would return to a 133,000-square-foot hangar standing up to 100 feet tall.  Rivaling the open-air exhibit of famous spacecraft at the nearby KSC Visitor Complex, SpaceX plans to display "historic space vehicles" in its own rocket garden, potentially including Falcon boosters or Dragon capsules staged vertically or horizontally. The SpaceX Operations Area would expand the company's KSC footprint beyond the hangar it built at the base of pad 39A, which can house three Falcon boosters.

-_-_-_-_-_-_ METRICS _-_-_-_-_-_-
Original length: 6035 characters
Smooshed length: 1480 characters

Original smooshed by 75.48%

Most common words:
  1. spacex (15 times)
  2. would (14 times)
  3. launch (12 times)
  4. space (10 times)
  5. falcon (10 times)
  6. area (7 times)
  7. nasa (7 times)

Most important sentences:
  1. Sentence #4
  2. Sentence #5
  3. Sentence #12
  4. Sentence #16
  5. Sentence #17
```

Pretty cool, right??


## Issues
If you think you've found a bug, please open an issue! Or, if you're feeling extra special, fork, fix the problem yourself, and open a new pull request (I'm usually pretty good about responding quickly!). Please make sure to check the current issues before opening a new one to ensure we don't have duplicates.

This has been tested on a few different news websites, and it is a known issue that the _New York Times_ does not play nice with `smoosh`. That is a work and progress, and I'd love any help to fix it!
