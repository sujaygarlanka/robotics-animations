from manimlib import *
from klampt.math import so3
import copy


manim_config.camera.background_color = WHITE

class Cube(Group):
    # https://sketchfab.com/3d-models/15-cases-marching-cubes-representation-78927bfd96694fccbc064bb5fe820f3d
    # https://www.cs.carleton.edu/cs_comps/0405/shape/marching_cubes.html
    #                 v7_______e6_____________v6
    #                  /|                    /|
    #                 / |                   / |
    #              e7/  |                e5/  |
    #               /___|______e4_________/   |
    #            v4|    |                 |v5 |e10
    #              |    |                 |   |
    #              |    |e11              |e9 |
    #            e8|    |                 |   |
    #              |    |_________________|___|
    #              |   / v3      e2       |   /v2
    #              |  /                   |  /
    #              | /e3                  | /e1
    #              |/_____________________|/
    #              v0         e0          v1

    CUBE_VERTICES = np.array([
        [-0.5, -0.5, -0.5],  # 0
        [ 0.5, -0.5, -0.5],  # 1
        [ 0.5,  0.5, -0.5],  # 2
        [-0.5,  0.5, -0.5],  # 3
        [-0.5, -0.5,  0.5],  # 4
        [ 0.5, -0.5,  0.5],  # 5
        [ 0.5,  0.5,  0.5],  # 6
        [-0.5,  0.5,  0.5]   # 7
    ])

    # Edge → (start corner index, end corner index)
    CUBE_EDGES = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # bottom face
        (4, 5), (5, 6), (6, 7), (7, 4),  # top face
        (0, 4), (1, 5), (2, 6), (3, 7)   # verticals
    ]

    def __init__(self, scene, scale=1.0, vertex_idx=[], triangles=[]):
        super().__init__()
        self.scene = scene
        self.edges = []
        self.vertices = []
        self.vertex_idx = []
        self.scale_val = scale
        self.rotation_matrix = so3.identity()

        self.triangles = []
        self.create_cube()
        self.add_vertices(vertex_idx)
        self.add_triangles(triangles)

    def create_cube(self):
        # Draw cube edges
        for i, j in Cube.CUBE_EDGES:
            edge = Line(
                Cube.CUBE_VERTICES[i] * self.scale_val,
                Cube.CUBE_VERTICES[j] * self.scale_val,
                color=BLACK,
                stroke_width=1.0 * self.scale_val,
            )
            self.edges.append(edge)
            self.add(edge)

    def clear_vertices(self, animation=False):
        # Clear previous vertices
        if animation:
            vertices = self.vertices
            self.vertices = []
            self.vertex_idx = []
            return vertices
        else:
            for dot in self.vertices:
                self.remove(dot)
            self.vertices = []
            self.vertex_idx = []

    def add_vertices(self, vertex_idx, animation=False):
        self.vertex_idx = vertex_idx

        # Visualize corners
        for idx, pos in enumerate(Cube.CUBE_VERTICES):
            o = 1.0 if idx in vertex_idx else 0.0
            r = 0.05 * self.scale_val
            dot = Sphere(radius=r, opacity=o, color="#62AFE0")
            # Get the rotation frame of the group
            dot.move_to(np.array(so3.apply(self.rotation_matrix, pos)) * self.scale_val)
            self.vertices.append(dot)
            if not animation:
                self.add(dot)

        return self.vertices

    def add_triangles(self, triangles):
        for t in triangles:
            triangle_points = []
            for edge in t:
                e = Cube.CUBE_EDGES[edge]
                v1 = Cube.CUBE_VERTICES[e[0]] * self.scale_val
                v2 = Cube.CUBE_VERTICES[e[1]] * self.scale_val
                triangle_points.append((v1 + v2)/2.0)
            triangle = Polygon(triangle_points[0], triangle_points[1], triangle_points[2])
            triangle.set_fill(YELLOW, opacity=1.0)
            triangle.set_stroke(BLACK, width=1 * self.scale_val)
            self.triangles.append(triangle)
            self.add(triangle)

    def get_vertex_locations(self):
        return Cube.CUBE_VERTICES[self.vertex_idx]
    
    def rotate(
        self,
        angle,
        axis = OUT,
        **kwargs
    ):
        super().rotate(angle, axis=axis, **kwargs)
        R = so3.rotation(axis, angle)
        self.rotation_matrix = so3.mul(R, self.rotation_matrix)

    def scale(self, scale):
        super().scale(scale)
        self.scale_val *= scale
        for edge in self.edges:
            edge.set_stroke(BLACK, width=1.0 * self.scale_val)
        for triangle in self.triangles:
            triangle.set_stroke(BLACK, width=1)
        
class TorusPlot(InteractiveScene):
    def construct(self):
        # Animation script

        # Show 256 combos
        # Show 15 base cases rotating around
        # Minimize to the top banner
        # Show a few cubes intersecting
        # - Find the cube in the table that shows in the top banner
        # - Show the cube rotating
        # - Show the cube moving to the location of the intersection
        # Fast forward to the end without the intersection animations
        # Fade out the sphere and the strokes of the cubes

        # Set up camera orientation
        self.camera.frame.reorient(phi_degrees=90, theta_degrees=0)

        # Initial orientation
        self.prev_ori_camera = self.camera.frame.get_orientation()

        self.lookup_table = self.create_lookup_table()
        self._animate_different_corners()
        self._show_base_cases()
        
        # # Sphere
        # sphere = Sphere(radius=1, color=BLUE, opacity=0.2)

        # # Axes
        # axes = ThreeDAxes()
        # axes.set_color(GREY)
        # self.add(axes)

        # # self.run_marching_cubes(sphere)
        # self.add(sphere)
        # self.wait(1)


    def _animate_different_corners(self):
        cube = Cube(self, 3.0)
        self.add(cube)

        # Define an updater function
        def rotate_cube(mob, dt):
            mob.rotate(PI/4 * dt, axis=OUT)  # rotate around z-axis
            mob.rotation_frame = ((PI/4 * dt) % (2 * PI), OUT)
        
        # Add the updater
        cube.add_updater(rotate_cube)
        combos = [
            [0, 1, 2, 3],
            [0, 3, 4, 7],
            [0],
            [0, 3, 5, 6],
            [0, 1, 2],
            [0, 5],
            [0, 1, 2, 4],
            [0, 1, 5, 6],
        ]
        for combo in combos:
            cube.clear_vertices(animation=False)
            cube.add_vertices(combo)
            self.wait(1)

        # Remove the updater
        cube.remove_updater(rotate_cube)
        
        # Fade out the cube
        self.play(FadeOut(cube), run_time=1)

    def _show_base_cases(self):
        # Show the base cases
        rows = 3
        cols = 5
        spacing = 1.8

        cubes = []
        # Arrange manually
        for i, cube in enumerate(self.lookup_table):
            row = i // cols
            col = i % cols
            x = (col - (cols - 1)/2) * spacing
            z = - (row - (rows - 1)/2) * spacing
            cube.move_to(np.array([x, 0, z]))
            cubes.append(cube)

        self.play(*[FadeIn(cube) for cube in cubes])
        
        # First animation - rotations
        rotations = []
        for i, cube in enumerate(cubes):
            if i % 3 == 0:
                rotations.append(Rotate(cube, PI, axis=RIGHT))
            elif i % 3 == 1:
                rotations.append(Rotate(cube, PI, axis=UP))
            else:
                rotations.append(Rotate(cube, PI, axis=OUT))

        self.play(*rotations, run_time=2)
        self.play(*rotations, run_time=2)

        # Mirror the cubes
        vertices_to_fade_out = []
        vertices_to_fade_in = []
        for cube in cubes:
            mirror_idx = set(0, 1, 2, 3, 4, 5, 6, 7) - set(cube.vertex_idx)
            v = cube.clear_vertices(animation=True)
            vertices_to_fade_out.extend(v)
            v = cube.add_vertices(mirror_idx, animation=True)
            vertices_to_fade_in.extend(v)

        self.play(*[FadeOut(dot) for dot in vertices_to_fade_out])
        self.play(*[FadeIn(dot) for dot in vertices_to_fade_in])

        # Create target arrangement
        target_group = Group(*cubes).copy()
        target_group.arrange(
            direction=RIGHT,
            buff=1.0  # spacing between cubes
        ).scale(0.4)  # scale down the entire group
        target_group.move_to([0, 0, 3])  # move to top of screen
        
        # Animate each cube to its target position
        self.play(
            *[
                Transform(cube, target)
                for cube, target in zip(cubes, target_group)
            ],
            run_time=2
        )

        self.wait(1)
    
    def run_marching_cubes(self, shape):
        self.scale = 0.5
        self.shape = shape
        scale = 0.5
        
        # Create a 3D grid of points
        x = np.arange(-1, 2, scale)
        y = np.arange(-1, 2, scale)
        z = np.arange(-1, 2, scale)
        X, Y, Z = np.meshgrid(x, y, z)

        self._run_marching_cubes(1, 0, 0)

        # for i in range(X.shape[0]):
        #     print(f"i: {i}")
        #     for j in range(X.shape[1]):
        #         for k in range(X.shape[2]):
        #             # Check if the point is inside the sphere
        #             vertices = []
        #             for index, v in enumerate(vertex_locations_scaled):
        #                 if ((X[i, j, k] + v[0])**2 + (Y[i, j, k] + v[1])**2 + (Z[i, j, k] + v[2])**2)**0.5 < shape.radius:
        #                     vertices.append(index)
        #             if len(vertices) > 4:
        #                 # mirror the vertices
        #                 vertices = {0, 1, 2, 3, 4, 5, 6, 7} - set(vertices)
        #             vertices = [tuple(vertex_locations[vert]) for vert in vertices]
        #             # print(vertices)
        #             if len(vertices) == 0 or len(vertices) == 8:
        #                 continue
        #             matching_cube, axis, angle = self.find_matching_cube(vertices)
        #             matching_cube = matching_cube.scale(scale)
        #             matching_cube.rotate(angle, axis=axis)
        #             matching_cube.move_to(np.array([X[i, j, k], Y[i, j, k], Z[i, j, k]]))
        #             self.add(matching_cube)
        # print(X, Y, Z)
        # 2.4, -1, 2.4
        # for i in range(X.shape[0]):
        #     print(f"i: {i}")
        #     for j in range(X.shape[1]):
        #         for k in range(X.shape[2]):
        #             # Check if the point is inside the sphere
        #             self._run_marching_cubes(X[i, j, k], Y[i, j, k], Z[i, j, k])

    def _run_marching_cubes(self, x, y, z):
        scale = self.scale
        shape = self.shape
        vertex_locations = np.array([
            [-0.5, -0.5, -0.5],  # 0
            [ 0.5, -0.5, -0.5],  # 1
            [ 0.5,  0.5, -0.5],  # 2
            [-0.5,  0.5, -0.5],  # 3
            [-0.5, -0.5,  0.5],  # 4
            [ 0.5, -0.5,  0.5],  # 5
            [ 0.5,  0.5,  0.5],  # 6
            [-0.5,  0.5,  0.5]   # 7
        ])

        vertex_locations_scaled = vertex_locations * scale
        # Check if the point is inside the sphere
        vertices = []
        for index, v in enumerate(vertex_locations_scaled):
            if ((x + v[0])**2 + (y + v[1])**2 + (z + v[2])**2)**0.5 < shape.radius:
                vertices.append(index)
        if len(vertices) > 4:
            # mirror the vertices
            vertices = {0, 1, 2, 3, 4, 5, 6, 7} - set(vertices)
        vertices = [tuple(vertex_locations[vert]) for vert in vertices]
        if len(vertices) == 0 or len(vertices) == 8:
            return
        matching_cube, axis, angle = self.find_matching_cube(vertices)
        matching_cube = matching_cube.scale(scale)
        matching_cube.rotate(angle, axis=axis)
        matching_cube.move_to(np.array([x, y, z]))
        self.add(matching_cube)
    

    def find_matching_cube(self, vertices):
        # 24 possible rotations
        cube_rotations = [
            # Identity
            (np.array([0, 0, 1]),   0),

            # 90°, 180°, 270° about X
            (np.array([1, 0, 0]),  PI / 2),
            (np.array([1, 0, 0]),  PI),
            (np.array([1, 0, 0]),  3 * PI / 2),

            # 90°, 180°, 270° about Y
            (np.array([0, 1, 0]),  PI / 2),
            (np.array([0, 1, 0]),  PI),
            (np.array([0, 1, 0]),  3 * PI / 2),

            # 90°, 180°, 270° about Z
            (np.array([0, 0, 1]),  PI / 2),
            (np.array([0, 0, 1]),  PI),
            (np.array([0, 0, 1]),  3 * PI / 2),

            # 120°, 240° about body diagonals
            (np.array([1, 1, 1]),   2 * PI / 3),
            (np.array([1, 1, 1]),   4 * PI / 3),
            (np.array([-1, 1, 1]),  2 * PI / 3),
            (np.array([-1, 1, 1]),  4 * PI / 3),
            (np.array([1, -1, 1]),  2 * PI / 3),
            (np.array([1, -1, 1]),  4 * PI / 3),
            (np.array([1, 1, -1]),  2 * PI / 3),
            (np.array([1, 1, -1]),  4 * PI / 3),

            # 180° about face diagonals (edge centers)
            (np.array([0, 1, 1]),   PI),
            (np.array([0, -1, 1]),  PI),
            (np.array([1, 0, 1]),   PI),
            (np.array([-1, 0, 1]),  PI),
            (np.array([1, 1, 0]),   PI),
            (np.array([-1, 1, 0]),  PI),
        ]


        # Find the cube in the lookup table that matches the given vertices
        for cube in self.lookup_table:
            for axis, angle in cube_rotations:
                rotated_cubeVs = self.rotate_points(cube.get_vertex_locations(), axis, angle)
                if set(vertices) == set(rotated_cubeVs):
                    return (copy.deepcopy(cube), axis, angle)

    def rotate_points(self, points, axis, angle):
        matrix = rotation_matrix(angle, axis)
        return [tuple(np.round(matrix.dot(p), 2)) for p in points]

    def create_lookup_table(self):
        baseCubes = [
            {
                "vertices": [0, 2, 3, 6],
                "triangles": [
                    [0, 8, 11],
                    [0, 1, 5],
                    [0, 11, 5],
                    [11, 5, 6]
                ]
            },
            {
                "vertices": [0, 4, 6, 2],
                "triangles": [
                    [0, 3, 7],
                    [7, 4, 0],
                    [1, 2, 6],
                    [6, 5, 1]
                ]
            },
            {
                "vertices": [1, 4, 6],
                "triangles": [
                    [8, 4, 7],
                    [0, 1, 9],
                    [10, 5, 6]
                ]
            },
            {
                "vertices": [0, 1, 6],
                "triangles": [
                    [3, 1, 8],
                    [1, 8, 9],
                    [10, 5, 6]
                ]
            },
            {
                "vertices": [0, 6],
                "triangles": [
                    [8, 0, 3],
                    [10, 5, 6],
                ]
            },
            {
                "vertices": [1, 2, 3, 7],
                "triangles": [
                    [3, 0, 7],
                    [0, 10, 9],
                    [0, 10, 7],
                    [7, 6, 10]
                ]
            },
            {
                "vertices": [0, 2, 3, 7],
                "triangles": [
                    [8, 7, 6],
                    [8, 6, 0],
                    [0, 6, 10],
                    [0, 1, 10]  
                ]
            },
            {
                "vertices": [0, 2, 5, 7],
                "triangles": [
                    [0, 3, 8],
                    [6, 7, 11],
                    [4, 9, 6],
                    [1, 2, 10]
                ]
            },
            {
                "vertices": [1, 2, 3, 4],
                "triangles": [
                    [8, 7, 4],
                    [0, 3, 9],
                    [3, 11, 9],
                    [9, 10, 11]
                ]
            },
            {
                "vertices": [0, 1, 2, 3],
                "triangles": [
                    [8, 9, 11],
                    [9, 10, 11]
                ]
            },
            {
                "vertices": [1, 2, 3],
                "triangles": [
                    [9, 10, 11],
                    [3, 11, 9], 
                    [0, 3, 9]
                ]
            },
            {
                "vertices": [0, 5],
                "triangles": [
                    [0, 3, 8],
                    [4, 5, 9]
                ]
            },
            {
                "vertices": [0, 1],
                "triangles":[
                    [3, 1, 8],
                    [8, 9, 1]
                ]
            },
            {
                "vertices": [0],
                "triangles":[
                    [3, 0, 8],
                ]
            },
            {
                "vertices": [],
                "triangles":[]
            },
        ]
        table = []
        for c in baseCubes:
            cube = Cube(self, 1.0, c["vertices"], c["triangles"])
            table.append(cube)
        return table