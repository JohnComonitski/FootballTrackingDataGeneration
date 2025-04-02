import supervision as sv
from sports.common.team import TeamClassifier
from sports.annotators.soccer import draw_pitch
from sports.configs.soccer import SoccerPitchConfiguration
from sports.annotators.soccer import draw_pitch, draw_paths_on_pitch, draw_points_on_pitch
from sports.common.view import ViewTransformer
from supervision.draw.utils import draw_image
import numpy as np
from tqdm import tqdm
import csv
from FootballTrackingDataGeneration.data_cleanup.lib.detection_classes import Coordinate, Detections, Rect

FILE_NAME = ''
CSV_PATH = './track/output/' + FILE_NAME
SOURCE_VIDEO_PATH = './track/footage/' + FILE_NAME

ellipse_annotator = sv.EllipseAnnotator(
    color=sv.ColorPalette.from_hex(['#00BFFF', '#FF1493', '#FFD700']),
    thickness=2
)
label_annotator = sv.LabelAnnotator(
    color=sv.ColorPalette.from_hex(['#00BFFF', '#FF1493', '#FFD700']),
    text_color=sv.Color.from_hex('#000000'),
    text_position=sv.Position.BOTTOM_CENTER
)
triangle_annotator = sv.TriangleAnnotator(
    color=sv.Color.from_hex('#FFD700'),
    base=25,
    height=21,
    outline_thickness=1
)

players = {}
ball = {}
i = 0
with open(CSV_PATH, 'r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
      if(i != 0):
        obj_type = row[1]
        if(obj_type == "player"):
          player_id = row[2]
          if player_id not in players:
            players[player_id] = {}

          frame = row[0]
          if(frame not in players[player_id]):
            players[player_id][frame] = {
                "Object" : obj_type,
                "Team ID" : row[3],
                "X1" : row[4],
                "Y1" : row[5],
                "X2" : row[6],
                "Y2" : row[7],
                "X_Pitch" : row[8],
                "Y_Pitch" : row[9],
            }
        else:
          frame = row[0]
          if(frame not in ball):
            ball[frame] = {
                "Object" : obj_type,
                "X1" : row[4],
                "Y1" : row[5],
                "X2" : row[6],
                "Y2" : row[7],
                "X_Pitch" : row[8],
                "Y_Pitch" : row[9],
            }
      i += 1

video_info = sv.VideoInfo.from_video_path(video_path=SOURCE_VIDEO_PATH)
frame_generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)
CONFIG = SoccerPitchConfiguration()

frame_number = 1
with sv.VideoSink(target_path="./output.mp4", video_info=video_info) as sink:
  for frame in tqdm(frame_generator, desc='Collecting Tracking Data...'):
    player_xys = []
    home_player_pitch_xys = []
    away_player_pitch_xys = []
    label_xys = []
    teams = []
    ball_xys = []
    ball_pitch_xys = []
    labels = []

    for player_id in players:
      player = players[player_id]
      if str(frame_number) in player:
        player_data = player[str(frame_number)]
        xy = Coordinate(float(player_data["X1"]), float(player_data["Y1"]), float(player_data["X2"]), float(player_data["Y2"]))
        player_xys.append(xy)
        if(float(player_data["Team ID"]) < 1):
          home_player_pitch_xys.append([float(player_data["X_Pitch"]), float(player_data["Y_Pitch"])])
        else:
          away_player_pitch_xys.append([float(player_data["X_Pitch"]), float(player_data["Y_Pitch"])])
        xy = Coordinate(float(player_data["X1"]), float(player_data["Y1"])-40, float(player_data["X2"]), float(player_data["Y2"]))
        label_xys.append(xy)
        labels.append("Player #" + player_id)
        teams.append(int(float(player_data["Team ID"])))

    if str(frame_number) in ball:
      ball_data = ball[str(frame_number)]
      xy = Coordinate(float(ball_data["X1"])+17, float(ball_data["Y1"])+10, float(ball_data["X2"]), float(ball_data["Y2"]))
      ball_xys.append(xy)
      ball_pitch_xys.append([float(ball_data["X_Pitch"]), float(ball_data["Y_Pitch"])])

    detects = Detections(player_xys, teams)
    label_detects = Detections(label_xys, teams)

    annotated_frame = frame.copy()
    pitch_frame = draw_pitch(CONFIG)

    pitch_frame = draw_points_on_pitch(
        config=CONFIG,
        xy=ball_pitch_xys,
        face_color=sv.Color.WHITE,
        edge_color=sv.Color.BLACK,
        radius=10,
        pitch=pitch_frame)
    pitch_frame = draw_points_on_pitch(
        config=CONFIG,
        xy=home_player_pitch_xys,
        face_color=sv.Color.from_hex('00BFFF'),
        edge_color=sv.Color.BLACK,
        radius=16,
        pitch=pitch_frame)

    pitch_frame = draw_points_on_pitch(
        config=CONFIG,
        xy=away_player_pitch_xys,
        face_color=sv.Color.from_hex('FF1493'),
        edge_color=sv.Color.BLACK,
        radius=16,
        pitch=pitch_frame)

    annotated_frame = draw_image(
        scene=annotated_frame,
        image=pitch_frame,
        opacity=0.75,
        rect=Rect(75,75,600,350)
    )

    annotated_frame = ellipse_annotator.annotate(
        scene=annotated_frame,
        detections=detects
    )

    annotated_frame = label_annotator.annotate(
        scene=annotated_frame,
        detections=label_detects,
        labels=np.array(labels))

    ball_detects = Detections(ball_xys, np.array([0]))
    annotated_frame = triangle_annotator.annotate(
        scene=annotated_frame,
        detections=ball_detects)

    sink.write_frame(frame=annotated_frame)
    frame_number += 1