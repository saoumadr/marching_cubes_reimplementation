import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Patch

from utils import make_mesh_collection, set_axes_equal
from metrics import compute_hausdorff_distance
from marching_cubes import marching_cubes


def run_interactive_viewer(
    volume,
    verts,
    faces,
    gt_points,
    origin,
    spacing,
    unit_to_mm,
    isolevel_init,
    dataset_name,
    n
):
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    mesh = make_mesh_collection(verts, faces)
    ax.add_collection3d(mesh)
    set_axes_equal(ax, verts)

    proxy = Patch(color='pink', label=f'Marching Cubes ({dataset_name})')
    ax.legend(handles=[proxy])
    ax.set_title(
        f"Hausdorff = {compute_hausdorff_distance(verts, gt_points) * unit_to_mm:.3f} mm  "
        f"with grid resolution (n={n})",
        fontsize=10
    )

    ax_iso = plt.axes([0.2, 0.01, 0.6, 0.03], facecolor='lightgoldenrodyellow')
    slider_iso = Slider(
        ax_iso,
        'Isolevel',
        float(volume.min()),
        float(volume.max()),
        valinit=float(isolevel_init),
        valstep=(volume.max() - volume.min()) / 1000.0
    )

    def update(val):
        isolevel = slider_iso.val
        verts_new, faces_new = marching_cubes(
            volume,
            isolevel,
            origin=origin,
            spacing=spacing
        )

        if verts_new.size == 0 or faces_new.size == 0:
            mesh.set_verts([])
            mesh.set_alpha(0.0)
        else:
            triangles_new = [verts_new[face] for face in faces_new]
            mesh.set_verts(triangles_new)
            mesh.set_alpha(0.6)

        set_axes_equal(ax, verts_new)

        try:
            dH_units = compute_hausdorff_distance(verts_new, gt_points)
            dH_mm = dH_units * unit_to_mm
            ax.set_title(
                f"Hausdorff = {dH_mm:.3f} mm  (iso={isolevel:.3f})",
                fontsize=10
            )
        except Exception as e:
            print("Could not compute Hausdorff:", e)

        fig.canvas.draw_idle()

    slider_iso.on_changed(update)
    plt.show()
