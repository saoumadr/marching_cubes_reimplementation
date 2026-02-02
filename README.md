# 3D Surface Reconstruction with Marching Cubes

This repository contains a **custom Python implementation of the Marching Cubes (MC)** algorithm for 3D surface reconstruction from volumetric data.  
The project is primarily **educational**, focusing on understanding the algorithmic foundations, limitations, and modern variants of Marching Cubes.

The repository includes:

- Synthetic volumetric datasets (sphere, torus, ellipsoid, cube, cone)
- Quantitative evaluation of reconstructed surfaces using standard distance metrics
- Interactive 3D visualization with adjustable isolevels
- Experimental comparison with modern implementations on real CT volumes
- Discussion of algorithmic limitations and ambiguity-resolving variants

---

## Table of Contents

- [Installation](#installation)
- [Dataset](#dataset)
- [Key Features](#key-features)
- [Evaluation Metrics](#evaluation-metrics)
- [Results](#results)
- [Limitations](#limitations)
- [Modern Variants](#modern-variants)
- [Usage](#usage)

---

## Installation

Clone the repository and install the core dependencies:

```bash
git clone <repository_url>
cd <repository_folder>
pip install -r requirements.txt
```

Additional dependencies required to run the experimental scripts are listed in:
```bash
pip install -r requirements-experiments.txt
```
---

## Dataset

This project supports both **synthetic datasets** and **real medical imaging data**.

### Synthetic datasets

The following synthetic shapes are generated as 3D scalar fields on uniform grids:

- Sphere
- Torus
- Ellipsoid
- Cube
- Cone

For these shapes, **analytical ground-truth surfaces** are available and sampled, enabling quantitative evaluation of reconstruction accuracy.

### CT volumes

The following anatomical structures are used in experimental benchmarks:

- Bladder
- Liver
- Lungs
- Kidneys
- Skeleton

Real CT volumes are processed **only in the experimental scripts**, using optimized library implementations.  
The naive Marching Cubes implementation provided in the core project is computationally too slow to reconstruct full-resolution CT volumes.

Details and download instructions for the CT dataset are provided in `datasets/README.md`.

---

## Key Features

- Custom Python implementation of **classic Marching Cubes** for educational purposes  
- NumPy-based voxel representation  
- Interactive 3D visualization with **real-time isolevel adjustment**  
- Clear separation between:
  - Core algorithm implementation
  - Experimental comparison with modern methods

---

## Evaluation Metrics

Two standard surface distance metrics are used to assess reconstruction accuracy on synthetic datasets:

- **Hausdorff Distance**  
  Maximum distance from any point on the reconstructed surface to the closest point on the ground-truth surface.

- **Average Symmetric Surface Distance (ASSD)**  
  Average of distances from reconstructed surface points to the ground-truth surface and vice versa.

These metrics provide complementary insights into worst-case and average geometric errors.

---

## Results

Detailed results, visualizations, and quantitative evaluations are provided in the accompanying project report.

---

## Limitations

The current custom implementation has several known limitations:

- **Vertex duplication**: Vertices are not shared between adjacent triangles, increasing memory usage.  
- **Performance**: Python-level iteration over the voxel grid limits scalability to large volumes.  
- **Topological ambiguities**: The original Marching Cubes algorithm may generate holes or non-manifold surfaces.  
- **Manual isolevel selection**: No automatic isovalue optimization or gradient-based refinement is implemented.  
- **Uniform grids only**: Non-uniform voxel spacing is not fully supported in the custom implementation.  

These limitations motivate the use of **modern variants** in the experimental section.

---

## Modern Variants

Several improvements and alternatives to the original Marching Cubes algorithm are explored experimentally:

- **Marching Cubes 33 (MC33)**: Resolves topological ambiguities by expanding the number of cube configurations.  
- **Marching Tetrahedra**: Avoids ambiguous cases by decomposing cubes into tetrahedra.  
- **Optimized library implementations**: Used for benchmarking on real CT volumes.  
- **Surface smoothing and post-processing**: Improve mesh quality and visual appearance.  

The implementations of these variants are available in the `experiments/` directory.

---

## Usage

Run the main script to reconstruct and visualize surfaces from synthetic datasets:

```bash
python main.py
```

Experimental scripts for CT volumes and algorithm comparison can be found in the experiments/ directory.
