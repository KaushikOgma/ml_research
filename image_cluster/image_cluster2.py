import os
import cv2
import torch
import numpy as np
from tqdm import tqdm
from typing import List, Tuple, Dict
from insightface.app import FaceAnalysis
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize
from collections import defaultdict
import shutil


def initialize_face_analysis() -> FaceAnalysis:
    ctx_id = 0 if torch.cuda.is_available() else -1
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=ctx_id)
    return app


def extract_faces_with_embeddings(app: FaceAnalysis, image_path: str) -> List[Tuple[np.ndarray, str]]:
    """Returns list of (embedding, image_path) for each face found in an image."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Cannot read image: {image_path}")
        return []
    
    try:
        faces = app.get(img)
        return [(face.embedding / np.linalg.norm(face.embedding), image_path) for face in faces]
    except Exception as e:
        print(f"[ERROR] Face extraction failed for {image_path}: {e}")
        return []


def cluster_images_by_unique_faces(image_dir: str, output_dir: str = "unique_face_clusters", eps: float = 0.35, min_samples: int = 1):
    app = initialize_face_analysis()

    embeddings = []
    image_paths = []

    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    print(f"[INFO] Extracting embeddings from {len(image_files)} images...")
    for file in tqdm(image_files, desc="Extracting Faces"):
        path = os.path.join(image_dir, file)
        faces = extract_faces_with_embeddings(app, path)
        for emb, img_path in faces:
            embeddings.append(emb)
            image_paths.append(img_path)

    if not embeddings:
        print("[FATAL] No faces found in dataset.")
        return

    # Normalize and cluster
    print(f"[INFO] Clustering {len(embeddings)} faces using DBSCAN...")
    embeddings = normalize(embeddings)
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(embeddings)
    labels = clustering.labels_

    # Map: cluster_id -> set of image paths
    cluster_to_images: Dict[int, set] = defaultdict(set)
    for label, img_path in zip(labels, image_paths):
        if label == -1:
            continue  # skip noise
        cluster_to_images[label].add(img_path)

    print(f"[INFO] Found {len(cluster_to_images)} unique face clusters.")
    os.makedirs(output_dir, exist_ok=True)

    # Save full images into each cluster folder (may be duplicated)
    for cluster_id, img_paths in cluster_to_images.items():
        cluster_folder = os.path.join(output_dir, f"cluster_{cluster_id}")
        os.makedirs(cluster_folder, exist_ok=True)
        for img_path in img_paths:
            try:
                filename = os.path.basename(img_path)
                dest_path = os.path.join(cluster_folder, filename)
                shutil.copy(img_path, dest_path)
            except Exception as e:
                print(f"[ERROR] Could not copy {img_path} to cluster {cluster_id}: {e}")

    print(f"[✅] Completed. Images grouped into {len(cluster_to_images)} unique face clusters at '{output_dir}'.")


# Example usage
if __name__ == "__main__":
    cluster_images_by_unique_faces(image_dir="images", output_dir="unique_face_clusters", eps=0.35, min_samples=1)