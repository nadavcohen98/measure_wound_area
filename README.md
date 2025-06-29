# measure_wound_area

# Wound Mask Cleanup & Area Measurement
Robust, reproducible post-processing for scratch-wound assays
============================================================

> **Objective** Automatically clean binary wound masks, extract the largest wound
> region, and report its area—ready for high-throughput cell-migration or
> wound-healing studies.

---

## Table of Contents
1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Command-Line Usage](#command-line-usage)
5. [Python API](#python-api)
6. [Repository Layout](#repository-layout)
7. [Citation](#citation)
8. [License](#license)

---

## Overview
Quantifying cell migration in scratch-wound assays hinges on accurate wound
segmentation. Raw binary masks produced by classical thresholding or
deep-learning models often contain **salt-and-pepper noise** and small holes that
bias area measurements.  
This toolkit applies **elliptical morphological opening and closing** to:

1. **Remove isolated noise pixels** that could be mistaken for tissue or
   background.  
2. **Fill micro-holes** within the wound so the resulting mask is contiguous.  
3. **Identify the largest dark region**—the wound—and compute its area
   in pixels² (and physical units if pixel size is provided).

Everything is implemented in pure Python with **OpenCV ≥ 4.5** and **NumPy**,
so it runs on any workstation without GPU dependencies.

---

## Key Features
| Feature | Benefit |
|---------|---------|
| **Elliptical kernels** | Preserve the naturally rounded boundaries of biological structures better than square kernels. |
| **Opening → Closing pipeline** | Cleans specks *and* plugs holes in a single pass. |
| **`largest_wound_area()` helper** | Returns the area (px² / mm²) of the dominant wound region—ideal for batch analytics. |
| **CLI & library modes** | Use from the terminal for large datasets *or* import functions in Jupyter. |
| **Lightweight dependencies** | Only `opencv-python` and `numpy`. Installs in seconds. |
| **Modular design** | Drop‐in replacement component for any wound-segmentation workflow. |

---

## Quick Start
```bash
# 1. Clone and install
git clone https://github.com/<user>/wound-mask-cleanup.git
cd wound-mask-cleanup
pip install -r requirements.txt   # numpy, opencv-python

# 2. Run on a single image
python wound_mask_cleanup.py \
    --input  samples/raw_mask.png \
    --output results/clean_mask.png

# 3. Inspect results
feh results/clean_mask.png        # or any image viewer
