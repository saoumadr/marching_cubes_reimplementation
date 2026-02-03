# 3D Surface Reconstruction with Marching Cubes

This repository contains a **Python implementation of the Marching Cubes (MC)** algorithm for 3D surface reconstruction from volumetric data.  
The project is primarily **educational**, focusing on understanding the algorithmic foundations, limitations, and modern variants of Marching Cubes.

The repository includes:

- Synthetic volumetric datasets (sphere, torus, ellipsoid, cube, cone)
- Evaluation of reconstructed surfaces using ASSD and the Hausdorff distance
- Interactive 3D visualization with adjustable isolevels
- Experimental comparison with modern implementations on real CT scans
- Discussion of limitations and variants of the algorithm

---

## Table of Contents

- [Installation](#installation)
- [Dataset](#dataset)
- [Results](#results)
- [Limitations](#limitations)
- [Modern Variants](#modern-variants)
- [Usage](#usage)

---

## Installation

Clone the repository, create the environment and install the core dependencies:

```bash
git clone <repository_url>
cd <repository_folder>
conda create -n envname python=3.11
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

The dataset used can be found online [here](https://www.cancerimagingarchive.net/collection/ct-org/)

The folowing organs are presented in the results:
- Bladder
- Liver
- Lungs
- Kidneys
- Skeleton

Real CT volumes are used **only in the experimental scripts** with optimized library implementations.  
The naive Marching Cubes implementation provided in the core project is computationally too slow to reconstruct full-resolution CT volumes.

---


## Results

Detailed results, visualizations, and quantitative evaluations are provided in the project [report](report/report.pdf).

---

## Limitations

The current custom implementation has several known limitations:

- **Vertex duplication**: Vertices are not shared between adjacent triangles, increasing memory usage.  
- **Performance**: Complexity $O(8n^3)$ makes it impossible to use it on real imaging data without further optimizations. 
- **Topological ambiguities**: The original Marching Cubes algorithm may generate holes or non-manifold surfaces.  

These limitations motivate the use of **modern variants** and **libraries** in the [experimental section](experiments/).

---

## Variants

Alternatives to the presented python Marching Cubes algorithm are explored experimentally:

- **Marching Cubes 33 (MC33)**: Solves topological ambiguities by expanding the number of cube configurations.  
- **Marching Tetrahedra**: Solves topological ambiguities by decomposing cubes into tetrahedra.  
- **Optimized Marching Cubes using Scikit-image**: Used for benchmarking on real CT volumes.
  
The implementations of these variants are available in the [experiments](experiments/) directory.

---

## Usage

Run the main script to reconstruct and visualize surfaces from synthetic datasets:

```bash
python main.py
```
