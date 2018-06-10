# smoosh 
### /smooSH/ (verb) to squash, crush, or flatten

This is a short program to summarize text files. For example, this simple script can take any New York Times, CNN, or Fox News article and _smoosh_ it down by ~70-80% on average. This means that most news articles can be read in just a few sentences!

The current implementation only works from the command line with `.txt` files (although `utf-8` is supported), but the goal in the future is to allow the script to be fed in an html, and scrape the content of the article to be summarized.

Currently runs successfully on Python 2.7.10

## Installation

This uses [Python](https://www.python.org/), and is almost vanilla except for one small dependency called [Unidecode](https://pypi.org/project/Unidecode/). To install it, just run:
```
pip install unidecode
```
Then just clone and run!

## Usage

`python smoosh.py [-h] [-n NUMBER_OF_SENTENCES] [-f] [-o] [-v] filename`

Use `python smoosh.py -h` to pull up the help menu and get a summary of the command line arguments:
```
positional arguments:
  filename              the name of the file to be summarized (as a .txt file)

optional arguments:
  -h, --help            show this help message and exit
  -n NUMBER_OF_SENTENCES, --number-of-sentences NUMBER_OF_SENTENCES
                        the number of sentences that will be used to describe the text (default is 7)
  -f, --file            if included, output will be written to 'output.txt'
  -o, --omit-metrics    if included, metric summary will be ommitted
  -v, --verbose         if included, metric summary will be verbose
```

## Examples

I've included a few test files in the `articles/` directory to showcase how the script works. For example, running: `python smoosh.py -v articles/article1.txt` will produce:

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
