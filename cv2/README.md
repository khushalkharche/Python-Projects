# 🐘 Ganpati Bappa Sketch Animation

A cinematic, frame-by-frame sketch animation of Lord Ganesha built entirely from scratch using **Python**, **OpenCV**, and **Pygame**.

This project bridges computer vision and 2D rendering. It processes a static image using edge detection algorithms, calculates the contours, and then dynamically draws the sketch on a full-screen canvas with synchronized audio and alpha-blending effects.

## ✨ Features

- **Computer Vision Edge Detection:** Uses OpenCV (Gaussian Blur and Canny Edge Detection) to mathematically map out the contours of the original source image.
- **Dynamic Vector Rendering:** Translates mathematical contours into coordinate points, drawing thousands of golden line segments frame-by-frame via Pygame.
- **Auto-Centering & Scaling:** Dynamically calculates screen bounds to perfectly center the final drawing on any resolution monitor in `FULLSCREEN` mode.
- **Alpha-Blended Text Reveal:** Uses a snapshot rendering method to smoothly fade in text without smearing the previously drawn frames.
- **Cinematic Sequencing:** Features background music (`pygame.mixer`), audio fade-out, and a smooth screen fade-to-black wrap-up designed specifically for clean video recording.

## 🛠️ Prerequisites

You will need Python 3 installed on your system. You also need to install the required libraries:

```bash
pip install pygame opencv-python numpy
```
