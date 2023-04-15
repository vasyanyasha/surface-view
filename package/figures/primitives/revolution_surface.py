import pyvista as pv
import numpy as np
from package.figures.figure import Figure, FigureTypes


class RevolutionSurface(Figure):
    def __init__(
        self,
        curve,
        direction,
        t_bounce: tuple[float, float],
        uid: str,
        resolution: int = 400,
        **kwargs
    ):
        super().__init__(uid, FigureTypes.REVOLUTION, **kwargs)

        self.__t_bounce = t_bounce
        self.__curve = curve
        self.__direction = direction
        self.__resolution = resolution

    def get_mesh(self):
        t_bounce = self.__t_bounce
        curve = self.__curve
        direction = self.__direction
        resolution = self.__resolution

        t = np.linspace(t_bounce[0], t_bounce[1], resolution)
        theta = np.linspace(0, 2 * np.pi, 180)

        direction = direction / np.linalg.norm(direction)
        
        x = curve[0](t)
        y = curve[1](t)
        z = curve[2](t)
        points_on_curve = np.vstack((x, y, z)).T

        surface_points = []

        for point in points_on_curve:
            plane_points = []
            for angle in theta:
                rotation_matrix = np.array(
                    [
                        [
                            np.cos(angle) + direction[0] ** 2 * (1 - np.cos(angle)),
                            direction[0] * direction[1] * (1 - np.cos(angle))
                            - direction[2] * np.sin(angle),
                            direction[0] * direction[2] * (1 - np.cos(angle))
                            + direction[1] * np.sin(angle),
                        ],
                        [
                            direction[1] * direction[0] * (1 - np.cos(angle))
                            + direction[2] * np.sin(angle),
                            np.cos(angle) + direction[1] ** 2 * (1 - np.cos(angle)),
                            direction[1] * direction[2] * (1 - np.cos(angle))
                            - direction[0] * np.sin(angle),
                        ],
                        [
                            direction[2] * direction[0] * (1 - np.cos(angle))
                            - direction[1] * np.sin(angle),
                            direction[2] * direction[1] * (1 - np.cos(angle))
                            + direction[0] * np.sin(angle),
                            np.cos(angle) + direction[2] ** 2 * (1 - np.cos(angle)),
                        ],
                    ]
                )
                rotated_point = point.dot(rotation_matrix)
                plane_points.append(rotated_point)
            surface_points.append(plane_points)

        surface_points = np.array(surface_points)
        x, y, z = (
            surface_points[:, :, 0],
            surface_points[:, :, 1],
            surface_points[:, :, 2],
        )

        return pv.StructuredGrid(x, y, z)