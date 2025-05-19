from manimlib import *
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

    CUBE_VERTICES = [
        [-0.5, -0.5, -0.5],  # 0
        [ 0.5, -0.5, -0.5],  # 1
        [ 0.5,  0.5, -0.5],  # 2
        [-0.5,  0.5, -0.5],  # 3
        [-0.5, -0.5,  0.5],  # 4
        [ 0.5, -0.5,  0.5],  # 5
        [ 0.5,  0.5,  0.5],  # 6
        [-0.5,  0.5,  0.5]   # 7
    ]

    # Edge → (start corner index, end corner index)
    CUBE_EDGES = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # bottom face
        (4, 5), (5, 6), (6, 7), (7, 4),  # top face
        (0, 4), (1, 5), (2, 6), (3, 7)   # verticals
    ]

    def __init__(self, vertices=[], triangles=[]):
        super().__init__()
        self.edges = []
        self.vertices = []
        self.triangles = []
        self.create_cube()
        self.update_vertices(vertices)
        self.update_triangles(triangles)

    def create_cube(self):
        # Draw cube edges
        for i, j in Cube.CUBE_EDGES:
            edge = Line(
                np.array(Cube.CUBE_VERTICES[i]),
                np.array(Cube.CUBE_VERTICES[j]),
                color=BLACK,
                stroke_width=1.0,
            )
            self.edges.append(edge)
            self.add(edge)

    def update_vertices(self, vertices):
        # Clear previous vertices
        for dot in self.vertices:
            self.remove(dot)
        self.vertices = []

        # Visualize corners
        for idx, pos in enumerate(Cube.CUBE_VERTICES):
            o = 1.0 if idx in vertices else 0.0
            dot = Sphere(radius=0.05, opacity=o, color=RED)
            dot.move_to(np.array(pos))
            # if idx in vertices:
            #     dot.set_color(RED)
            # dot.set_fill(RED, opacity=opacity)
            self.vertices.append(dot)
            self.add(dot)

    def update_triangles(self, triangles):
        # Clear previous triangles
        for triangle in self.triangles:
            self.remove(triangle)
        self.triangles = []

        for t in triangles:
            triangle_points = []
            for edge in t:
                e = Cube.CUBE_EDGES[edge]
                v1 = Cube.CUBE_VERTICES[e[0]]
                v2 = Cube.CUBE_VERTICES[e[1]]
                triangle_points.append((v1 + v2)/2.0)
            triangle = Polygon(triangle_points[0], triangle_points[1], triangle_points[2])
            triangle.set_fill(YELLOW, opacity=1.0)
            triangle.set_stroke(BLACK, width=1)
            self.add(triangle)

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
        self.camera.frame.reorient(phi_degrees=75, theta_degrees=45)

        # # Add a coordinate frame to the scene
        # coord_frame = self.create_coordinate_frame(
        #     origin=np.array([-4, -3, -3]),  # Position in bottom left corner
        #     axis_length=1.5,
        #     axis_thickness=0.05
        # )
        # self.add(coord_frame)

        # # Make the text labels face the camera
        # for label in [coord_frame[3], coord_frame[4], coord_frame[5]]:  # The text labels
        #     self.add(label)

        self.lookup_table = self.create_lookup_table()


        # Sphere
        sphere = Sphere(radius=1, color=BLUE, opacity=0.2)

        # Axes
        axes = ThreeDAxes()
        axes.set_color(GREY)
        self.add(axes)

        self.run_marching_cubes(sphere)
        self.add(sphere)
        self.wait(1)
    
    def run_marching_cubes(self, shape):
        self.scale = 0.1
        self.shape = shape
        scale = 0.1
        
        # Create a 3D grid of points
        x = np.arange(-1, 2, scale)
        y = np.arange(-1, 2, scale)
        z = np.arange(-1, 2, scale)
        X, Y, Z = np.meshgrid(x, y, z)

        # vertex_locations = np.array([
        #     [-0.5, -0.5, -0.5],  # 0
        #     [ 0.5, -0.5, -0.5],  # 1
        #     [ 0.5,  0.5, -0.5],  # 2
        #     [-0.5,  0.5, -0.5],  # 3
        #     [-0.5, -0.5,  0.5],  # 4
        #     [ 0.5, -0.5,  0.5],  # 5
        #     [ 0.5,  0.5,  0.5],  # 6
        #     [-0.5,  0.5,  0.5]   # 7
        # ])

        # vertex_locations_scaled = vertex_locations * scale

        # sp = [2.0, -1.0, -1.0]
        # vertices = []
        # for i, v in enumerate(vertex_locations_scaled):
        #     if ((sp[0] + v[0])**2 + (sp[1] + v[1])**2 + (sp[2] + v[2])**2)**0.5 < shape.radius:
        #         vertices.append(tuple(vertex_locations[i]))

        # m_cube, axis, angle = self.find_matching_cube(vertices)
        # # self.add(m_cube)
        # m_cube = m_cube.scale(scale) 
        # # m_cube.rotate(angle, axis=axis)
        # m_cube.move_to(np.array([sp[0], sp[1], sp[2]]))
        # self.add(m_cube)
        # self.play(Rotate(m_cube, angle=angle, axis=axis), run_time=2)
        # print(axis, angle)

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
        for i in range(X.shape[0]):
            print(f"i: {i}")
            for j in range(X.shape[1]):
                for k in range(X.shape[2]):
                    # Check if the point is inside the sphere
                    self._run_marching_cubes(X[i, j, k], Y[i, j, k], Z[i, j, k])

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
    
    def create_coordinate_frame(self, origin=ORIGIN, axis_length=1.0, axis_thickness=0.05):
        """Create a 3D coordinate frame with X, Y, and Z axes."""
        x_axis = Cylinder(
            radius=axis_thickness,
            height=axis_length,
            axis=np.array([axis_length, 0, 0]),
            color=RED,
        )
        
        y_axis = Cylinder(
            radius=axis_thickness,
            height=axis_length,
            axis=np.array([0, axis_length, 0]),
            color=GREEN,
        )
        
        z_axis = Cylinder(
            radius=axis_thickness,
            height=axis_length,
            axis=np.array([0, 0, axis_length]),
            color=BLUE,
        )
        
        # Labels
        x_label = Text("X", color=RED).scale(0.5).next_to(x_axis.get_end(), RIGHT, buff=0.1)
        y_label = Text("Y", color=GREEN).scale(0.5).next_to(y_axis.get_end(), UP, buff=0.1)
        z_label = Text("Z", color=BLUE).scale(0.5).next_to(z_axis.get_end(), OUT, buff=0.1)
        
        # Group all elements
        frame = Group(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        return frame
    
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
        for cube, cubeVs in self.lookup_table:
            for axis, angle in cube_rotations:
                rotated_cubeVs = self.rotate_points(cubeVs, axis, angle)
                if set(vertices) == set(rotated_cubeVs):
                    return (copy.deepcopy(cube), axis, angle)

    def rotate_points(self, points, axis, angle):
        matrix = rotation_matrix(angle, axis)
        return [tuple(np.round(matrix.dot(p), 2)) for p in points]

    def create_lookup_table(self):
        # vertex locations for a cube center at origin and a side length of 1
        vertexLocations = [
            [-0.5, -0.5, -0.5],  # 0
            [ 0.5, -0.5, -0.5],  # 1
            [ 0.5,  0.5, -0.5],  # 2
            [-0.5,  0.5, -0.5],  # 3
            [-0.5, -0.5,  0.5],  # 4
            [ 0.5, -0.5,  0.5],  # 5
            [ 0.5,  0.5,  0.5],  # 6
            [-0.5,  0.5,  0.5]   # 7
        ]

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
                "vertices": [0, 1, 2, 3, 4, 5, 6, 7],
                "triangles":[]
            },
            {
                "vertices": [],
                "triangles":[]
            },
        ]
        table = []
        for c in baseCubes:
            cube = self.create_cube(c["vertices"], c["triangles"])
            cubeVs = []
            for v in c["vertices"]:
                cubeVs.append(tuple(vertexLocations[v]))
            table.append((cube, cubeVs))
        return table

    # def create_cube(self, vertices, triangles):
    #     # https://sketchfab.com/3d-models/15-cases-marching-cubes-representation-78927bfd96694fccbc064bb5fe820f3d
    #     # https://www.cs.carleton.edu/cs_comps/0405/shape/marching_cubes.html
    #     #                 v7_______e6_____________v6
    #     #                  /|                    /|
    #     #                 / |                   / |
    #     #              e7/  |                e5/  |
    #     #               /___|______e4_________/   |
    #     #            v4|    |                 |v5 |e10
    #     #              |    |                 |   |
    #     #              |    |e11              |e9 |
    #     #            e8|    |                 |   |
    #     #              |    |_________________|___|
    #     #              |   / v3      e2       |   /v2
    #     #              |  /                   |  /
    #     #              | /e3                  | /e1
    #     #              |/_____________________|/
    #     #              v0         e0          v1
            

    #     # Cube corners (0–7) in 3D space
    #     CUBE_VERTICES = [
    #         np.array([0, 0, 0]),  # 0
    #         np.array([1, 0, 0]),  # 1
    #         np.array([1, 1, 0]),  # 2
    #         np.array([0, 1, 0]),  # 3
    #         np.array([0, 0, 1]),  # 4
    #         np.array([1, 0, 1]),  # 5
    #         np.array([1, 1, 1]),  # 6
    #         np.array([0, 1, 1]),  # 7
    #     ]

    #     # Edge → (start corner index, end corner index)
    #     CUBE_EDGES = [
    #         (0, 1), (1, 2), (2, 3), (3, 0),  # bottom face
    #         (4, 5), (5, 6), (6, 7), (7, 4),  # top face
    #         (0, 4), (1, 5), (2, 6), (3, 7)   # verticals
    #     ]

    #     cube = Group()

    #     # Draw cube edges
    #     for i, j in CUBE_EDGES:
    #         edge = Line(
    #             np.array(CUBE_VERTICES[i]),
    #             np.array(CUBE_VERTICES[j]),
    #             color=BLACK,
    #             stroke_width=1.0,
    #         )
    #         cube.add(edge)

    #     # Visualize corners
    #     for idx, pos in enumerate(CUBE_VERTICES):
    #         o = 1.0 if idx in vertices else 0.0
    #         dot = Sphere(radius=0.05, opacity=o, color=RED)
    #         dot.move_to(np.array(pos))
    #         # if idx in vertices:
    #         #     dot.set_color(RED)
    #         # dot.set_fill(RED, opacity=opacity)
    #         cube.add(dot)

    #     # Polygon faces
    #     for t in triangles:
    #         triangle_points = []
    #         for edge in t:
    #             e = CUBE_EDGES[edge]
    #             v1 = CUBE_VERTICES[e[0]]
    #             v2 = CUBE_VERTICES[e[1]]
    #             triangle_points.append((v1 + v2)/2.0)
    #         triangle = Polygon(triangle_points[0], triangle_points[1], triangle_points[2])
    #         triangle.set_fill(YELLOW, opacity=1.0)
    #         triangle.set_stroke(BLACK, width=1)
    #         cube.add(triangle)
    #     # cube.rotate(PI, axis=UP)
    #     # self.add(cube)

    #     return cube