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
