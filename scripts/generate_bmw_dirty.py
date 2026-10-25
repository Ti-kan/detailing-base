import cv2, numpy as np

CLEAN_PATH = '/Users/takanov/detailing-base/img/bmw-clean.jpg'
OUT_PATH = '/Users/takanov/.gemini/antigravity-cli/brain/0cba8e2f-79d3-4c29-a34a-d0fa28861163/verify_fix1_bmw_slider_natural.png'

clean_img = cv2.imread(CLEAN_PATH)
h, w, c = clean_img.shape

# 1. Build a smooth, soft-feathered mask for car paint
raw_mask = np.zeros((h, w), dtype=np.float32)

# Hood & front bumper paint zone (well inside perimeter, strictly above grille & splitter, below headlights)
hood_poly = np.array([
    [270, 500], [350, 455], [440, 430], [530, 435],
    [520, 475], [470, 485], [370, 490], [280, 520], [250, 540]
], np.int32)
cv2.fillPoly(raw_mask, [hood_poly], 1.0)

# Front fender & doors (above wheel arch, below side windows, strictly above rocker panel)
body_poly = np.array([
    [530, 440], [660, 430], [820, 455], [970, 480], [1020, 510],
    [1010, 570], [950, 600], [850, 615], [750, 620], [670, 620],
    [640, 560], [610, 510], [550, 490]
], np.int32)
cv2.fillPoly(raw_mask, [body_poly], 1.0)

# Exclude wheel areas with generous buffer (radius 95 and 75)
cv2.circle(raw_mask, (582, 645), 95, 0.0, -1)
cv2.circle(raw_mask, (1080, 580), 75, 0.0, -1)

# Exclude side glass and windshield completely
glass_poly = np.array([
    [460, 420], [560, 330], [860, 340], [1020, 440], [1000, 465], [660, 420]
], np.int32)
cv2.fillPoly(raw_mask, [glass_poly], 0.0)

# Exclude headlights & kidney grille
headlights_grille = np.array([
    [200, 470], [530, 460], [530, 610], [200, 610]
], np.int32)
# But keep the top of the hood! Notice hood_poly is above headlights/grille.
cv2.fillPoly(raw_mask, [headlights_grille], 0.0)
# Re-add hood top surface
hood_top = np.array([
    [290, 490], [360, 455], [450, 430], [540, 435],
    [520, 470], [420, 475], [340, 485], [280, 500]
], np.int32)
cv2.fillPoly(raw_mask, [hood_top], 1.0)

# Soft feather with sigma = 35px as requested
mask = cv2.GaussianBlur(raw_mask, (0, 0), sigmaX=35, sigmaY=35)
# Normalize to max 1.0
mask = np.clip(mask / (np.max(mask) if np.max(mask) > 0 else 1.0), 0.0, 1.0)

# 2. Simulate unpolished weathered paint inside the mask:
# Lift blacks +18, contrast * 0.82, saturation * 0.85
clean_float = clean_img.astype(np.float32)

# Convert to HSV to scale saturation
hsv = cv2.cvtColor(clean_img, cv2.COLOR_BGR2HSV).astype(np.float32)
hsv[:, :, 1] = hsv[:, :, 1] * 0.85 # desaturate paint slightly
desat_bgr = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)

# Lifted blacks +18, contrast * 0.82
oxidized = desat_bgr * 0.82 + 18.0
# Light scatter blur
blurred = cv2.GaussianBlur(oxidized, (5, 5), 1.2)
unpolished = oxidized * 0.60 + blurred * 0.40

# 3. Add ultra-fine subtle cobweb swirl marks (micro-holograms)
# ONLY around specular light reflection spots on the hood and fender
swirl_canvas = np.zeros((h, w), dtype=np.float32)

swirl_centers = [
    (380, 465), (440, 450), (490, 455), # hood hex light reflections
    (670, 475), (740, 485), (820, 505)  # front fender / door reflection
]

np.random.seed(1337)
for cx, cy in swirl_centers:
    # Concentric micro-scratches
    for r in range(12, 75, 4):
        # Draw 2-3 broken arcs per radius
        for _ in range(np.random.randint(1, 3)):
            start_ang = np.random.randint(0, 360)
            arc_len = np.random.randint(25, 75)
            temp = np.zeros((h, w), dtype=np.uint8)
            cv2.ellipse(temp, (cx, cy), (r, int(r * 0.7)), 12, start_ang, start_ang + arc_len, 255, 1)
            # Add fine swirl with low opacity <= 0.18 (values 15 to 40 out of 255)
            swirl_canvas += (temp.astype(np.float32) / 255.0) * np.random.uniform(16.0, 38.0)

# Subtle directional motion blur on swirls to simulate optical glare
kernel = np.zeros((3, 3))
kernel[0, 2] = 0.3
kernel[1, 1] = 0.4
kernel[2, 0] = 0.3
swirl_canvas = cv2.filter2D(swirl_canvas, -1, kernel)

# Swirls only appear where mask is active and on darker paint (not blown out highlights)
swirl_layer = swirl_canvas[:, :, np.newaxis]

# Combine onto unpolished paint
defective_paint = unpolished + swirl_layer
defective_paint = np.clip(defective_paint, 0, 255)

# Alpha blend using 35px soft feather mask
mask_3d = mask[:, :, np.newaxis]
result = clean_float * (1.0 - mask_3d) + defective_paint * mask_3d
result = np.clip(result, 0, 255).astype(np.uint8)

cv2.imwrite('/Users/takanov/detailing-base/img/bmw-dirty.jpg', result, [cv2.IMWRITE_JPEG_QUALITY, 93])
cv2.imwrite(OUT_PATH, result)
print('Successfully generated natural bmw-dirty.jpg!')
