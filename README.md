<div>
  <img align="left" width="100px" src="terminal.svg" alt="Terminal icon" />
  <h1 margin="auto">monty-hall-visualization</h1>
</div>

A minimal, command-line visualizer built in [Python](http://www.python.org/) using [urwid](http://urwid.org/) to show the probabilities of the [Monty Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem).

[![Python](https://img.shields.io/badge/Python-3d79aa?style=for-the-badge)](https://www.python.org/)
[![urwid](https://img.shields.io/badge/urwid-grey?style=for-the-badge)](http://urwid.org/)

***This README is still being written and wil change.***

## Contents

- [Description](#description)
- [Requirements](#requirements)
- [Setup](#setup)
- [Running](#running)
- [Control](#controls)
- [Acknowledgements](#acknowledgements)

## Description

This is a terminal-based visualization of the [Monty Hall problem](https://en.wikipedia.org/wiki/Monty_Hall_problem). 
There are three doors, where a random door is picked as the winning door, a random door is chosen as the "initial pick", a random non-winning, un-selected door is revealed, and whether to stay or switch is randomly chosen.
Wins are sorted by whether or not the decision to stay or switch was made. The simulator can be sped up or slowed down.

The interface is built in [urwid](http://urwid.org/).

## Requirements

- To run the project, you will need:
  - [Python](https://www.python.org/) 3.7+
  - [urwid](https://pypi.org/project/urwid/)

## Setup

To install the project, just clone it from GitHub:

```shell script
git clone https://github.com/bradendubois/monty-hall-visualization
cd monty-hall-visualization
```

## Running

Run the ``MontyHall.py`` file in Python:
```shell script
python MontyHall.py
```

### Controls

- **Q**: Quit / Exit
- **S**, **space**: Toggle simulation
- **A**, **left arrow**: Decrease simulation speed
- **D**, **right arrow**: Increase simulation speed

## Acknowledgements

- The terminal icon used in my README is from [Font Awesome Free 5.2.0 by @fontawesome - https://fontawesome.com](https://fontawesome.com), licensed under the [Creative Commons](https://en.wikipedia.org/wiki/Creative_Commons) [Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/deed.en) license. Changes/alterations were not made to the image.
   - https://commons.wikimedia.org/wiki/File:Font_Awesome_5_solid_terminal.svg
