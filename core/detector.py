import os
import cv2
import numpy as np
from dataclasses import dataclass
from typing import List

@dataclass
class DetectionMetrics:
    total_particles: int
    mean_particle_size_px: float
    surface_contamination_index: str
    annotated_image_filename: str

class DustParticleEngine:
    def __init__(self, min_area: int = 3, max_area: int = 300, min_circularity: float = 0.35):
        self.min_area = min_area
        self.max_area = max_area
        self.min_circularity = min_circularity
        # 15x15 pixel rectangular structuring element to extract small bright features
        self.kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))

    def analyze(self, image_path: str, output_dir: str) -> DetectionMetrics:
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not decode image from file.")

        # Step A: Convert to single-channel 8-bit grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step B: Contrast Limited Adaptive Histogram Equalization (CLAHE)
        # Prevents room shadows and dim lighting from skewing detection
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        contrast_adjusted = clahe.apply(gray)

        # Step C: White Top-Hat Transform
        # Computes: Input Image - Morphological Opening
        # Result: Leaves ONLY features that are brighter than their local background
        tophat = cv2.morphologyEx(contrast_adjusted, cv2.MORPH_TOPHAT, self.kernel)

        # Step D: Automatic thresholding via Otsu's algorithm
        _, binary = cv2.threshold(tophat, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Step E: Morphological Opening (Erosion followed by Dilation) to drop 1-pixel camera noise
        noise_kernel = np.ones((2, 2), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, noise_kernel)

        # Step F: Extract contours of remaining candidate particles
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        annotated = img.copy()
        valid_areas: List[float] = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if self.min_area <= area <= self.max_area:
                perimeter = cv2.arcLength(cnt, True)
                if perimeter == 0:
                    continue

                # Mathematical Circularity: 4 * pi * Area / (Perimeter^2)
                # True spheres/dots score near 1.0; long fibers/hair score near 0.0
                circularity = (4 * np.pi * area) / (perimeter * perimeter)
                if circularity >= self.min_circularity:
                    valid_areas.append(area)
                    (x, y), radius = cv2.minEnclosingCircle(cnt)
                    # Draw a high-visibility target ring around each particle
                    cv2.circle(annotated, (int(x), int(y)), max(int(radius) + 2, 4), (0, 180, 255), 1)

        total_count = len(valid_areas)
        mean_size = float(np.mean(valid_areas)) if total_count > 0 else 0.0

        # Heuristic Cleanliness Rating
        if total_count < 15:
            rating = "Clean (Low Contamination)"
        elif total_count <= 60:
            rating = "Moderate Contamination"
        else:
            rating = "Critical (Cleaning Recommended)"

        output_filename = f"inspected_{os.path.basename(image_path)}"
        cv2.imwrite(os.path.join(output_dir, output_filename), annotated)

        return DetectionMetrics(
            total_particles=total_count,
            mean_particle_size_px=round(mean_size, 2),
            surface_contamination_index=rating,
            annotated_image_filename=output_filename
        )
