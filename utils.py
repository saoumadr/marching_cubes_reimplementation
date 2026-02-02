import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def make_mesh_collection(verts, faces):
    if verts.size == 0 or faces.size == 0:
        return Poly3DCollection([], alpha=0.0)
    triangles = [verts[face] for face in faces]
    return Poly3DCollection(triangles, facecolor='pink', edgecolor='k', alpha=0.6)


def set_axes_equal(ax, verts):
    """Make axes have equal scale and a small padding."""
    if verts.size == 0:
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        ax.set_zlim(-1, 1)
        return

    xmin, xmax = verts[:, 0].min(), verts[:, 0].max()
    ymin, ymax = verts[:, 1].min(), verts[:, 1].max()
    zmin, zmax = verts[:, 2].min(), verts[:, 2].max()
    max_range = max(xmax - xmin, ymax - ymin, zmax - zmin)
    xmid, ymid, zmid = (xmax + xmin) / 2, (ymax + ymin) / 2, (zmax + zmin) / 2
    r = 0.6 * max_range
    ax.set_xlim(xmid - r, xmid + r)
    ax.set_ylim(ymid - r, ymid + r)
    ax.set_zlim(zmid - r, zmid + r)
    ax.set_box_aspect([1, 1, 1])
