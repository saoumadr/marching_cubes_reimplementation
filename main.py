import numpy as np
import time

from datasets.synthetic_datasets import choose_data_set
from metrics import compute_hausdorff_distance, compute_assd
from marching_cubes import marching_cubes
from visualization import run_interactive_viewer


# -----------DATASET------------
DATASET = "torus"   # "sphere", "torus", "ellipsoid", "cube", "cone"
n = 2**4            # grid resolution

volume, isolevel_init, gt_points = choose_data_set(DATASET, n)


# -----------SCALING------------
physical_size_mm = 100.0
grid_min, grid_max = -1.0, 1.0
origin = np.array([grid_min, grid_min, grid_min], dtype=float)
spacing = np.array([(grid_max - grid_min) / (n - 1)] * 3, dtype=float)

unit_to_mm = physical_size_mm / (grid_max - grid_min)
voxel_size_mm = spacing[0] * unit_to_mm


# -----------RUNNING AND EVALUATION------------
start = time.time()
verts, faces = marching_cubes(volume, isolevel_init, origin=origin, spacing=spacing)
end = time.time()
full_time = end - start
print(f"Time for resolution {n} is: {full_time:.3f} seconds")

hausdorff_distance = compute_hausdorff_distance(verts, gt_points)
hausdorff_mm = hausdorff_distance * unit_to_mm

num_triangles = faces.shape[0]
print(f"Number of triangles in reconstructed mesh: {num_triangles}")

print(f"Hausdorff Distance between reconstructed surface and ground truth:")
print(f"  {hausdorff_distance:.6f} (model units)  =  {hausdorff_mm:.3f} mm with grid resolution (n={n})")

assd_value = compute_assd(verts, gt_points)
print(f"Average Symmetric Surface Distance (ASSD): {assd_value:.6f} (model units)  =  {assd_value * unit_to_mm:.3f} mm")


# -----------VISUALIZATION------------
run_interactive_viewer(
    volume=volume,
    verts=verts,
    faces=faces,
    gt_points=gt_points,
    origin=origin,
    spacing=spacing,
    unit_to_mm=unit_to_mm,
    isolevel_init=isolevel_init,
    dataset_name=DATASET,
    n=n
)
