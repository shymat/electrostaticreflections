import numpy as np
import pyvista as pv

# far too many modules and libraries here to work.. the premise is relatively simple so I shouldn't be relying on
# module upon module to fix my problems need to define a position vector within a grid; can represent the position
# vector as a matrix

# ah, before that. i'll defo need to establish a coordinate system to describe these transforms

# confirmed that i'm gonna try use sympy to visualise these things

# can use the lambdify to transfer these sympy arrays and vector classes into numbers to be used by other libaries
# i really only need a 2d coordinate system.. because of that working in matrices is going to be so much easier
# nevermind, i'm using numpy and planes. linear algebra is so wonderful (:wonder:)
# iteration program nesting is annoying but it makes sense.
# not deriving the point reflection eq. i'm just glad it works
# prob not even that hard tbh. u can work it out w some parameterisation
# plotting system i took from their published documentation site

theta = np.pi/(5/2)

# defining planes by point and normal vector
plane1 = {"point": np.array([0, 0, 0]), "normal": np.array([0, 0, 1])}
plane2 = {"point": np.array([0, 0, 0]), "normal": np.array([np.sin(theta), 0, np.cos(theta)])}
planes = [plane1, plane2]


# initial charge set up (charges and position)
charges = [{"pos": np.array([0, 0, 1]), "q": 1.0}]


# defining relection iteration

def reflect_point(p, plane):
    """Reflect point p across a plane defined by normal n and point x0."""
    n = plane["normal"] / np.linalg.norm(plane["normal"])
    x0 = plane["point"]
    return p - 2 * np.dot(p - x0, n) * n



def iterate_reflections(charges, planes, N=10):
    all_charges = charges.copy()
    for _ in range(N):
        new_charges = []
        for c in all_charges:
            for pl in planes:
                p_ref = reflect_point(c["pos"], pl)
                new_charges.append({"pos": p_ref, "q": -c["q"]})
        all_charges += new_charges
    return all_charges


def plot_system(charges, planes):
    plotter = pv.Plotter()

    for pl in planes:
        n = pl["normal"]
        origin = pl["point"]
        plane_mesh = pv.Plane(center=origin, direction=n, i_size=3, j_size=3)
        plotter.add_mesh(plane_mesh, opacity=0.3, color="lightblue")

    for c in charges:
        color = "red" if c["q"] > 0 else "blue"
        sphere = pv.Sphere(radius=0.05, center=c["pos"])
        plotter.add_mesh(sphere, color=color)

    plotter.show_axes()
    plotter.show()

all_charges = iterate_reflections(charges, planes, N=10)
plot_system(all_charges, planes)
