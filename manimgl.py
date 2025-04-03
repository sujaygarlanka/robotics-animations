from manim import *
import numpy as np

config.renderer = "opengl"
class Gimbal3D(ThreeDScene):
    def construct(self):
        # Set camera view
        # self.set_camera_orientation(phi=70 * DEGREES, theta=-45 * DEGREES)

        # Add legend and coordinate frame (labels will remain fixed on screen)
        self._add_legend()
        # self._display_coordinate_frame(np.array([-4, -5, -3]))

        # Define display commands: each command is a pair [strings, numeric angles]
        display_commands = [
            [["\\pi/2", "\\pi/2", "0"], [PI/2, PI/2, 0]],
            [["0", "\\pi/2", "0"], [0, PI/2, PI/2]]
        ]

        # For this example, run one cycle (i in range(1))
        for i in range(1):
            # Create the rings and arrow
            outer_ring, middle_ring, inner_ring, arrow = self._create_rings()
            self.add(outer_ring, middle_ring, inner_ring, arrow)
            command = display_commands[i]
            command_text = self._display_commands(command[0])
            command_nums = command[1]
            
            ## Animations
            # Roll: rotate all components around RIGHT (X-axis)
            self.wait(0.5)
            self.play(
                command_text[0].animate.set_opacity(1),
                ApplyMethod(outer_ring.rotate(angle=command_nums[0], axis=RIGHT)),
                ApplyMethod(middle_ring.rotate(angle=command_nums[0], axis=RIGHT)),
                ApplyMethod(inner_ring.rotate(angle=command_nums[0], axis=RIGHT)),
                ApplyMethod(arrow.rotate(angle=command_nums[0], axis=RIGHT)),
            )
            
            # Pitch: rotate remaining parts around the OUT axis (camera's depth direction)
            self.wait(0.5)
            # self.play(
            #     command_text[0].animate.set_opacity(0.4),
            #     command_text[1].animate.set_opacity(1),
            #     ApplyMethod(middle_ring.rotate, angle=command_nums[1], axis=OUT),
            #     ApplyMethod(inner_ring.rotate, angle=command_nums[1], axis=OUT),
            #     ApplyMethod(arrow.rotate, angle=command_nums[1], axis=OUT),
            # )

            # (Yaw section commented out; you can enable or adjust it as needed.)
            # self.wait(0.5)
            # self.play(
            #     command_text[1].animate.set_opacity(0.4),
            #     command_text[2].animate.set_opacity(1),
            #     Rotate(inner_ring, angle=command_nums[2], axis=new_yaw_axis, run_time=2),
            #     Rotate(arrow, angle=command_nums[2], axis=new_yaw_axis, run_time=2)
            # )     

            # (Fade-out section commented out; enable if you want the objects to disappear at the end.)
            # self.play(
            #     FadeOut(outer_ring),
            #     FadeOut(middle_ring),
            #     FadeOut(inner_ring),
            #     FadeOut(arrow),
            #     *[FadeOut(item) for item in command_text],
            # )
    
    def _create_rings(self):
        # Parameters
        ring_thickness = 0.13  # Tube (minor) radius

        # Outer Torus (Roll ring)
        outer_ring_sphere = Sphere(radius=0.2, color=RED, resolution=(32, 32))
        outer_ring_ob = Torus(major_radius=3, minor_radius=ring_thickness, color=RED, resolution=(32, 32))
        outer_ring_sphere.move_to(outer_ring_ob.get_center() + np.array([-3, 0, 0]))
        outer_ring = VGroup(outer_ring_ob, outer_ring_sphere)
        outer_ring.rotate(PI / 2, axis=UP)

        # Middle Torus (Pitch ring)
        middle_ring_sphere = Sphere(radius=0.2, color=GREEN, resolution=(32, 32))
        middle_ring_ob = Torus(major_radius=2.5, minor_radius=ring_thickness, color=GREEN, resolution=(32, 32))
        middle_ring_sphere.move_to(middle_ring_ob.get_center() + np.array([0, 2.5, 0]))
        middle_ring = VGroup(middle_ring_ob, middle_ring_sphere)
        middle_ring.rotate(PI / 2, axis=RIGHT)

        # Inner Torus (Yaw ring)
        inner_ring_sphere = Sphere(radius=0.2, color=BLUE, resolution=(32, 32))
        inner_ring_ob = Torus(major_radius=2.1, minor_radius=ring_thickness, color=BLUE, resolution=(32, 32))
        inner_ring_sphere.move_to(inner_ring_ob.get_center() + np.array([2.1, 0, 0]))
        inner_ring = VGroup(inner_ring_ob, inner_ring_sphere)

        # Center the rings together
        middle_ring.move_to(outer_ring.get_center())
        inner_ring.move_to(outer_ring.get_center())

        arrow = self._create_arrow_3D()
        arrow.move_to(outer_ring.get_center())

        return outer_ring, middle_ring, inner_ring, arrow
    
    def _display_coordinate_frame(self, origin=ORIGIN, axis_length=1.0, axis_thickness=0.05):
        """Create a 3D coordinate frame with X, Y, and Z axes."""
        x_axis = Arrow3D(start=origin, end=origin + np.array([axis_length, 0, 0]), stroke_width=axis_thickness, color=RED)
        y_axis = Arrow3D(start=origin, end=origin + np.array([0, axis_length, 0]), stroke_width=axis_thickness, color=GREEN)
        z_axis = Arrow3D(start=origin, end=origin + np.array([0, 0, axis_length]), stroke_width=axis_thickness, color=BLUE)
        
        # Labels
        x_label = Text("X", color=RED).scale(0.5).next_to(x_axis.get_end(), RIGHT, buff=0.1)
        y_label = Text("Y", color=GREEN).scale(0.5).next_to(y_axis.get_end(), UP, buff=0.1)
        z_label = Text("Z", color=BLUE).scale(0.5).next_to(z_axis.get_end(), OUT, buff=0.1)
        
        # Group all elements
        frame = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        self.add(frame)

        # Fix labels so they always face the camera
        for label in [x_label, y_label, z_label]:
            self.add_fixed_in_frame_mobjects(label)
        return frame
        
    def _add_legend(self):
        legend_items = VGroup(
            self._legend_entry(RED, "Roll (X-axis)"),
            self._legend_entry(GREEN, "Pitch (Y-axis)"),
            self._legend_entry(BLUE, "Yaw (Z-axis)")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UL)

        for item in legend_items:
            self.add_fixed_in_frame_mobjects(item)

    def _legend_entry(self, color, label_text):
        """Helper method to create a color dot and label pair."""
        color_box = Circle(radius=0.15, fill_opacity=1, color=color)
        label = Text(label_text, font_size=24, color=color).next_to(color_box, RIGHT, buff=0.2)
        return VGroup(color_box, label)
    
    def _display_commands(self, commands):
        roll_command = MathTex(f"Roll: {commands[0]}", font_size=35, fill_opacity=0.5)
        pitch_command = MathTex(f"Pitch: {commands[1]}", font_size=35, fill_opacity=0.5)
        yaw_command = MathTex(f"Yaw: {commands[2]}", font_size=35, fill_opacity=0.5)

        command_group = VGroup(roll_command, pitch_command, yaw_command).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR)

        for command in command_group:
            self.add_fixed_in_frame_mobjects(command)

        return command_group
    
    def _create_arrow_3D(self):
        # Create a simple 3D arrow from a cylinder (shaft) and a cone (head)
        shaft = Cylinder(radius=0.05, height=2, direction=UP, fill_color=WHITE, fill_opacity=1)
        cone = Cone(base_radius=0.1, height=0.4, direction=UP, fill_color=WHITE, fill_opacity=1)
        cone.next_to(shaft, UP, buff=0)
        arrow = VGroup(shaft, cone)
        return arrow

# A simple Arrow3D class for Manim Community.
class Arrow3D(Arrow):
    """A 3D arrow that works in a ThreeDScene.
    It extends the built-in Arrow by allowing 3D coordinates.
    """
    def __init__(self, start=ORIGIN, end=RIGHT, **kwargs):
        super().__init__(start=start, end=end, **kwargs)