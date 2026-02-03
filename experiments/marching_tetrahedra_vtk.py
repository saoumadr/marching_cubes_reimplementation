"""
marching_tetrahedra_vtk.py

Marching Tetrahedra surface extraction using VTK on CT-ORG segmentations.

Dataset (not included in repo):
https://www.cancerimagingarchive.net/collection/ct-org/

Requirements:
- nibabel
- numpy
- pyvista
- vtk
- matplotlib

Author: Adrien Saouma
"""

import time
import numpy as np
import nibabel as nib
import pyvista as pv
import vtk
from vtk.util.numpy_support import numpy_to_vtk
import matplotlib.pyplot as plt



# ------ Configuration ------

LABEL_PATH = "path/to/labels-1.nii.gz"   # CHANGE THIS
ISO_VALUE = 0.5
BACKGROUND_LABEL = 0

# ------Utilities -------

def load_nifti_labels(path):
    """Load NIfTI label volume."""
    img = nib.load(path)
    data = img.get_fdata().astype(np.uint8)
    spacing = img.header.get_zooms()
    return data, spacing


def numpy_mask_to_vtk_image(mask, spacing):
    """
    Convert a NumPy 3D mask to vtkImageData..
    """
    vtk_array = numpy_to_vtk(
        mask.ravel(order="F"),
        deep=True,
        array_type=vtk.VTK_UNSIGNED_CHAR
    )
    vtk_array.SetName("labels")

    image = vtk.vtkImageData()
    image.SetDimensions(mask.shape)
    image.SetSpacing(spacing)
    image.GetPointData().SetScalars(vtk_array)

    return image


def extract_surface_marching_tetrahedra(mask, spacing, iso_value=0.5):
    """
    Extract an isosurface using the Marching Tetrahedra.
    """
    image = numpy_mask_to_vtk_image(mask, spacing)
    tetra = vtk.vtkDataSetTriangleFilter()
    tetra.SetInputData(image)
    tetra.Update()
    contour = vtk.vtkContourFilter()
    contour.SetInputConnection(tetra.GetOutputPort())
    contour.SetValue(0, iso_value)
    contour.Update()

    return pv.wrap(contour.GetOutput())


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
        mesh = extract_surface_marching_tetrahedra(mask, spacing, ISO_VALUE)
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
    plotter.show(title="Marching Tetrahedra (VTK)")

    print("\n----- Summary -----")
    for lbl, tris in triangle_counts.items():
        print(f"Label {lbl}: {tris} triangles")
    print(f"Total triangles: {sum(triangle_counts.values())}")
    print(f"Total time: {total_time:.2f} s")


if __name__ == "__main__":
    main()
