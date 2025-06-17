import os
import cv2
import torch
import numpy as np
from tqdm import tqdm
from typing import List, Tuple
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
from insightface.app import FaceAnalysis


def initialize_face_analysis() -> FaceAnalysis:
    """Initialize InsightFace FaceAnalysis model with GPU (if available)."""
    ctx_id = 0 if torch.cuda.is_available() else -1
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=ctx_id)
    return app


def extract_face_embeddings(app: FaceAnalysis, image_path: str) -> List[Tuple[np.ndarray, List[int], np.ndarray]]:
    """
    Extract normalized face embeddings from a single image.

    Returns:
        List of tuples (embedding, bounding_box, image_array)
    """
    img = cv2.imread(image_path)
    if img is None:
        print(f"[ERROR] Could not read image: {image_path}")
        return []
    
    try:
        faces = app.get(img)
        return [(face.embedding / np.linalg.norm(face.embedding), face.bbox, img) for face in faces]
    except Exception as e:
        print(f"[ERROR] Face extraction failed for {image_path}: {e}")
        return []


def compute_similarity(embedding: np.ndarray, reference_embeddings: np.ndarray) -> float:
    """Compute maximum cosine similarity between a face embedding and a set of reference embeddings."""
    similarities = cosine_similarity([embedding], reference_embeddings)[0]
    return np.max(similarities)


def save_matched_image(img_path: str, output_dir: str, filename: str) -> None:
    """Save image to output directory if it matches."""
    try:
        img = cv2.imread(img_path)
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, filename)
        cv2.imwrite(save_path, img)
    except Exception as e:
        print(f"[ERROR] Failed to save image {img_path}: {e}")


def match_faces(image_dir: str, reference_image_path: str, similarity_threshold: float = 0.30) -> None:
    """
    Main function to match faces in a dataset against a reference face.
    
    Args:
        image_dir: Directory of images to process.
        reference_image_path: Path to the reference face image.
        similarity_threshold: Threshold for cosine similarity.
    """
    # Step 1: Setup
    app = initialize_face_analysis()
    ref_name = os.path.splitext(os.path.basename(reference_image_path))[0]
    output_dir = os.path.join('matched_faces', ref_name)

    # Step 2: Extract Reference Embeddings
    print(f"[INFO] Extracting face embeddings from reference image: {reference_image_path}")
    ref_results = extract_face_embeddings(app, reference_image_path)
    if not ref_results:
        print("[FATAL] No face found in reference image. Exiting.")
        return
    
    ref_embeddings = normalize(np.array([emb[0] for emb in ref_results]))

    # Step 3: Process Dataset
    print(f"[INFO] Processing images in directory: {image_dir}")
    image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for image_file in tqdm(image_files, desc="Matching Faces"):
        img_path = os.path.join(image_dir, image_file)
        detected_faces = extract_face_embeddings(app, img_path)
        if not detected_faces:
            print(f"[SKIP] {image_file} — No faces detected.")
            continue

        match_found = False
        for emb, _, _ in detected_faces:
            similarity = compute_similarity(emb, ref_embeddings)
            if similarity >= similarity_threshold:
                print(f"[MATCH ✅] {image_file} — Similarity: {similarity:.3f}")
                save_matched_image(img_path, output_dir, image_file)
                match_found = True
                break

        if not match_found:
            print(f"[NO MATCH ❌] {image_file} — All similarities below {similarity_threshold}")

    print(f"\n✅ Matching complete. Matched images saved to: {output_dir}")


# Example usage
if __name__ == "__main__":
    match_faces(
        image_dir="images",
        reference_image_path="images/IMG_20230621_062731.jpg",
        similarity_threshold=0.30
    )
