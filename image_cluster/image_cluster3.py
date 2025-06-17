import os
import cv2
import torch
import numpy as np
from tqdm import tqdm
from typing import List, Tuple
from insightface.app import FaceAnalysis
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize
import shutil


def initialize_face_analysis() -> FaceAnalysis:
    ctx_id = 0 if torch.cuda.is_available() else -1
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=ctx_id)
    return app


def extract_faces_with_embeddings(app: FaceAnalysis, image_path: str) -> List[Tuple[np.ndarray, np.ndarray, Tuple[int, int, int, int], str]]:
    """
    Returns a list of (embedding, original image, face bbox, image_path)
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Cannot read image: {image_path}")
        return []

    try:
        faces = app.get(img)
        results = []
        for face in faces:
            emb = face.embedding / np.linalg.norm(face.embedding)
            bbox = tuple(map(int, face.bbox))  # (x1, y1, x2, y2)
            results.append((emb, img, bbox, image_path))
        return results
    except Exception as e:
        print(f"[ERROR] Face extraction failed for {image_path}: {e}")
        return []


def save_unique_faces(image_dir: str, output_dir: str = "unique_faces", eps: float = 0.35, min_samples: int = 1):
    app = initialize_face_analysis()

    embeddings = []
    face_data = []  # (img, bbox, image_path)

    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    print(f"[INFO] Extracting face embeddings from {len(image_files)} images...")
    for file in tqdm(image_files, desc="Processing Images"):
        path = os.path.join(image_dir, file)
        faces = extract_faces_with_embeddings(app, path)
        for emb, img, bbox, img_path in faces:
            embeddings.append(emb)
            face_data.append((img, bbox, img_path))

    if not embeddings:
        print("[FATAL] No faces found in the dataset.")
        return

    print(f"[INFO] Clustering {len(embeddings)} faces...")
    embeddings = normalize(embeddings)
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='cosine').fit(embeddings)
    labels = clustering.labels_

    print(f"[INFO] Found {len(set(labels) - {-1})} unique face clusters.")

    os.makedirs(output_dir, exist_ok=True)
    saved_clusters = set()

    for i, label in enumerate(labels):
        if label == -1 or label in saved_clusters:
            continue  # Skip noise and already saved clusters

        img, bbox, img_path = face_data[i]
        x1, y1, x2, y2 = bbox
        face_crop = img[y1:y2, x1:x2]
        save_path = os.path.join(output_dir, f"face_cluster_{label}.jpg")
        try:
            cv2.imwrite(save_path, face_crop)
            saved_clusters.add(label)
        except Exception as e:
            print(f"[ERROR] Could not save face for cluster {label}: {e}")

    print(f"[✅] Saved {len(saved_clusters)} unique face crops to '{output_dir}'.")


# Example usage
if __name__ == "__main__":
    save_unique_faces(image_dir="images", output_dir="unique_faces", eps=0.40, min_samples=1)