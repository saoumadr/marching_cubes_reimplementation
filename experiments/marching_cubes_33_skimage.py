"""
marching_cubes_33_skimage.py

Marching Cubes 33 (Lewiner) surface extraction using scikit-image on CT-ORG segmentations.

Dataset (not included in repo):
https://www.cancerimagingarchive.net/collection/ct-org/

Requirements:
- nibabel
- numpy
- scikit-image
- pyvista
- matplotlib

Author: Adrien Saouma
"""

import time
import numpy as np
import nibabel as nib
import pyvista as pv
import matplotlib.pyplot as plt
from skimage import measure


# ------- Configuration ------

LABEL_PATH = "path/to/labels-1.nii.gz"   # CHANGE THIS
ISO_VALUE = 0.5
BACKGROUND_LABEL = 0


# ------- Utilities -------

def load_nifti_labels(path):
    """Load NIfTI label volume."""
    img = nib.load(path)
    data = img.get_fdata().astype(np.uint8)
    spacing = img.header.get_zooms()
    return data, spacing


def extract_surface_mc33(mask, spacing, iso_value=0.5):
    """
    Extract surface using Marching Cubes 33 (Lewiner).
    """
    verts, faces, normals, _ = measure.marching_cubes(
        mask,
        level=iso_value,
        spacing=spacing,
        method="lewiner"
    )

    
    faces_pv = np.hstack(
        (np.full((faces.shape[0], 1), 3), faces)
    ).astype(np.int32)

    return pv.PolyData(verts, faces_pv)


def main():

    label_data, spacing = load_nifti_labels(LABEL_PATH)
    labels = np.unique(label_data)

    print("Labels found:", labels)
    print("Voxel spacing:", spacing)

    plotter = pv.Plotter()
    colormap = plt.colormaps.get_cmap("tab10")

    triangle_counts = {}
    start_total = time.time()

    for i, lbl in enumerate(labels):

        if lbl == BACKGROUND_LABEL:
            print("\nSkipping background label")
            continue

        print(f"\nProcessing label {lbl}...")

        mask = (label_data == lbl).astype(np.uint8)
        if mask.sum() == 0:
            print("  No voxels found, skipping.")
            continue

        t0 = time.time()
        mesh = extract_surface_mc33(mask, spacing, ISO_VALUE)
        t1 = time.time()

        if mesh.n_cells == 0:
            print("  No surface extracted.")
            continue

        triangle_counts[lbl] = mesh.n_cells

        print(f"  Extraction time: {t1 - t0:.2f} s")
        print(f"  Triangles: {mesh.n_cells}")

        color = colormap(i % 10)[:3]
        plotter.add_mesh(mesh, color=color, opacity=0.6)

    total_time = time.time() - start_total

    plotter.add_axes()
    plotter.show(title="Marching Cubes 33 (Lewiner)")

    print("\n ------- Summary ------")
    for lbl, tris in triangle_counts.items():
        print(f"Label {lbl}: {tris} triangles")
    print(f"Total triangles: {sum(triangle_counts.values())}")
    print(f"Total time: {total_time:.2f} s")


if __name__ == "__main__":
    main()
