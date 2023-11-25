import numpy as np


def normalize(x):
    return x / np.linalg.norm(x)


class Camera:
    def __init__(self):
        self.m_pos = np.array([0.0, 0.0, 0.0])
        self.m_pitch = 0.0
        self.m_yaw = -np.pi/2
        self.m_fov = 90.0

    def GetForward(self):
        return np.array([
            np.cos(self.m_yaw) * np.cos(self.m_pitch),
            np.sin(self.m_pitch),
            np.sin(self.m_yaw) * np.cos(self.m_pitch)
        ])

    def GetRightward(self):
        forward = self.GetForward()
        return normalize(np.array([-forward[2], 0, forward[0]]))

    def GetViewMatrix(self):
        forward = self.GetForward()
        right = normalize(np.array([-forward[2], 0, forward[0]]))
        up = np.cross(right, forward)
        return np.matrix([[*right, -np.dot(right, self.m_pos)],
                          [*up, -np.dot(up, self.m_pos)],
                          [*forward, -np.dot(forward, self.m_pos)],
                          [0, 0, 0, 1]])

    def GetProjectionMatrix(self):
        fov = np.pi * 0.5
        width = 800
        height = 600
        zNear = 0.01
        zFar = 50

        h = np.cos(0.5 * fov) / np.sin(0.5 * fov)
        w = h * height / width
        return np.matrix(np.array([
            [w, 0, 0, 0],
            [0, h, 0, 0],
            [0, 0, zFar / (zFar - zNear), zFar * zNear / (zNear - zFar)],
            [0, 0, 1, 0]]))
