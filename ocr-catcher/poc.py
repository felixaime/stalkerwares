from PIL import Image
import pytesseract
import itertools
import json
import sys
import cv2

# Load icons paths.
assets = json.loads(open("assets.json", "r").read())
icons = list(itertools.chain.from_iterable([a["icons"] for a in assets]))
names = [{"app": a["app"], "names": a["names"]} for a in assets]

# Icon recognition part.

# Load source image
image_src = cv2.imread(sys.argv[1])

# Apply some blur and threshold.
grey = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(grey, (5, 5))
blur2 = cv2.blur(grey, (5, 5))
tresh = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY)[1]

# Find contours.
contours, hierarchy = cv2.findContours(tresh, 1, 2)

img_icons = []

# Extracting icons.
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    cropped = blur2[y:y+h, x:x+w]
    if 0.9 <= (w/h) <= 1.1:
        if h > 50 and w > 50:
            img_icons.append(cropped)

for icon_path in icons:
    icon = cv2.imread(icon_path, 0)
    icon = cv2.blur(icon, (5, 5))
    orb = cv2.AKAZE_create()
    kp1, dest1 = orb.detectAndCompute(icon, None)

    for i in img_icons:
        kp2, dest2 = orb.detectAndCompute(i, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = bf.knnMatch(dest1, dest2, k=2)
        try:
            good = []
            for m, n in matches:
                if m.distance < 0.72*n.distance:
                    good.append([m])

            if len(good) > 3:
                print(icon_path.split("/")[1], len(good))
                img = cv2.drawMatchesKnn(
                    icon, kp1, i, kp2, good[:1], None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                cv2.imshow(icon_path.split("/")[1], img)
                cv2.waitKey(500)
        except:
            continue

# OCR part
text = pytesseract.image_to_string(Image.open(sys.argv[1]))

for line in text.splitlines():
    for app in names:
        for name in app["names"]:
            if name != "Accessibility":
                if name == line.strip():
                    print(app)
