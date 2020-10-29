# smoosh 
### /smo͞oSH/ (verb) to squash, crush, or flatten

This is a short program that summarizes (smooshes) text files, either locally or from the web. For example, this simple script can take any New York Times, CNN, or Fox News article and _smoosh_ it down by ~70-80% on average. This means that most news articles can be read in just a few sentences!

## Installation

Install with [Homebrew](https://brew.sh):
```bash
brew install wcarhart/tools/smoosh
smoosh --help
```

Or, install manually:
```bash
# clone repo
git clone https://github.com/wcarhart/smoosh.git
cd smoosh

# set up virtual environment
# if you don't have virtualenv, you can install it with `python3 -m pip install virtualenv`
python3 -m virtualenv -p `which python3` venv
source venv/bin/activate
python --version # should be 3.x

# install dependencies
python -m pip install -r requirements.txt

# verify installation
python smoosh.py --help
```

## Usage

Use `smoosh --help` to view the help menu.

```
usage: smoosh [-h] [-n SENTENCE_LIMIT] [-o] [-v] [-t TIMEOUT] source

Summarize any text article

positional arguments:
  source                the text source, which can either be the path to a local file or a URL to a webpage

optional arguments:
  -h, --help            show this help message and exit
  -n SENTENCE_LIMIT, --sentence-limit SENTENCE_LIMIT
                        the number of sentences that will be used to describe the text
  -o, --omit-metrics    omit metric summary
  -v, --verbose         print verbose metric summary
  -t TIMEOUT, --timeout TIMEOUT
                        timeout (in seconds) to use when fetching data from a URL
```

## Examples

You can run smoosh on a webpage:
```
smoosh 'https://www.cnn.com/2020/10/27/investing/amd-xilinx-purchase/index.html'
```
Or on a local file (see the `articles/` folder for a few test files):
```
smoosh articles/spacex.txt
```
Output shows the summary and some metrics, which you can omit with the `--omit-metrics` flag or make verbose with the `--verbose` flag.
```
It will be an operational monument to Elon Musk's vision: a towering SpaceX launch control center,
a hangar and a rocket garden rising in the heart of Kennedy Space Center. According to plans
detailed in a draft environmental review published recently by KSC, SpaceX will undertake a major
expansion of its facilities at the space center sometime in the future. The site would replace or
add to SpaceX's current launch and landing control center, which is tucked in a small office space
outside the south gate to Cape Canaveral Air Force Station near Port Canaveral. The tower would
include a data center; firing room; engineering room; control center for Falcon 9, Falcon Heavy and
Dragon vehicles; customer control center; and meeting spaces. "As SpaceX's launch cadence and
manifest for missions from Florida continues to grow, we are seeking to expand our capabilities and
streamline operations to launch, land and re-fly our Falcon family of rockets," said James Gleeson,
a SpaceX spokesman. Rivaling the open-air exhibit of famous spacecraft at the nearby KSC Visitor
Complex, SpaceX plans to display "historic space vehicles" in its own rocket garden, potentially
including Falcon boosters or Dragon capsules staged vertically or horizontally. SpaceX opted not to
build near the other companies in Exploration Park or to repurpose or share legacy NASA facilities,
such as KSC's own Launch Control Center.

-_-_-_-_-_-_ METRICS _-_-_-_-_-_-
Original length: 6035 characters
Smooshed length: 1411 characters
Original smooshed by 76.62%
```

## Issues
If you think you've found a bug, please open an issue! Or, if you're feeling extra special, fork, fix the problem yourself, and open a new pull request. Please make sure to check the current issues before opening a new one to ensure we don't have duplicates.
