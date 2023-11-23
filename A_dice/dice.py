import OpenGL.GL as GL
import numpy as np
import quaternion


class Dice:
    diceCnt = 0

    def __init__(self):
        self.m_pos = np.array([0.0, 0.0, 0.0])
        self.m_rot = np.quaternion(1, 0, 0, 0)
        self.m_vel = np.array([0.0, 0.0, 0.0])
        self.m_omega = np.array([0.0, 0.0, 0.0])
        self.m_id = Dice.diceCnt
        self.m_colliding = -1
        Dice.diceCnt += 1

    def Draw(self):
        m = np.matrix([[*x, 0] for x in quaternion.as_rotation_matrix(self.m_rot)] + [[0, 0, 0, 1]])
        m[0, 3], m[1, 3], m[2, 3] = self.m_pos[0], self.m_pos[1], self.m_pos[2]
        GL.glUniformMatrix4fv(0, 1, GL.GL_TRUE, m)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
