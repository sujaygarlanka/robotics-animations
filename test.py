# manimgl code (Manim Community “.import” syntax differs slightly—this is for the older ManimGL/3b1b version)

from manimlib import *
import numpy as np
from collections import defaultdict, deque

manim_config.camera.background_color = "#CCCCCC"
# manim_config.camera.background_color = "#000000"
# manim_config.frame.center_point = np.array([-5, -5, 0])
# manim_config.camera.frame_height = 10
class CellBoundary():
    def __init__(self, start, end_y):
        self.start = start
        self.end = np.array([start[0], end_y, 0])
        self.center = np.array([self.start[0], (self.start[1] + self.end[1])/2, 0])

class TrapezoidDecomp(Scene):
    def construct(self):
        """
        Example: Create multiple gray polygons and optional vertical dashed lines
        to mimic 'background' shapes. Adjust coordinates and styling as needed.
        """
        edges = self._create_background()
        line = self._create_sweep_line()
        intersection_dot = self._create_dot()
        cell_boundaries = defaultdict(list)
        prev_cbs = [None]

        self.CUSTOM_BLUE = "#0000FF"
        self.CUSTOM_GREEN = "#01FF00"
        self.CUSTOM_RED = "#FF0000"

        # Move the line
        self.play(line.animate.move_to(self._convert_point_to_sweep_point(edges[0].start)), run_time=0.5)
        intersection_dot.move_to(edges[0].start)
        self.play(FadeIn(intersection_dot), run_time=0.5)

        # Birth
        self._add_edge_to_L(edges[0], edges[-5])

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[1].start)

        # Continue
        self._remove_edge_from_L(edges[0])
        # self.wait(1.0)
        self._add_edge_to_L(edges[1])
        cb = CellBoundary(edges[1].start, edges[14].end[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs = [cb]
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[2].start)

        # Continue
        self._remove_edge_from_L(edges[1])
        # self.wait(1.0)
        self._add_edge_to_L(edges[2])
        cb = CellBoundary(edges[2].start, edges[14].end[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs = [cb]
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[15].start)

        # Split
        self._add_edge_to_L(edges[15], edges[18])
        end_y = (edges[2].start[1] + edges[2].end[1]) / 2
        cb = CellBoundary(edges[15].start, end_y)
        cb2 = CellBoundary(edges[15].start, edges[14].end[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        cell_boundaries[prev_cbs[0]].append(cb2)
        prev_cbs = [cb, cb2]
        self._draw_cell_boundary(cb, cb2)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[3].start)

        # Continue        
        self._remove_edge_from_L(edges[2])
        # self.wait(1.0)
        self._add_edge_to_L(edges[3])
        cb = CellBoundary(edges[3].start, 0)
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs[0] = cb
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[16].start)

        # Continue
        self._remove_edge_from_L(edges[15])
        # self.wait(1.0)
        self._add_edge_to_L(edges[16])
        cb = CellBoundary(edges[16].start, edges[3].start[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs[0] = cb
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[18].start)

        # Continue
        self._remove_edge_from_L(edges[18])
        # self.wait(1.0)
        self._add_edge_to_L(edges[17])
        cb = CellBoundary(edges[18].start, edges[14].end[1])
        cell_boundaries[prev_cbs[1]].append(cb)
        prev_cbs[1] = cb
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[17].start)

        # Continue
        self._remove_edge_from_L(edges[16], edges[17])
        # self.wait(1.0)
        cb = CellBoundary(edges[17].start, edges[3].start[1])
        cb2 = CellBoundary(edges[17].start, edges[14].end[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        cell_boundaries[prev_cbs[1]].append(cb2)
        prev_cbs = [cb, cb2]
        self._draw_cell_boundary(cb, cb2)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[4].start)

        # Continue
        self._remove_edge_from_L(edges[3])
        # self.wait(1.0)
        self._add_edge_to_L(edges[4])
        cb = CellBoundary(edges[4].start, edges[14].start[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        cell_boundaries[prev_cbs[1]].append(cb)
        prev_cbs = [cb]
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[14].start)

        # Continue
        self._remove_edge_from_L(edges[14])
        # self.wait(1.0)
        self._add_edge_to_L(edges[13])
        cb = CellBoundary(edges[14].start, edges[11].start[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs = [prev_cbs[0], cb]
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[11].start)

        # Split
        self._add_edge_to_L(edges[10], edges[11])

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[10].start)

        # Continue
        self._remove_edge_from_L(edges[10])
        # self.wait(1.0)
        self._add_edge_to_L(edges[9])
        end_y = (edges[4].start[1] + edges[4].end[1]) / 2
        cb = CellBoundary(edges[10].start, end_y)
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs[0] = cb
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[12].start)

        # Continue
        self._remove_edge_from_L(edges[11])
        # self.wait(1.0)
        self._add_edge_to_L(edges[12])
        cb = CellBoundary(edges[10].start, edges[4].start[1])
        cell_boundaries[prev_cbs[1]].append(cb)
        prev_cbs[1] = cb
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[5].start)

        # Continue
        self._remove_edge_from_L(edges[4])
        # self.wait(1.0)
        self._add_edge_to_L(edges[5])
        cb = CellBoundary(edges[5].start, edges[9].end[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs[0] = cb
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[13].start)

        # Merge
        self._remove_edge_from_L(edges[12], edges[13])

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[9].start)

        # Continue
        self._remove_edge_from_L(edges[9])
        # self.wait(1.0)
        self._add_edge_to_L(edges[8])
        cb = CellBoundary(edges[9].start, edges[5].end[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs = [cb]
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[8].start)

        # Continue
        self._remove_edge_from_L(edges[8])
        # self.wait(1.0)
        self._add_edge_to_L(edges[7])
        cb = CellBoundary(edges[8].start, edges[5].end[1])
        cell_boundaries[prev_cbs[0]].append(cb)
        prev_cbs = [cb]
        self._draw_cell_boundary(cb)

        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[7].start)

        # Continue
        self._remove_edge_from_L(edges[7])
        # self.wait(1.0)
        
        # Move the line to the next edge
        self._move_sweep_line(intersection_dot, line, edges[6].start)
        self._remove_edge_from_L(edges[5])

        self._create_graph(cell_boundaries)
        # from IPython import embed; embed()

        # Optionally animate their creation
        # self.play(ShowCreation(outer_polygon), ShowCreation(inner_polygon), ShowCreation(dashed_lines))
        # self.wait()

    def _create_graph(self, cell_boundaries):
        # Create a graph with vertices and edges
        queue = deque()
        queue.extend(cell_boundaries[None])
        while queue:
            node = queue.popleft()
            node_dot = Dot(node.center, radius=0.15, fill_color=RED, fill_opacity=1)
            node_dot.set_z_index(300)
            self.play(ShowCreation(node_dot))
            for cb in cell_boundaries[node]:
                # Add lines to represent the edges
                line = Line(node.center, cb.center, color=RED, stroke_width=6)
                line.set_z_index(300)
                self.play(ShowCreation(line))
                
            # Add the neighbors to the queue for further processing
            queue.extend(cell_boundaries[node])
        

    def _move_sweep_line(self, dot, line, point):
        self.play(FadeOut(dot), run_time=0.5)
        self.play(line.animate.move_to(self._convert_point_to_sweep_point(point)), run_time=0.5)
        dot.move_to(point)
        self.play(FadeIn(dot), run_time=0.5)

    def _add_edge_to_L(self, *edges):
        self.play(*[self._highlight_edge(e, self.CUSTOM_GREEN) for e in edges], run_time=0.5)
        self.play(*[self._highlight_edge(e, self.CUSTOM_BLUE) for e in edges], run_time=0.5)
    
    def _remove_edge_from_L(self, *edges):
        self.play(*[self._highlight_edge(e, self.CUSTOM_RED) for e in edges], run_time=0.5)
        self.play(*[self._highlight_edge(e, BLACK) for e in edges], run_time=0.5)

    def _highlight_edge(self, edge, color):
       return ApplyMethod(edge.set_color, color)

    def _create_background(self):
        outline_points = [
            np.array([-6.5, -3.5, 0]),
            np.array([-6.0, 3.5, 0]),
            # Dip in the top
            np.array([-2.5, 3.5, 0]),
            np.array([-1.5, 2.0, 0]),
            np.array([1.5, 2.0, 0]),
            np.array([2.5, 3.5, 0]),
            ######
            np.array([6,  3.5, 0]),
            np.array([6,  -3.5, 0]),
            # Jutting structure from floor
            np.array([5, -3.5, 0]),
            np.array([4,  -1.0, 0]),
            np.array([2,  -1.0, 0]),
            np.array([2,  -1.5, 0]),
            np.array([2.5,  -1.5, 0]),
            np.array([3.0,  -2.5, 0]),
            np.array([2, -3.5, 0]),
            ######
        ]

        # Middle structure
        inner_points = [
            np.array([-2, -1, 0]),
            np.array([-1, 0.75, 0]),
            np.array([0.5, 0.75, 0]),
            np.array([0, -1, 0]),
        ]

        outer_polygon = Polygon(
            *outline_points,
            fill_color=WHITE,
            fill_opacity=1,    # Opaque fill
            stroke_color=BLACK,
        )

        inner_polygon = Polygon(
            *inner_points,
            fill_color="#CCCCCC",  # Light gray
            fill_opacity=1,  # Semi-transparent fill
            stroke_color=BLACK,
        )
        
        self.play(FadeIn(outer_polygon))
        self.play(FadeIn(inner_polygon))

        def _create_edge(edge, color):
            hEdge = Line(
                    start=edge[0],
                    end=edge[1],
                    stroke_width=4,
                    color=color,
                    stroke_opacity=1,
                )
            self.add(hEdge)
            return hEdge
        
        # Create an array of edges
        edges = [
            _create_edge(e, color=BLACK)
            for e in zip(outline_points, outline_points[1:] + [outline_points[0]])
        ]

        edges += [
            _create_edge(e, color=BLACK)
            for e in zip(inner_points, inner_points[1:] + [inner_points[0]])
        ]

        return edges

        # self.add(outer_polygon, inner_polygon)

    def _draw_cell_boundary(self, *cell_boundary):
        for cb in cell_boundary:
            # Convert the point to a 3D point
            line = DashedLine(
                start=cb.start,
                end=cb.end,
                dash_length=0.2,
                stroke_width=4,
                color=BLACK
            )
            line.set_z_index(100)
            self.add(line)

    def _create_dot(self):
        dot = Dot(
            point=np.array([0, 0, 0]),
            radius=0.15,
            fill_color="#FFFF00",
            stroke_color=BLACK,
            stroke_width=4,
            fill_opacity=1,
        )
        dot.set_z_index(200)
        return dot
    
    def _convert_point_to_sweep_point(self, point):
        # Convert the point to a 3D point
        point_3d = np.array([point[0], 0, 0])
        return point_3d

    def _create_sweep_line(self):
        # print(self.camera.frame.get_width())
        frame_width = self.camera.frame.get_width()
        frame_height = self.camera.frame.get_height()
        left_boundary = -1 * frame_width / 2 - 0.5
        line = DashedLine(
            start=np.array([left_boundary, -frame_height / 2, 0]),
            end=np.array([left_boundary, frame_height / 2, 0]),
            dash_length=0.2,
            stroke_width=4,
            color=BLACK
        )
        line.set_z_index(100)
        self.play(FadeIn(line))
        return line