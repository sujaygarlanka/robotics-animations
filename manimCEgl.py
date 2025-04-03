from manim import *
from manim.opengl import *
from manim.mobject.opengl.opengl_geometry import *
from manim.renderer.opengl_renderer import OpenGLCamera
from manim.typing import Point3DLike, Vector3D
from collections.abc import Sequence
from manim.utils import opengl

config.renderer = "opengl"
# config.write_to_movie = False
config.fullscreen = True


class OpenGLSphere(OpenGLSurface):
    def __init__(
        self,
        center: Point3DLike = ORIGIN,
        radius: float = 1,
        u_range: Sequence[float] = (0, TAU),
        v_range: Sequence[float] = (0, PI),
        **kwargs,
    ) -> None:
        self.radius = radius

        super().__init__(
            self.func,
            u_range=u_range,
            v_range=v_range,
            **kwargs,
        )

        self.shift(center)

    def func(self, u: float, v: float) -> np.ndarray:
        return self.radius * np.array(
            [np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)],
        )


class OpenGLTorus(OpenGLSurface):
    """A torus.

    Parameters
    ----------
    major_radius
        Distance from the center of the tube to the center of the torus.
    minor_radius
        Radius of the tube.
    u_range
        The range of the ``u`` variable: ``(u_min, u_max)``.
    v_range
        The range of the ``v`` variable: ``(v_min, v_max)``.
    resolution
        The number of samples taken of the :class:`Torus`. A tuple can be
        used to define different resolutions for ``u`` and ``v`` respectively.

    Examples
    --------
    .. manim :: ExampleTorus
        :save_last_frame:

        class ExampleTorus(ThreeDScene):
            def construct(self):
                axes = ThreeDAxes()
                torus = Torus()
                self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
                self.add(axes, torus)
    """

    def __init__(
        self,
        major_radius: float = 3,
        minor_radius: float = 1,
        u_range: Sequence[float] = (0, TAU),
        v_range: Sequence[float] = (0, TAU),
        resolution: tuple[int, int] = (101, 101),
        **kwargs,
    ) -> None:
        self.R = major_radius
        self.r = minor_radius
        super().__init__(
            self.func,
            u_range=u_range,
            v_range=v_range,
            resolution=resolution,
            **kwargs,
        )

    def func(self, u: float, v: float) -> np.ndarray:
        """The z values defining the :class:`Torus` being plotted.

        Returns
        -------
        :class:`numpy.ndarray`
            The z values defining the :class:`Torus`.
        """
        P = np.array([np.cos(u), np.sin(u), 0])
        return (self.R - self.r * np.cos(v)) * P - self.r * np.sin(v) * OUT


#! Uwezi Cube
class OpenGLPrism(OpenGLGroup):
    def __init__(self, x_length=2, y_length=1, z_length=1, color=BLUE, **kwargs):
        x = x_length / 2
        y = y_length / 2
        z = z_length / 2
        obj = [
            OpenGLSurface(
                lambda u, v: np.array(p0) + u * np.array(a) + v * np.array(b),
                u_range=[-1, 1],  # u and v are normalized
                v_range=[-1, 1],
                resolution=[2, 2],
                color=color,
            )
            for p0, a, b in [
                [[-x, 0, 0], [0, y, 0], [0, 0, z]],
                [[+x, 0, 0], [0, y, 0], [0, 0, z]],
                [
                    [0, -y, 0],
                    [x, 0, 0],
                    [0, 0, z],
                ],
                [[0, +y, 0], [x, 0, 0], [0, 0, z]],
                [[0, 0, -z], [x, 0, 0], [0, y, 0]],
                [[0, 0, +z], [x, 0, 0], [0, y, 0]],
            ]
        ]
        super().__init__(*obj, **kwargs)


class OpenGLCube(OpenGLPrism):
    def __init__(self, side_length=1, **kwargs):
        super().__init__(
            x_length=side_length, y_length=side_length, z_length=side_length, **kwargs
        )


class OpenGLCone(OpenGLSurface):
    def __init__(
        self,
        base_radius: float = 1,
        height: float = 1,
        direction: np.ndarray = Z_AXIS,
        show_base: bool = False,
        v_range: Sequence[float] = [0, TAU],
        u_min: float = 0,
        **kwargs,
    ) -> None:
        self.direction = direction
        self.theta = PI - np.arctan(base_radius / height)

        super().__init__(
            self.func,
            v_range=v_range,
            u_range=[u_min, np.sqrt(base_radius**2 + height**2)],
            **kwargs,
        )
        # used for rotations
        self.new_height = height
        self._current_theta = 0
        self._current_phi = 0
        self.base_circle = OpenGLCircle3D(
            radius=base_radius,
            color=self.color,
            opacity=self.opacity,
        )
        self.base_circle.shift(height * IN)
        self._set_start_and_end_attributes(direction)
        if show_base:
            self.add(self.base_circle)

        self._rotate_to_direction()

    def func(self, u: float, v: float) -> np.ndarray:
        """Converts from spherical coordinates to cartesian.

        Parameters
        ----------
        u
            The radius.
        v
            The azimuthal angle.

        Returns
        -------
        :class:`numpy.array`
            Points defining the :class:`Cone`.
        """
        r = u
        phi = v
        return np.array(
            [
                r * np.sin(self.theta) * np.cos(phi),
                r * np.sin(self.theta) * np.sin(phi),
                r * np.cos(self.theta),
            ],
        )

    def get_start(self) -> np.ndarray:
        return self.start_point.get_center()

    def get_end(self) -> np.ndarray:
        return self.end_point.get_center()

    def _rotate_to_direction(self) -> None:
        x, y, z = self.direction

        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(z / r) if r > 0 else 0

        if x == 0:
            if y == 0:  # along the z axis
                phi = 0
            else:
                phi = np.arctan(np.inf)
                if y < 0:
                    phi += PI
        else:
            phi = np.arctan(y / x)
        if x < 0:
            phi += PI

        # Undo old rotation (in reverse order)
        self.rotate(-self._current_phi, Z_AXIS, about_point=ORIGIN)
        self.rotate(-self._current_theta, Y_AXIS, about_point=ORIGIN)

        # Do new rotation
        self.rotate(theta, Y_AXIS, about_point=ORIGIN)
        self.rotate(phi, Z_AXIS, about_point=ORIGIN)

        # Store values
        self._current_theta = theta
        self._current_phi = phi

    def set_direction(self, direction: np.ndarray) -> None:
        """Changes the direction of the apex of the :class:`Cone`.

        Parameters
        ----------
        direction
            The direction of the apex.
        """
        self.direction = direction
        self._rotate_to_direction()

    def get_direction(self) -> np.ndarray:
        """Returns the current direction of the apex of the :class:`Cone`.

        Returns
        -------
        direction : :class:`numpy.array`
            The direction of the apex.
        """
        return self.direction

    def _set_start_and_end_attributes(self, direction):
        normalized_direction = direction * np.linalg.norm(direction)

        start = self.base_circle.get_center()
        end = start + normalized_direction * self.new_height
        self.start_point = OpenGLVectorizedPoint(start)
        self.end_point = OpenGLVectorizedPoint(end)
        self.add(self.start_point, self.end_point)


class OpenGLCircle3D(OpenGLSurface):
    def __init__(
        self,
        radius: float = 1,
        height: float = 2,
        direction: np.ndarray = Z_AXIS,
        u_range: Sequence[float] = [0, 1],
        v_range: Sequence[float] = [0, TAU],
        resolution: Sequence[int] = (24, 24),
        **kwargs,
    ):
        self._height = height
        self.radius = radius
        super().__init__(
            self.func,
            resolution=resolution,
            u_range=[radius * u for u in u_range],
            v_range=v_range,
            **kwargs,
        )
        self._current_phi = 0
        self._current_theta = 0
        self.set_direction(direction)

    def func(self, u: float, v: float) -> np.ndarray:
        """Generates a filled circle aligned with the given normal direction.

        Parameters
        ----------
        u : float
            The radial distance (0 to r).
        v : float
            The azimuthal angle (0 to TAU).

        Returns
        -------
        np.ndarray
            3D point in Cartesian coordinates.
        """
        return np.array(
            [
                u * np.cos(v),  # X coordinate
                u * np.sin(v),  # Y coordinate
                0,  # Z coordinate (circle lies in XY plane)
            ]
        )

    def _rotate_to_direction(self) -> None:
        x, y, z = self.direction

        r = np.sqrt(x**2 + y**2 + z**2)
        theta = np.arccos(z / r) if r > 0 else 0

        if x == 0:
            if y == 0:  # along the z axis
                phi = 0
            else:  # along the x axis
                phi = np.arctan(np.inf)
                if y < 0:
                    phi += PI
        else:
            phi = np.arctan(y / x)
        if x < 0:
            phi += PI

        # undo old rotation (in reverse direction)
        self.rotate(-self._current_phi, Z_AXIS, about_point=ORIGIN)
        self.rotate(-self._current_theta, Y_AXIS, about_point=ORIGIN)

        # do new rotation
        self.rotate(theta, Y_AXIS, about_point=ORIGIN)
        self.rotate(phi, Z_AXIS, about_point=ORIGIN)

        # store new values
        self._current_theta = theta
        self._current_phi = phi

    def set_direction(self, direction: np.ndarray) -> None:
        """Sets the direction of the central axis of the :class:`Cylinder`.

        Parameters
        ----------
        direction : :class:`numpy.array`
            The direction of the central axis of the :class:`Cylinder`.
        """
        # if get_norm(direction) is get_norm(self.direction):
        #     pass
        self.direction = direction
        self._rotate_to_direction()

    def get_direction(self) -> np.ndarray:
        """Returns the direction of the central axis of the :class:`Cylinder`.

        Returns
        -------
        direction : :class:`numpy.array`
            The direction of the central axis of the :class:`Cylinder`.
        """
        return self.direction


class Gimbal3D(ThreeDScene):
    def construct(self):
        # Set camera view
        self.set_camera_orientation(phi=70 * DEGREES, theta=(-45 + 90) * DEGREES)

        # Add to scene
        self._add_legend()
        self._display_coordinate_frame(np.array([-4, -5, -3]))
        display_commands = [
            [[r"\pi/2", r"\pi/2", r"0"], [PI / 2, PI / 2, 0]],
            [[r"0", r"\pi/2", r"0"], [0, PI / 2, PI / 2]],
        ]

        for i in range(1):
            # Create the rings and arrow
            outer_ring, middle_ring, inner_ring, arrow = self._create_rings()
            self.add(
                outer_ring, middle_ring, inner_ring, arrow
            )  # Add the rings and arrow to the scene
            command = display_commands[i]
            command_text = self._display_commands(command[0])
            command_nums = command[1]

            ## Animations
            # Roll
            self.wait(0.5)
            self.play(
                command_text[0].animate.set_opacity(1),
                Rotate(outer_ring, angle=command_nums[0], axis=RIGHT, run_time=2),
                Rotate(middle_ring, angle=command_nums[0], axis=RIGHT, run_time=2),
                Rotate(inner_ring, angle=command_nums[0], axis=RIGHT, run_time=2),
                Rotate(arrow, angle=command_nums[0], axis=RIGHT, run_time=2),
            )

            # Pitch
            self.wait(0.5)
            # applied_rotation = so3.from_axis_angle(([1.0, 0, 0], command_nums[0]))
            # new_pitch_axis = np.array(so3.apply(applied_rotation, [0, 1, 0]))
            # print(new_pitch_axis)
            self.play(
                command_text[0].animate.set_opacity(0.4),
                command_text[1].animate.set_opacity(1),
                Rotate(middle_ring, angle=command_nums[1], axis=OUT, run_time=2),
                Rotate(inner_ring, angle=command_nums[1], axis=OUT, run_time=2),
                Rotate(arrow, angle=command_nums[1], axis=OUT, run_time=2),
            )

        # # Yaw
        # applied_rotation = so3.mul(
        #     so3.from_axis_angle((list(new_pitch_axis), command_nums[1])),
        #     applied_rotation,
        # )
        # new_yaw_axis = np.array(so3.apply(applied_rotation, [0, 0, 1]))
        # self.wait(0.5)
        # self.play(
        #     command_text[1].animate.set_opacity(0.4),
        #     command_text[2].animate.set_opacity(1),
        #     Rotate(inner_ring, angle=command_nums[2], axis=new_yaw_axis, run_time=2),
        #     Rotate(arrow, angle=command_nums[2], axis=new_yaw_axis, run_time=2),
        # )

        # # Fade out the outer ring, middle ring, inner ring, arrow, and legend
        # self.play(
        #     FadeOut(outer_ring),
        #     FadeOut(middle_ring),
        #     FadeOut(inner_ring),
        #     FadeOut(arrow),
        #     *[FadeOut(item) for item in command_text],
        # )

    def _create_rings(self):
        # Parameters
        ring_thickness = 0.13  # tube radius

        # Outer Torus (Roll ring)
        outer_ring_sphere = OpenGLSphere(radius=0.2, color=RED)
        outer_ring_ob = OpenGLTorus(
            major_radius=3,
            minor_radius=ring_thickness,
            color=RED,
        )
        outer_ring_sphere.move_to(outer_ring_ob.get_center() + np.array([-3, 0, 0]))
        outer_ring = OpenGLGroup(outer_ring_ob, outer_ring_sphere)
        outer_ring.rotate(PI / 2, axis=UP)

        # Middle Torus (Pitch ring)
        middle_ring_sphere = OpenGLSphere(radius=0.2, color=GREEN)
        middle_ring_ob = OpenGLTorus(
            major_radius=2.5, minor_radius=ring_thickness, color=GREEN
        )
        middle_ring_sphere.move_to(middle_ring_ob.get_center() + np.array([0, 2.5, 0]))
        middle_ring = OpenGLGroup(middle_ring_ob, middle_ring_sphere)
        middle_ring.rotate(PI / 2, axis=RIGHT)

        # Inner Torus (Yaw ring)
        inner_ring_sphere = OpenGLSphere(radius=0.2, color=BLUE)
        inner_ring_ob = OpenGLTorus(
            major_radius=2.1,
            minor_radius=ring_thickness,
            color=BLUE,
        )
        inner_ring_sphere.move_to(inner_ring_ob.get_center() + np.array([2.1, 0, 0]))
        inner_ring = OpenGLGroup(inner_ring_ob, inner_ring_sphere)

        # Position all rings at the center
        middle_ring.move_to(outer_ring.get_center())
        inner_ring.move_to(outer_ring.get_center())

        arrow = self._create_arrow_3D()
        arrow.move_to(outer_ring.get_center())

        return outer_ring, middle_ring, inner_ring, arrow

    def _display_coordinate_frame(
        self, origin=ORIGIN, axis_length=1.0, axis_thickness=0.05
    ):
        """Create a 3D coordinate frame with X, Y, and Z axes."""
        x_axis = Arrow3D(
            start=origin,
            end=origin + np.array([axis_length, 0, 0]),
            resolution=8,
            thickness=axis_thickness,
            color=RED,
        )

        y_axis = Arrow3D(
            start=origin,
            end=origin + np.array([0, axis_length, 0]),
            resolution=8,
            thickness=axis_thickness,
            color=GREEN,
        )

        z_axis = Arrow3D(
            start=origin,
            end=origin + np.array([0, 0, axis_length]),
            resolution=8,
            thickness=axis_thickness,
            color=BLUE,
        )

        # Labels
        x_label = (
            Text("X", color=RED).scale(0.5).next_to(x_axis.get_end(), RIGHT, buff=0.1)
        )
        y_label = (
            Text("Y", color=GREEN).scale(0.5).next_to(y_axis.get_end(), UP, buff=0.1)
        )
        z_label = (
            Text("Z", color=BLUE).scale(0.5).next_to(z_axis.get_end(), OUT, buff=0.1)
        )

        # Group all elements
        frame = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)

        self.add(frame)

        # Make the text labels face the camera
        for label in [frame[3], frame[4], frame[5]]:  # The text labels
            self.add_fixed_orientation_mobjects(label)
        return frame

    def _add_legend(self):
        legend_items = (
            VGroup(
                self._legend_entry(RED, "Roll (X-axis)"),
                self._legend_entry(GREEN, "Pitch (Y-axis)"),
                self._legend_entry(BLUE, "Yaw (Z-axis)"),
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .to_corner(UL)
        )

        for item in legend_items:
            self.add_fixed_in_frame_mobjects(item)

    def _legend_entry(self, color, label_text):
        """Helper method to create a color dot and label pair"""
        color_box = Circle(
            radius=0.15, fill_color=color, fill_opacity=1, stroke_width=0
        )
        label = Text(label_text, font_size=24).next_to(color_box, RIGHT, buff=0.2)
        return VGroup(color_box, label)

    def _display_commands(self, commands):
        roll_command = MathTex(f"Roll: {commands[0]}", font_size=35, fill_opacity=0.5)
        pitch_command = MathTex(f"Pitch: {commands[1]}", font_size=35, fill_opacity=0.5)
        yaw_command = MathTex(f"Yaw: {commands[2]}", font_size=35, fill_opacity=0.5)

        command_group = (
            VGroup(roll_command, pitch_command, yaw_command)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            .to_corner(UR)
        )

        for command in command_group:
            self.add_fixed_in_frame_mobjects(command)

        return command_group

    def _create_arrow_3D(self):
        prism = OpenGLPrism(3, 0.4, 0.2, color=WHITE)
        pyramid_height = 0.8
        pyramid = OpenGLCone(
            base_radius=0.3, height=pyramid_height, color=WHITE, show_base=True
        )
        # make arrow tip in 3d
        pyramid.rotate(PI / 2, axis=UP)
        # pyramid.scale(0.3)
        pyramid.move_to(prism.get_center() + np.array([1.5 + pyramid_height / 2, 0, 0]))
        return OpenGLGroup(prism, pyramid)
