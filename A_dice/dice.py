import OpenGL.GL as GL
import numpy as np
import quaternion


class Dice:
    diceCnt = 0
    posQueueSize = 5

    def __init__(self):
        self.m_pos = np.array([0.0, 0.0, 0.0])
        self.m_rot = np.quaternion(1, 0, 0, 0)
        self.m_vel = np.array([0.0, 0.0, 0.0])
        self.m_omega = np.array([0.0, 0.0, 0.0])
        self.m_id = Dice.diceCnt
        self.m_colliding = -1
        Dice.diceCnt += 1
        self.m_queueNxt = 0
        self.m_posQueue = np.array([np.array([0.0, 0.0, 0.0]) for _ in range(Dice.posQueueSize)])
        self.m_avgPos = np.array((0.0, 0.0, 0.0))
        self.m_rotQueue = np.array([np.quaternion(1.0, 0.0, 0.0, 0.0) for _ in range(Dice.posQueueSize)])
        self.m_avgRot = np.quaternion(1.0, 0.0, 0.0, 0.0)

    def Draw(self):
        m = np.matrix([[*x, 0] for x in quaternion.as_rotation_matrix(self.m_avgRot)] + [[0, 0, 0, 1]])
        m[0, 3], m[1, 3], m[2, 3] = self.m_avgPos[0], self.m_avgPos[1], self.m_avgPos[2]
        GL.glUniformMatrix4fv(0, 1, GL.GL_TRUE, m)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
