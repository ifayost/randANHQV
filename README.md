# randANHQV - Random Aqui No Hay Quien Viva Episode Selector

When I go to bed I like to fall asleep watching a random episode of ANHQV but I don't want to decide which episode to watch. I just want to see a random episod which I haven't seen recently. This script provides an organized and probabilistic approach to selecting episodes based on viewing history.

## Features

- **Weighted Random Selection**: Uses dynamic probability weights based on how many times episodes have been viewed
- **Season Filtering**: Ability to focus on specific seasons or view across all seasons
- **Browser Integration**: Built-in browser automation for playing selected episodes
- **Statistics Tracking**: Keeps track of viewing history and episode counts
- **Customizable Probability Parameters**: Adjust the weighting factors to control randomness

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/randANHQV.git
```

2. Create virtual environment and install Python dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Set up credentials (first run):
```python
python randANHQV.py
```

## Usage

```
usage: randANHQV [-h] [-s [SEASONS ...]] [--uniform] [--nonorm] [--reset-stats]

                    __                     __
 .---.-.-----.--.--|__|   .-----.-----.   |  |--.---.-.--.--.
 |  _  |  _  |  |  |  |   |     |  _  |   |     |  _  |  |  |
 |___._|__   |_____|__|   |__|__|_____|   |__|__|___._|___  |
          |__|__                       __             |_____|
 .-----.--.--|__.-----.-----.   .--.--|__.--.--.---.-.
 |  _  |  |  |  |  -__|     |   |  |  |  |  |  |  _  |
 |__   |_____|__|_____|__|__|    \___/|__|\___/|___._|
    |__|

Open a random ANHQV episode.

options:
  -h, --help            show this help message and exit
  -s, --seasons [SEASONS ...]
                        Seasons space separated. Ex: --seasons 3 4 5
  --uniform             All episodes have the same chancex of being selected
  --nonorm              Disable probability normalization among seasons
  --reset-stats         Reset episode statistics before selection

```
The script can be run from the command line with various options:

### Basic Usage
```bash
python randANHQV.py
```

This will randomly select and suggest an episode based on weighted probabilities.

### Optional Arguments
- Filter by specific seasons:
```bash
python randANHQV.py --seasons 3 4 5
```

- Uniform random selection (no weighting):
```bash
python randANHQV.py --uniform
```

- Disable normalization by season:
```bash
python randANHQV.py --nonorm
```

### Statistics Management

The script maintains the count of the season and episodes viewed in a CSV file. You can:

- Reset all statistics:
```bash
python randANHQV.py --reset-stats
```

## How It Works

1. **Data Collection**: Scrapes episode information from Prime Video
2. **Probability Calculation**: Uses weighted probabilities based on:
   - Episode view count (`episode_count`)
   - Season view count (`season_count`)
   - Custom weighting factors (controlled by `POWER` and `POWER_SEASON` in the randANHQV.py)
3. **Random Selection**: Selects an episode based on calculated probabilities
4. **Browser Integration**: Opens the selected episode in your default browser

## Statistics Tracking

The script maintains two key metrics for each episode:
- `episode_count`: Number of times the specific episode has been viewed
- `season_count`: Number of times any episode in that season has been viewed

These counts are saved in a CSV file and used to calculate viewing probabilities.

### Probability Formula
```python
pseudo_probs = 1 / (1 + episode_count) ** power
normalized_probs = pseudo_probs / (sum of probs for other seasons) ** power_season
final_probs = normalized_probs / sum(all probs)
```

## Notes

- The script requires Selenium for browser automation. Make sure to install the appropriate WebDriver for your browser.
- Supported browsers: Safari

## TODO
- [ ] Add other browsers integration

