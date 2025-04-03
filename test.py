from manim import *

class Gimbal3D(ThreeDScene):
    def construct(self):
        # Set camera view
        self.set_camera_orientation(phi=70 * DEGREES, theta=150 * DEGREES)

        # Parameters
        ring_thickness = 0.13  # tube radius

        # Outer Torus (Roll ring)
        # outer_ring_dot = Sphere(color=RED)
        outer_ring_sphere = Sphere(radius=0.2, checkerboard_colors=[RED, RED], stroke_color=RED)
        outer_ring_ob = Torus(major_radius=3, minor_radius=ring_thickness, checkerboard_colors=[RED, RED], stroke_color=RED)
        outer_ring_sphere.move_to(outer_ring_ob.get_center() + np.array([-3, 0, 0]))
        outer_ring = VGroup(outer_ring_ob, outer_ring_sphere)
        outer_ring.rotate(PI / 2, axis=UP)

        # Middle Torus (Pitch ring)
        middle_ring_sphere = Sphere(radius=0.2, checkerboard_colors=[GREEN, GREEN], stroke_color=GREEN)
        middle_ring_ob = Torus(major_radius=2.5, minor_radius=ring_thickness, checkerboard_colors=[GREEN, GREEN], stroke_color=GREEN)
        middle_ring_sphere.move_to(middle_ring_ob.get_center() + np.array([0, 2.5, 0]))
        middle_ring = VGroup(middle_ring_ob, middle_ring_sphere)
        middle_ring.rotate(PI / 2, axis=RIGHT)

        # Inner Torus (Yaw ring)
        inner_ring_sphere = Sphere(radius=0.2, checkerboard_colors=[BLUE, BLUE], stroke_color=BLUE)
        inner_ring_ob = Torus(major_radius=2.1, minor_radius=ring_thickness, checkerboard_colors=[BLUE, BLUE], stroke_color=BLUE)
        inner_ring_sphere.move_to(inner_ring_ob.get_center() + np.array([-2.1, 0, 0]))
        inner_ring = VGroup(inner_ring_ob, inner_ring_sphere)
        # inner_ring.rotate(PI / 2, axis=RIGHT)

        # Position all rings at the center
        middle_ring.move_to(outer_ring.get_center())
        inner_ring.move_to(outer_ring.get_center())

        arrow = Arrow3D(
            start=np.array([1.5, 0, 0]),
            end=np.array([-1.5, 0, 0]),
            resolution=8,
            thickness=0.1,
            color=RED
        )
        # arrow = self.create_extruded_arrow(color=RED, scale_factor=1.5, depth=0.1)
        arrow.move_to(outer_ring.get_center())

        arrowTest = self._create_arrow_3D()
        # .move_to(outer_ring.get_center())
        arrowTest.move_to(outer_ring.get_center())
        self.add(arrowTest)

        # Add to scene
        self.add(outer_ring, middle_ring, inner_ring, arrow)
        # arrow_3 = Arrow(start=LEFT, end=RIGHT)

        legend_items = VGroup(
            self._legend_entry(RED, "Roll (X-axis)"),
            self._legend_entry(GREEN, "Pitch (Y-axis)"),
            self._legend_entry(BLUE, "Yaw (Z-axis)")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL)

        for item in legend_items:
            self.add_fixed_in_frame_mobjects(item)

        # Animations
        self.wait(1)
        self.play(Rotate(arrowTest, angle=PI / 2, axis=UP, run_time=2))     # Roll
        # self.play(Rotate(outer_ring, angle=PI / 2, axis=RIGHT, run_time=2))     # Roll
        # self.play(Rotate(middle_ring, angle=PI / 2, axis=RIGHT, run_time=2))  # Pitch
        # self.play(Rotate(inner_ring, angle=PI / 2, axis=UP, run_time=2))     # Yaw
        # self.play(self.move_camera(theta=180 * DEGREES, run_time=1))
        # self.wait(2)
    def _legend_entry(self, color, label_text):
        """Helper method to create a colored square and label pair"""
        color_box = Circle(radius=0.15, fill_color=color, fill_opacity=1, stroke_width=0)
        label = Text(label_text, font_size=24).next_to(color_box, RIGHT, buff=0.2)
        return VGroup(color_box, label)
    
    def _create_arrow_3D(self):
        vertex_coords = [
            [1, 1, 0],
            [1, -1, 0],
            [-1, -1, 0],
            [-1, 1, 0],
            [0, 0, 2]
        ]
        faces_list = [
            [0, 1, 4],
            [1, 2, 4],
            [2, 3, 4],
            [3, 0, 4],
            [0, 1, 2, 3]
        ]
        prism = Prism(dimensions=[3, 0.5, 0.5])
        pyramid = Polyhedron(vertex_coords, faces_list)
        pyramid.rotate(-PI / 2, axis=UP)
        pyramid.scale(0.5)
        pyramid.move_to(prism.get_center() + np.array([-1.5, 0, 0]))
        return VGroup(prism, pyramid)
    
