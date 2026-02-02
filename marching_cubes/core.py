import numpy as np
from .tables import EDGE_TABLE, TRIANGLE_TABLE 

def interpolate_vertex(p1, p2, valp1, valp2, isolevel):
    eps = 1e-8
    if abs(isolevel - valp1) < eps:
        return p1.copy()
    if abs(isolevel - valp2) < eps:
        return p2.copy()
    if abs(valp1 - valp2) < eps:
        return p1.copy()
    mu = (isolevel - valp1) / (valp2 - valp1)
    return p1 + mu * (p2 - p1)

def marching_cubes(volume, isolevel=0.5, origin=None, spacing=None):
    """
    volume: 3D numpy array of scalar values
    isolevel: threshold
    origin: 3-array giving coordinates of voxel (0,0,0) corner in world space
    spacing: 3-array giving physical spacing between consecutive grid points (dx, dy, dz)
    Returns:
      vertices: (M,3) array in world coordinates
      faces: (K,3) int array (indices into vertices)
    """
    vertices = []
    faces = []
    nx, ny, nz = volume.shape

    if origin is None:
        origin = np.array([0.0, 0.0, 0.0], dtype=float)
    else:
        origin = np.array(origin, dtype=float)

    if spacing is None:
        spacing = np.array([1.0, 1.0, 1.0], dtype=float)
    else:
        spacing = np.array(spacing, dtype=float)

    corner_idxs = [(0,0,0),(1,0,0),(1,1,0),(0,1,0),(0,0,1),(1,0,1),(1,1,1),(0,1,1)]
    EDGE_CONNECTIONS = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    #Iteration over the whole grid (O(8n^3))
    for x in range(nx - 1):
        for y in range(ny - 1):
            for z in range(nz - 1):
                cube = np.zeros(8)
                points = []
                for i in range(8):
                    dx, dy, dz = corner_idxs[i]
                    cube[i] = volume[x+dx, y+dy, z+dz]
                    world_pt = origin + spacing * np.array([x+dx, y+dy, z+dz], dtype=float)
                    points.append(world_pt)

                # Convention: corner inside if value < isolevel OR outside if >= 
                cube_index = 0
                for i in range(8):
                    if cube[i] < isolevel:
                        cube_index |= 1 << i

                if EDGE_TABLE[cube_index] == 0:
                    continue

                vert_list = [None]*12
                for i_edge in range(12):
                    if EDGE_TABLE[cube_index] & (1 << i_edge):
                        p1_idx, p2_idx = EDGE_CONNECTIONS[i_edge]
                        p1 = points[p1_idx]
                        p2 = points[p2_idx]
                        valp1 = cube[p1_idx]
                        valp2 = cube[p2_idx]
                        vert_list[i_edge] = interpolate_vertex(p1, p2, valp1, valp2, isolevel)

                tri = TRIANGLE_TABLE[cube_index]
                for i in range(0, len(tri), 3):
                    if tri[i] == -1:
                        break
                    v0 = vert_list[tri[i]]
                    v1 = vert_list[tri[i+1]]
                    v2 = vert_list[tri[i+2]]
                    # If any of them is None skip (safety)
                    if v0 is None or v1 is None or v2 is None:
                        continue
                    idx0, idx1, idx2 = len(vertices), len(vertices)+1, len(vertices)+2
                    vertices.extend([v0, v1, v2])
                    faces.append([idx0, idx1, idx2])

    return np.array(vertices, dtype=float), np.array(faces, dtype=int)
