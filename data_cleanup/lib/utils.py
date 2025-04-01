import math
import numpy as np
from scipy import interpolate
from scipy.signal import find_peaks

from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import kneighbors_graph, KDTree
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RANSACRegressor

from scipy.linalg import expm
from filterpy.kalman import KalmanFilter
from filterpy.common import Q_discrete_white_noise

def fill_gap( x1, y1, x2, y2, gap_size ):
    points = []
    for i in range(1, gap_size + 1):
        t = i / (gap_size + 1)
        x_new = float(x1) + t * (float(x2) - float(x1))
        y_new = float(y1) + t * (float(y2) - float(y1))
        points.append((x_new, y_new))
    return points

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def filter_lone_points(source, coordinates):
    threshold = 0.02
    if(source == "raw"):
        threshold = 200

    filtered_coordinates = []
    for i, (x, y, z) in enumerate(coordinates):
        has_nearby_point = False
        
        for j, (x2, y2, _) in enumerate(coordinates):
            if( i != j and distance((x, y), (x2, y2)) <= threshold ):
                has_nearby_point = True
                break
        
        if has_nearby_point:
            filtered_coordinates.append((x, y, z))
    return filtered_coordinates

def near_by_filter(source, coordinates):
    threshold = 0.2
    if(source == "raw"):
        threshold = 2000

    filtered_coordinates = []
    for i, (x, y, z) in enumerate(coordinates):
        if (x, y) == (0, 0):
            continue

        if not filtered_coordinates:
            filtered_coordinates.append((x, y, z))
        else:
            prev_x, prev_y, prev_z = filtered_coordinates[-1]
            if(distance((x, y), (prev_x, prev_y)) <= threshold):
                filtered_coordinates.append((x, y, z))
    return filtered_coordinates

def remove_arcs_from_path(coordinates):
    # Original Code: https://github.com/fenaux/soccer-applications/blob/main/path_radar.ipynb
    path_raw = []
    for coordinate in coordinates:
        path_raw.append([coordinate[2], coordinate[0], coordinate[1]])
    path_raw = np.array(path_raw)

    traj = path_raw.copy()
    reg_frames = traj.copy()

    fs = 25
    Xraw = path_raw.copy()

    scaler = StandardScaler()
    X = scaler.fit_transform(Xraw)
    X[:,0] *= 2
    tree = KDTree(X)
    dist, ind = tree.query(X, k=max(fs//3, 10))
    thresh = 2*np.quantile(dist[:,-1], 0.5)

    knn_graph = kneighbors_graph(X[:,0].reshape(-1,1), 5, include_self=False)
    clustering = AgglomerativeClustering(n_clusters=None, linkage='single',
                                        connectivity=knn_graph, distance_threshold=thresh)
    clustering.fit(X)

    labs, n_in_labs = np.unique(clustering.labels_, return_counts=True)
    outs = np.array([])
    for lab, n_in in zip(labs, n_in_labs):
        if n_in < 3:
            outs = np.append(outs, np.where(clustering.labels_== lab)[0])
    outs = np.sort(outs).astype(np.int16)

    path_xy_val = np.delete(path_raw, outs, axis=0)
    f = interpolate.interp1d(path_xy_val[:,0], path_xy_val[:,1:], axis=0, fill_value='extrapolate')
    frames = np.arange(path_raw[-1,0]+1)
    path_int = f(frames)

    dim_x = 4
    A = np.zeros((dim_x,dim_x))
    for i in range(dim_x-1): A[i, i+1] = 1
    dt = 1

    f = KalmanFilter (dim_x=dim_x, dim_z=1)
    f.F = expm(A * dt )

    f.H = np.zeros((1,dim_x))
    f.H[0,0] = 1
    f.P *= 10.
    f.R = 100**2

    varQ = 10
    f.Q = Q_discrete_white_noise(dim=dim_x, dt=dt, var=varQ**2)

    zs = path_int[:,1].copy()

    f.x = np.zeros((dim_x,1))
    f.x[0,0] = zs[0]
    mu, cov, _, _ = f.batch_filter(zs)
    xs, Ps, Ks,_ = f.rts_smoother(mu, cov)

    traj = xs.squeeze()[:,0]
    deltas = traj - zs

    path_int_save = path_int.copy()
    for i_loop in range(5):
        for i in range(2):

            zs = path_int[:,i].copy()
            #f.x = np.array([[zs[0], 0, 0]]).T
            f.x = np.zeros((dim_x,1))
            f.x[0,0] = zs[0]
            mu, cov, _, _ = f.batch_filter(zs)
            xs, Ps, Ks,_ = f.rts_smoother(mu, cov)
            if i==0:
                traj = xs.squeeze()[:,0].copy()
                d_path = xs.squeeze()[:,1].copy()
                d2_path = xs.squeeze()[:,2].copy()
            else:
                traj = np.vstack((traj, xs.squeeze()[:,0])).T
                d_path = np.vstack((d_path, xs.squeeze()[:,1])).T
                d2_path = np.vstack((d2_path, xs.squeeze()[:,2])).T

        deltas = np.abs(traj - path_int)
        thresholds = 5 * np.median(deltas,axis=0)

        for i in range(2):
            path_int[:,i] = np.where(deltas[:,i] < thresholds[i], path_int[:,i], traj[:,i])

    reg = RANSACRegressor(random_state=1, residual_threshold = 50)
    reg.fit(traj[500:,1].reshape(-1,1), traj[500:,0])

    all_ins=[]

    traj_reg = traj.copy()
    reg_frames = frames.copy()
    ins = []
    long_seg = True
    i = 0
    while long_seg:

        reg1 = RANSACRegressor(random_state=i, residual_threshold = 50 )
        reg1.fit(traj_reg[:,0].reshape(-1,1), traj_reg[:,1])
        frames_in_reg_1 = reg_frames[reg1.inlier_mask_]

        clustering1 = AgglomerativeClustering(n_clusters=None, linkage='single',
                                            distance_threshold=15)
        clustering1.fit(frames_in_reg_1.reshape(-1,1))
        labs1, n_in_labs1 = np.unique(clustering1.labels_, return_counts=True)

        reg2 = RANSACRegressor(random_state=i, residual_threshold = 50 )
        reg2.fit(traj_reg[:,1].reshape(-1,1), traj_reg[:,0])
        frames_in_reg_2 = reg_frames[reg2.inlier_mask_]

        clustering2 = AgglomerativeClustering(n_clusters=None, linkage='single',
                                            distance_threshold=15)
        clustering2.fit(frames_in_reg_2.reshape(-1,1))
        labs2, n_in_labs2 = np.unique(clustering2.labels_, return_counts=True)

        n_max = max(n_in_labs1.max(), n_in_labs2.max())
        long_seg = n_max > 25

        if long_seg:

            if n_in_labs1.max() > n_in_labs2.max():
                new_ins = frames_in_reg_1[clustering1.labels_== np.argmax(n_in_labs1)].astype(np.int16)
            else:
                new_ins = frames_in_reg_2[clustering2.labels_== np.argmax(n_in_labs2)].astype(np.int16)

            ins.append(new_ins)
            indexes = np.searchsorted(reg_frames, new_ins)
            reg_frames = np.delete(reg_frames, indexes)
            traj_reg = np.delete(traj_reg, indexes, axis=0)
            i += 1
        else:
            all_ins = np.hstack(ins)

    acc = np.linalg.norm(d2_path, axis=1)
    # Prominence controls peak threshold
    peaks, properties = find_peaks(acc, distance= int(0.8*fs), prominence=20)

    debs = np.sort(np.array([seg[0] for seg in ins]))
    ends = np.sort(np.array([seg[-1] for seg in ins]))

    peaks_in = []
    for end, deb in zip(ends[:-1], debs[1:]):
        in_between = np.logical_and(peaks >= end + 8, peaks <= deb - 8)
        peaks_in.append(peaks[in_between])
    new_pts = np.hstack(peaks_in)

    vertices = np.hstack((debs, ends, new_pts, [0, frames[-1]]))
    vertices = np.sort(np.unique(vertices)).astype(np.int16)

    f = interpolate.interp1d(vertices, traj[vertices], axis=0, fill_value='extrapolate')
    path_radar = f(frames)

    cleaned_path = []
    for frame in range(len(coordinates)):
        cleaned_path.append((float(path_radar[int(frame)-1][0]), float(path_radar[int(frame)-1][1])))
    return cleaned_path