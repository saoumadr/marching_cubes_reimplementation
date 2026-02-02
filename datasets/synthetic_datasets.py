import numpy as np

def choose_data_set(DATASET, n, n_samples=5000):
    """
    Generate the 3d grid and ground truth surface samples for a given shape.
    DATASET: string, one of "sphere", "torus", "ellipsoid", "cube", "cone"
    n: int, grid resolution (n x n x n)
    n_samples: int, number of ground truth surface samples to generate
    
    Returns:
        volume: 3D numpy array of scalar field values
        isolevel_init: float, isosurface level
        gt_points: (N, 3) array of ground truth surface samples (for evaluation)
    """
    if DATASET == "sphere":
        x, y, z = np.mgrid[-1:1:n*1j, -1:1:n*1j, -1:1:n*1j]
        volume = x**2 + y**2 + z**2
        isolevel_init = 0.5   # radius^2

        phi = np.random.uniform(0, np.pi, n_samples)
        theta = np.random.uniform(0, 2*np.pi, n_samples)
        r = np.sqrt(isolevel_init)
        x_gt = r * np.sin(phi) * np.cos(theta)
        y_gt = r * np.sin(phi) * np.sin(theta)
        z_gt = r * np.cos(phi)
        gt_points = np.stack([x_gt, y_gt, z_gt], axis=1)


    elif DATASET == "torus":
        R, r = 0.6, 0.3
        x, y, z = np.mgrid[-1:1:n*1j,
                           -1:1:n*1j,
                           -1:1:n*1j]
        volume = (np.sqrt(x**2 + y**2) - R)**2 + z**2 - r**2
        isolevel_init = 0.0

        u = np.random.uniform(0, 2*np.pi, n_samples)
        v = np.random.uniform(0, 2*np.pi, n_samples)
        x_gt = (R + r * np.cos(v)) * np.cos(u)
        y_gt = (R + r * np.cos(v)) * np.sin(u)
        z_gt = r * np.sin(v)
        gt_points = np.stack([x_gt, y_gt, z_gt], axis=1)

    elif DATASET == "ellipsoid":
        a, b, c = 1.0, 0.6, 0.4
        x, y, z = np.mgrid[-1:1:n*1j,
                           -1:1:n*1j,
                           -1:1:n*1j]
        volume = (x/a)**2 + (y/b)**2 + (z/c)**2
        isolevel_init = 1.0

        # --- Ground truth points ---
        phi = np.random.uniform(0, np.pi, n_samples)
        theta = np.random.uniform(0, 2*np.pi, n_samples)
        x_gt = a * np.sin(phi) * np.cos(theta)
        y_gt = b * np.sin(phi) * np.sin(theta)
        z_gt = c * np.cos(phi)
        gt_points = np.stack([x_gt, y_gt, z_gt], axis=1)


    elif DATASET == "cube":
        side = 1.0 # length of cube side
        x, y, z = np.mgrid[-1:1:n*1j,
                           -1:1:n*1j,
                           -1:1:n*1j]
        
        volume = np.maximum.reduce([np.abs(x), np.abs(y), np.abs(z)])
        isolevel_init = side / 2.0

        faces = np.random.randint(0, 3, n_samples)
        coords = np.random.uniform(-side/2, side/2, (n_samples, 3))
        for i in range(n_samples):
            coords[i, faces[i]] = side/2 * np.random.choice([-1, 1])
        gt_points = coords


    elif DATASET == "cone":
        R, h = 0.6, 1.2
        x, y, z = np.mgrid[-1:1:n*1j, -1:1:n*1j, -1:1:n*1j]
        volume = np.sqrt(x**2 + y**2) - (R * (h/2 - z) / h)
        isolevel_init = 0.0
        
        u = np.random.uniform(0, 2*np.pi, n_samples)
        t = np.random.uniform(0, 1, n_samples)
        z_gt = h/2 - t * h
        r_gt = t * R
        x_gt = r_gt * np.cos(u)
        y_gt = r_gt * np.sin(u)
        gt_points = np.stack([x_gt, y_gt, z_gt], axis=1)
    
    else:
        raise ValueError("Unknown DATASET")

    return volume, isolevel_init, gt_points
