## Requirements

 - Docker
 - Python 3.10
 - Pip

## How to install

 1. Clone this repository `git clone https://github.com/firebenderyt123/wikiracing.git`
 2. Open the wikiracing folder `cd wikiracing`
 3. Install the python requirements `python3 -m pip install -r requirements.txt`

## How to run

1. Run the postgres container `docker compose up -d`
2. Run the program `python3 main.py`

## Parameters

You can use parameters to run the program
 - Use `-h` to get help
 - Use `-s <start>` or `--start <start>` to set title of page where the search is beginning
 - Use `-f <finish>` or `--finish <finish>` to set title of page where the search  is  ending

## Examples

 - [x] `python3 main.py`
 - [x] `python3 main.py -s Дружба -f Рим`
 - [x] `python3 main.py --start "Мітохондріальна ДНК" --finish "Вітамін K"`

## Tests

To run tests use this command `python3 -m unittest wikiracing_test.py`