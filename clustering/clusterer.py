# clustering/clusterer.py

from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint, mapping, Point
import geojson
import config
from .utils import filter_valid_reports

def run_dbscan(raw_reports):
    valid = filter_valid_reports(raw_reports)
    # extract as (lat, lon)
    points = [(r['longitude'], r['latitude']) for r in valid]

    if not points:
        return geojson.FeatureCollection([])

    # Try clustering
    clustering = DBSCAN(
        eps=config.DBSCAN_EPS,
        min_samples=config.DBSCAN_MIN_SAMPLES  # you can lower this in config.py
    ).fit(points)
    labels = clustering.labels_

    features = []
    for label in set(labels):
        if label == -1:
            continue
        cluster_pts = [points[i] for i, lab in enumerate(labels) if lab == label]
        hull = MultiPoint(cluster_pts).convex_hull
        poly_geo = mapping(hull)
        features.append(
            geojson.Feature(
                geometry=poly_geo,
                properties={'cluster_id': int(label), 'count': len(cluster_pts)}
            )
        )

    # **Fallback**: if DBSCAN found no clusters, just return each point as a Feature
    if not features:
        for idx, (lon, lat) in enumerate(points):
            pt = geojson.Feature(
                geometry=geojson.Point((lon, lat)),
                properties={'cluster_id': idx, 'count': 1}
            )
            features.append(pt)

    return geojson.FeatureCollection(features)
