import cv2
import numpy as np
import os

img_path = "/Users/lanpixiao/.gemini/antigravity-ide/brain/11d6afaa-b414-42ee-b2df-cd1eb213b17e/.user_uploaded/media_1787651472471.jpg"
im = cv2.imread(img_path)
h_total, w_total = im.shape[:2]
os.makedirs("perfect_icons", exist_ok=True)

# Precise coordinates strictly avoiding surrounding lines/borders:
search_regions = {
    # Section 1
    "clipboard": (92, 146, 30, 78),
    "robot_face": (52, 112, 556, 606),
    "unsafe_triangle": (75, 102, 715, 736),  # exclude left border line
    "safe_shield": (185, 212, 715, 736),     # exclude left border line (y was 145, safe shield is at y ~185-212)
    
    # Section 2
    "target_task": (254, 292, 44, 82),
    "tvd_agent_bulb_robot": (324, 408, 25, 140),
    "data_doc": (300, 328, 254, 280),
    "shield_criteria": (490, 514, 256, 270),
    
    # Section 3 (Failure Modes 1~6)
    "fm1_scale": (256, 305, 642, 712),
    "fm2_cross": (320, 368, 642, 712),
    "fm3_check": (380, 428, 642, 712),
    "fm4_gauge": (442, 486, 642, 712),
    "fm5_speaker": (502, 552, 642, 712),
    "fm6_brain": (568, 620, 642, 712),
    
    # Bottom Takeaways
    "bottom_bulb": (672, 738, 34, 73),
    "bottom_rocket": (672, 738, 347, 398),
    "bottom_target": (672, 738, 670, 725),
}

for name, (ymin, ymax, xmin, xmax) in search_regions.items():
    patch = im[ymin:ymax, xmin:xmax].copy()
    patch = cv2.cvtColor(patch, cv2.COLOR_BGR2BGRA)
    ph, pw = patch.shape[:2]
    
    # Transparency
    for y in range(ph):
        for x in range(pw):
            b, g, r, a = patch[y, x]
            if b > 230 and g > 230 and r > 230:
                patch[y, x] = [0, 0, 0, 0]
            elif b > 215 and g > 215 and r > 215 and abs(int(b)-int(g)) < 8 and abs(int(g)-int(r)) < 8:
                patch[y, x] = [0, 0, 0, 0]
                
    # Auto tight bounding box
    alpha = patch[:, :, 3]
    coords_nz = cv2.findNonZero(alpha)
    if coords_nz is not None:
        x, y, w, h = cv2.boundingRect(coords_nz)
        x1 = max(0, x - 1)
        y1 = max(0, y - 1)
        x2 = min(pw, x + w + 1)
        y2 = min(ph, y + h + 1)
        cropped_patch = patch[y1:y2, x1:x2]
    else:
        cropped_patch = patch

    cv2.imwrite(f"perfect_icons/{name}.png", cropped_patch)
    print(f"Extracted {name}: {cropped_patch.shape[1]}x{cropped_patch.shape[0]}")

print("All icons successfully updated!")
