# Football Tracking Data Generation
Convert Football footage into proffesional level player & ball tracking data 

### Table of Contents
<!--TOC-->
- [Football Tracking Data Generation](fFootball-tracking-data-generation)
  - [Getting Started](#getting-started)
  - [Match Footage to Tracking Data Pipeline](#match-footage-to-tracking-data-Pipeline)
    - [Training a Player Detection Model](training-a-player-detection-model)
    - [Tracking Match Footage](tracking-match-footage)
    - [Cleaning Tracking Data](cleaning-tracking-data)
    - [Generating Tracking Clips](generating-tracking-clips)
  - [Resources](#resources)
  - [Licenses](#license)

## Getting Started
1. Clone the repository

    ```shell
    git clone https://github.com/JohnComonitski/FootballTrackingDataGeneration.git
    ```

2. Move to the project directory

    ```shell
    cd FootballTrackingDataGeneration
    ```

3. Create and activate a Python
    [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments).
    On GNU/Linux systems this is as easy as:

    ```shell
    python3 -m venv .venv
    . .venv/bin/activate
    # Work inside the environment.
    ```

4. Install the Python dependencies
    ```shell
    pip install -r requirements.txt
    ```

5. Get a Roboflow API Key
    Create an account with [Roboflow](https://roboflow.com/) and get an API key.

6. Create env.py

    ```shell
    touch env.py
    ```

7. Add your API Key to env.py

    ```python
    keys = {
        "roboflow_api" : "ROBOFLOW API KEY HERE"
    }
    ```

## Match Footage to Tracking Data Pipeline
...

### Training a Player Detection Model
How to Train

### Tracking Match Footage
How to Track

### Cleaning Tracking Data
How to use the event data cleaning library

### Generating Tracking Clips
Turn cleaned tracking data into event data footage

## Resources
- [Skalskip92's Football AI Tutorial: From Basics to Advanced Stats with Python](https://www.youtube.com/watch?v=aBVGKoNZQUw) - Essential to getting this project off the group and the foundation of the tracking & training notebook.
- [Roboflow's Training of a Pitch Key Point Detection Model Notebook](https://colab.research.google.com/github/roboflow/sports/blob/main/examples/soccer/notebooks/train_pitch_keypoint_detector.ipynb) - Use Roboflow's tools & libraries to train and deploy a pitch key point detection model.
- [Roboflow's Training of a Player Key Point Detection Model Notebook](https://colab.research.google.com/github/roboflow/sports/blob/main/examples/soccer/notebooks/train_pitch_keypoint_detector.ipynb) - Use Roboflow's tools & libraries to train and deploy a player detection model.
- [Skalskip92's Football-AI Notebook](https://colab.research.google.com/github/roboflow-ai/notebooks/blob/main/notebooks/football-ai.ipynb) - Skalskip92's tracking data generation collab notebook.
- [Eric Fenaux's Football-AI Improvements](https://github.com/fenaux/soccer-applications/blob/main/Ball_radar.ipynb) - I utilized his techniques to remove arcs from the ball's path.
- [ML with Hamza's Computer Vision for Football Analysis in Python with Yolov8 & OpenCV](https://www.youtube.com/watch?v=yJWAtr3kvPU) - Hamza's approach to solving this same problem with an interesting and faster approach to team detection (that I hope to implement soon).
- [Mihailo Radović's Football-AI Improvements](https://x.com/skalskip92/status/1843644812953883128) - Several key improvements & features such as ball possession determination, player speed estimation & significant processing speed optimization.

## Licenses
MIT License
Copyright (c) 2025 John Comonitski