from manim import *

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

############################################################################################################

class TwoLinkRobotArm(Scene):
    def construct(self):
        # Define lengths of the links
        l1, l2 = 2, 1.5

        # Define initial angles in radians
        theta1 = PI / 6  # 30 degrees
        theta2 = PI / 4  # 45 degrees

        # Calculate joint positions
        joint1 = np.array([l1 * np.cos(theta1), l1 * np.sin(theta1), 0])
        joint2 = joint1 + np.array([l2 * np.cos(theta1 + theta2), l2 * np.sin(theta1 + theta2), 0])
        

        # Create base, joints, and links
        base = Dot(ORIGIN, color=RED)
        joint1_dot = Dot(joint1, color=BLUE)
        joint2_dot = Dot(joint2, color=GREEN)
        link1 = Line(start=ORIGIN, end=joint1, color=YELLOW)
        link2 = Line(start=joint1, end=joint2, color=YELLOW)

        # Add them to the scene
        self.add(base, link1, link2, joint1_dot, joint2_dot)

        # Define the update function
        def update_robot(dt):
            nonlocal theta1, theta2
            # Increment angles
            theta1 += dt
            theta2 += dt / 2

            # Recalculate joint positions
            joint1_new = np.array([l1 * np.cos(theta1), l1 * np.sin(theta1), 0])
            joint2_new = joint1_new + np.array([l2 * np.cos(theta1 + theta2), l2 * np.sin(theta1 + theta2), 0])

            # Update links
            link1.put_start_and_end_on(ORIGIN, joint1_new)
            link2.put_start_and_end_on(joint1_new, joint2_new)

            # Update joint dots
            joint1_dot.move_to(joint1_new)
            joint2_dot.move_to(joint2_new)

        # Use the updater on the specific objects
        link1.add_updater(lambda mob, dt: update_robot(dt))
        link2.add_updater(lambda mob, dt: update_robot(dt))
        joint1_dot.add_updater(lambda mob, dt: update_robot(dt))
        joint2_dot.add_updater(lambda mob, dt: update_robot(dt))

        # Let the animation run for 10 seconds
        self.wait(10)

        # Clear updaters after animation
        link1.clear_updaters()
        link2.clear_updaters()
        joint1_dot.clear_updaters()
        joint2_dot.clear_updaters()

############################################################################################################

class NewtonsMethod1D(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-1.5, 3.5, 1],
            x_length=6,
            y_length=4,
            tips=True
        )

        # Functions for Newton's method
        def f(x):
            return x**2 - 1

        def df(x):
            return 2*x

        # Plot the function on our axes.
        function_graph = axes.plot(f, color=BLUE)
        function_label = MathTex("f(x) = x^2 - 1").next_to(axes, UP)

        x0 = 2.0  # Starting guess
        num_iterations = 4

        x_current = x0
        prev_tangent_line = None
        prev_intersection_dot = None
        prev_intersection_label = None
        prev_dashed_line = None
        
        dot = Dot(color=YELLOW).move_to(axes.coords_to_point(x0, 0))

        # Add the axes, function graph, and initial dot to the scene.
        self.play(
            Create(axes),
            Create(function_graph),
            Write(function_label),
            FadeIn(dot, scale=0.5)
        )
        self.wait()

        for i in range(num_iterations):
            ######################################
            # Compute
            ######################################

            # Current x_n
            intersection_dot = Dot(
                axes.coords_to_point(x_current, 0),
                color=MAROON
            )
            intersection_label = MathTex(f"x_{i}").next_to(intersection_dot, DOWN)

            # Current point (x_n, f(x_n))
            fx_val = f(x_current)
            dfx_val = df(x_current)

            # Dashed Line
            dashed_line = DashedLine(
                start=axes.coords_to_point(x_current, 0), 
                end=axes.coords_to_point(x_current, fx_val),
                dash_length=0.1, dashed_ratio=0.5  # Adjusts spacing
            )
            
            # Compute the next iteration:
            # x_{n+1} = x_n - f(x_n)/f'(x_n)
            x_next = x_current - fx_val / dfx_val

            # Create a tangent line at (x_n, f(x_n)).
            # Equation of the tangent line:
            # y - f(x_n) = f'(x_n) * (x - x_n)
            # We'll find two endpoints for a line segment that extends across the axes view.
            x_min, x_max = axes.x_range[0], axes.x_range[1]
            y_min = fx_val + dfx_val * (x_min - x_current)
            y_max = fx_val + dfx_val * (x_max - x_current)
            tangent_line = Line(
                axes.coords_to_point(x_min, y_min),
                axes.coords_to_point(x_max, y_max),
                color=RED
            )

            ######################################
            # Animate
            ######################################
            self.play(FadeIn(intersection_dot), FadeIn(intersection_label))
            if i != 0:
                self.play(FadeOut(prev_tangent_line), FadeOut(prev_intersection_dot), FadeOut(prev_intersection_label), FadeOut(prev_dashed_line))
            move_up_to_new_point = dot.animate.move_to(axes.coords_to_point(x_current, fx_val))
            self.play(move_up_to_new_point, Create(dashed_line))


            tangent_line_anim = Create(tangent_line)
            self.play(tangent_line_anim)
            self.wait(0.5)
            move_down_to_axis = dot.animate.move_to(axes.coords_to_point(x_next, 0))
            self.play(move_down_to_axis)

            prev_tangent_line = tangent_line
            prev_intersection_dot = intersection_dot
            prev_intersection_label = intersection_label
            prev_dashed_line = dashed_line
            
            # Update x_current
            x_current = x_next

        # Finally, hold the scene
        self.wait(2)

############################################################################################################

# Create a coordinate scene
def create_coordinate_frame(self, origin=ORIGIN, axis_length=1.0, axis_thickness=0.05):
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
        x_label = Text("X", color=RED).scale(0.5).next_to(x_axis.get_end(), RIGHT, buff=0.1)
        y_label = Text("Y", color=GREEN).scale(0.5).next_to(y_axis.get_end(), UP, buff=0.1)
        z_label = Text("Z", color=BLUE).scale(0.5).next_to(z_axis.get_end(), OUT, buff=0.1)
        
        # Group all elements
        frame = VGroup(x_axis, y_axis, z_axis, x_label, y_label, z_label)
        return frame

# Add a coordinate frame to the scene
coord_frame = self.create_coordinate_frame(
    origin=np.array([-4, -3, -3]),  # Position in bottom left corner
    axis_length=1.5,
    axis_thickness=0.05
)
self.add(coord_frame)

# Make the text labels face the camera
for label in [coord_frame[3], coord_frame[4], coord_frame[5]]:  # The text labels
    self.add_fixed_orientation_mobjects(label)