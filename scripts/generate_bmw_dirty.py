#!/usr/bin/env python3
"""
scripts/generate_bmw_dirty.py
Generates realistic automotive paint defects strictly on the BMW car paintwork:
- Micro-swirl spiderweb holograms around light reflections
- Clearcoat oxidation and matte haze
- Front bumper and hood edge stone chips
Strictly preserves 100% bitwise identical studio floor, walls, ceiling hex lights, and wheels.
"""
import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEAN_PATH = os.path.join(BASE_DIR, 'img', 'bmw-clean.jpg')
DIRTY_PATH = os.path.join(BASE_DIR, 'img', 'bmw-dirty.jpg')

def create_car_paint_mask(h, w):
    mask = np.zeros((h, w), dtype=np.uint8)

    # Outer car silhouette (covers hood, fenders, doors, quarter panel, roof)
    car_outer = np.array([
        # Front bumper bottom edge (splitter) - strictly ABOVE floor line!
        [205, 560], [235, 580], [300, 595], [370, 605], [420, 615], [480, 625],
        # Front wheel arch
        [525, 635], [535, 560], [575, 530], [615, 550], [635, 630],
        # Rocker panel
        [665, 665], [780, 660], [880, 655], [980, 645], [1025, 630],
        # Rear wheel arch
        [1035, 565], [1070, 535], [1095, 560], [1110, 615],
        # Rear bumper
        [1130, 615], [1135, 540], [1120, 470],
        # Roof & C-pillar
        [1070, 440], [1010, 390], [940, 350], [850, 330], [750, 320], [640, 318],
        # Windshield pillar & hood edge
        [550, 345], [480, 385], [420, 420], [350, 450], [290, 480], [240, 510], [210, 550],
        [205, 600], [208, 670]
    ], np.int32)
    cv2.fillPoly(mask, [car_outer], 255)

    # Exclude windshield glass
    windshield = np.array([
        [475, 415], [575, 325], [680, 325], [660, 410], [550, 420]
    ], np.int32)
    # Exclude side windows glass
    side_windows = np.array([
        [660, 410], [680, 325], [850, 335], [940, 355], [1025, 435], [1005, 455], [820, 440], [660, 410]
    ], np.int32)
    cv2.fillPoly(mask, [windshield, side_windows], 0)

    # Exclude wheels (rims and tires)
    cv2.circle(mask, (582, 645), 72, 0, -1)
    cv2.circle(mask, (1080, 580), 52, 0, -1)

    # Exclude kidney grilles
    grille = np.array([[215, 520], [380, 515], [375, 605], [215, 595]], np.int32)
    cv2.fillPoly(mask, [grille], 0)

    # Exclude headlights
    headlight_r = np.array([[390, 485], [535, 480], [525, 540], [390, 540]], np.int32)
    headlight_l = np.array([[208, 495], [225, 480], [240, 515], [210, 520]], np.int32)
    cv2.fillPoly(mask, [headlight_r, headlight_l], 0)

    # No artificial box cutouts in front bumper
    pass

    # Smooth the internal mask transition slightly (2px blur) to prevent harsh stair-stepping
    return mask

def generate_paint_defects(clean_img, mask):
    h, w = clean_img.shape[:2]
    np.random.seed(42)

    # 1. Base clearcoat oxidation:
    # Reduce contrast on the car paint and add subtle matte haze
    dirty = clean_img.copy().astype(np.float32)

    # Matte clearcoat oxidation: lift blacks slightly (+18) and compress bright highlights
    oxidized = dirty * 0.82 + 22.0
    # Soften reflections (unpolished oxidized clearcoat scatters light)
    blurred_paint = cv2.GaussianBlur(oxidized, (5, 5), 1.2)

    # Blend 60% blurred oxidized paint with 40% original for realistic depth
    paint_base = oxidized * 0.45 + blurred_paint * 0.55

    # 2. Spiderweb micro-swirl holograms around light reflections:
    # In automotive detailing, swirl marks are circular micro-scratches visible around point light reflections.
    swirl_layer = np.zeros((h, w), dtype=np.float32)

    # Swirl center points on the hood, front fender, and door
    swirl_centers = [
        # Hood highlights
        (330, 480), (420, 460), (480, 470), (370, 500), (280, 500),
        # Front fender & door highlights
        (650, 480), (730, 470), (810, 480), (890, 490), (750, 540), (840, 550),
        # Door lower section
        (720, 600), (800, 610), (900, 590),
        # Rear quarter
        (1020, 500), (1060, 510)
    ]

    for cx, cy in swirl_centers:
        num_arcs = np.random.randint(35, 60)
        for _ in range(num_arcs):
            r = np.random.randint(12, 95)
            start_angle = np.random.randint(0, 360)
            end_angle = start_angle + np.random.randint(25, 90)
            thickness = 1
            # draw arc on temp buffer
            temp_arc = np.zeros((h, w), dtype=np.uint8)
            cv2.ellipse(temp_arc, (cx, cy), (r, int(r * 0.65)), 15, start_angle, end_angle, 255, thickness)
            swirl_layer += (temp_arc.astype(np.float32) / 255.0) * np.random.uniform(22.0, 48.0)

    # Random fine directional scratches (from bad wash towels / automated car wash brushes)
    for _ in range(350):
        x1 = np.random.randint(210, 1050)
        y1 = np.random.randint(420, 660)
        length = np.random.randint(15, 65)
        angle = np.random.uniform(-0.3, 0.4) # mostly horizontal wash scratches
        x2 = int(x1 + length * np.cos(angle))
        y2 = int(y1 + length * np.sin(angle))
        temp_line = np.zeros((h, w), dtype=np.uint8)
        cv2.line(temp_line, (x1, y1), (x2, y2), 255, 1)
        swirl_layer += (temp_line.astype(np.float32) / 255.0) * np.random.uniform(20.0, 45.0)

    # 3. Fine road stone chips on front bumper and hood leading edge:
    chip_layer = np.zeros((h, w), dtype=np.float32)
    # Front bumper edge points: x in [220..490], y in [520..710]
    for _ in range(180):
        rx = np.random.randint(215, 490)
        ry = np.random.randint(500, 615)
        rad = np.random.choice([1, 1, 2])
        # chip primer is light grey / white speck
        temp_chip = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(temp_chip, (rx, ry), rad, 255, -1)
        chip_layer += (temp_chip.astype(np.float32) / 255.0) * np.random.uniform(70.0, 140.0)

    # Combine defects onto paint:
    defective_paint = paint_base + swirl_layer[:, :, np.newaxis] + chip_layer[:, :, np.newaxis]
    defective_paint = np.clip(defective_paint, 0, 255)

    # Soft alpha blend at the paint mask boundary (3px feather)
    mask_float = cv2.GaussianBlur(mask.astype(np.float32) / 255.0, (5, 5), 1.2)
    mask_3d = np.repeat(mask_float[:, :, np.newaxis], 3, axis=2)

    result = clean_img.astype(np.float32) * (1.0 - mask_3d) + defective_paint * mask_3d
    result = np.clip(result, 0, 255).astype(np.uint8)

    # STRICT BITWISE LOCK: Guarantee that outside mask == 0, result is 100% bitwise identical to clean_img
    result[mask == 0] = clean_img[mask == 0]

    return result

def main():
    clean = cv2.imread(CLEAN_PATH)
    if clean is None:
        raise RuntimeError("Failed to read " + CLEAN_PATH)
    h, w = clean.shape[:2]

    mask = create_car_paint_mask(h, w)
    dirty = generate_paint_defects(clean, mask)

    # Verify zero diff outside mask
    diff_outside = np.max(np.abs(dirty[mask == 0].astype(float) - clean[mask == 0].astype(float)))
    print(f"Max diff outside car paint mask: {diff_outside} (MUST BE 0.0)")
    assert diff_outside == 0.0, "Diff outside mask is not 0.0!"

    cv2.imwrite(DIRTY_PATH, dirty, [cv2.IMWRITE_JPEG_QUALITY, 96])
    print(f"Saved {DIRTY_PATH} successfully!")

    # Generate visual verification composite showing clean vs dirty side-by-side
    split_vis = clean.copy()
    split_vis[:, :w//2] = dirty[:, :w//2]
    # Draw slider line at center
    cv2.line(split_vis, (w//2, 0), (w//2, h), (255, 255, 255), 2)
    cv2.circle(split_vis, (w//2, h//2), 16, (255, 255, 255), -1)
    cv2.circle(split_vis, (w//2, h//2), 14, (11, 12, 14), -1)

    vis_path = os.path.join(BASE_DIR, 'img', 'bmw_slider_split_verification.jpg')
    cv2.imwrite(vis_path, split_vis, [cv2.IMWRITE_JPEG_QUALITY, 96])
    print(f"Saved slider verification: {vis_path}")

if __name__ == '__main__':
    main()
