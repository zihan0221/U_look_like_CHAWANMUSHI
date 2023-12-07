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

    def GetPoint(self):
        w,x,y,z = quaternion.as_float_array(self.m_rot)
        a = np.clip((1.4142135623730950488016887242097 * w) / (2.0 * (w * w + y * y)), -1, 1)
        b = np.sqrt(1 - a * a)
        if np.abs(a*w-b*y - 0.70710678118654752440084436210485) > 1e-2:
            if np.abs(a*w+b*y - 0.70710678118654752440084436210485) < 1e-2:
                b = -b
            else:
                if np.abs(w)<1e-2 and np.abs(a)>0.9:
                    return 5
                else :
                    return 6
        rot = np.quaternion(a, 0, b, 0) * self.m_rot
        w,x,y,z = quaternion.as_float_array(rot)
        if x > 0.5:
            return 1
        elif x < -0.5:
            return 3
        elif z > 0.5:
            return 2
        elif z < -0.5:
            return 4
        else:
            return 5
