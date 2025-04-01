# Football Tracking Data Generation
Convert football match footage into proffesional level player & ball tracking data utilizing [Roboflow's](https://roboflow.com/) machine learning and computer vision libraries. The goal of this project is to enable clubs at any level to turn their match footage into match tracking data and match event data they can use to step step their match analysis to the next level!
![Tracking Example](./examples/tracking.png)


### Table of Contents
<!--TOC-->
- [Football Tracking Data Generation](fFootball-tracking-data-generation)
  - [Getting Started](#getting-started)
  - [Match Footage to Tracking Data Pipeline](#match-footage-to-tracking-data-Pipeline)
    - Training a Player Detection Model
    - Tracking Match Footage
    - Cleaning Tracking Data
    - Generating Tracking Clips
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
  > [!NOTE]
  > This project was built with Python 3.11


4. Install the Python dependencies
    ```shell
    pip install -r requirements.txt
    ```
  > [!NOTE]
  > **_requirements.txt_** includes commented out packages which utilize your GPU. If your machine has a GPU, I recommend you uncomment out those packages.

5. Get a Roboflow API Key
   
    Create an account with [Roboflow](https://roboflow.com/) and get an API key.

6. Create env/keys.env

    ```shell
    touch env/keys.env
    ```

7. Add your API Key to env/keys.env

    ```
    ROBOFLOW_API=XXXXXXXXXXXXXXX
    ```

## Match Footage to Tracking Data Pipeline
...

### Training a Player Detection Model
The creation & training of a player detection model is performed by [train/train.ipynb](./train/train.ipynb). 

If you work through this notebook, you will have a player detection model capable of detecting players, balls and referees. Models will be saved to the [model](./model) directory. Once your model is trained, you are ready to start tracking match footage!

**Tips!**
- Training can take quite a long time. Depending on the resources available to your machine.
- If you are using a machine without a GPU, you may find faster training results using Google Collab and their (relatively) afforable GPU pricing.

### Tracking Match Footage
Tracking match footage is performed by [track/track.ipynb](./track/track.ipynb).

**How to Track Match Footage**
1. Copy the clip you would like to track to the [track/footage](./track/footage) directory.
2. Open [track/track.ipynb](./track/track.ipynb)
- If you want a tracking video output, set **_generate_video_** to **_1_** in the Configurations section:
    ```python
    generate_video = 1
    ```
> [!Warning] 
> The output at this stage will likely be rough and choppy tracking footage with many miss detections. I do not recommend you turn this on at this stage, as it will slow down tracking. This is best used as a reference to make sure your tracking is on the right track and not your final output.
- If you want teams tracked, set **_track_teams_** to **_1_** in the Configurations section:
    ```python
    track_teams = 1
    ```

3. Run the notebook to track the footage.
> [!Note] 
> Once complete, results will be saved to [track/output](./track/output) directory.

### Cleaning Tracking Data
Tracking results can be found in the [track/output](./track/output) directory as a CSV. Often the initial tracking results are imperfect and requires clean up. Tracking data can be cleaned from the [Cleanup Notebook](./data_cleanup/cleanup.ipynb) notebook. This notebook imports the Match library, which includes a series tools to evaluate & clean tracking results.

**How to Clean Tracking Data**
1. Open the [Cleanup Notebook](./data_cleanup/cleanup.ipynb)
2. Add the name of the file you wish to clean to the notebook in the **_Tracking Data Import_** section.
    ```python
    PATH = "./../track/output/"
    FILE_NAME = ""
    ```
3. Go to the **_Data Cleaning_** section. This is where you can work with the **_match_** object to clean your tracking data.
4. Once cleaning is complete, your results will be exported to the [data_cleanup/output](./data_cleanup/output) directory.


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