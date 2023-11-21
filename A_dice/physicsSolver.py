import numpy as np
import quaternion
import dice

diceMass = 1.0
diceMMOI = diceMass / 6.0
diceInverseMMOI = 1.0 / diceMMOI
COR = 0.7


def TestCollisionDiceAndPlane(d: dice.Dice):
    m = quaternion.as_rotation_matrix(d.m_rot).T * 0.5
    p = np.array((
        m[0]+m[1]+m[2],
        m[0]+m[1]-m[2],
        m[0]-m[1]+m[2],
        m[0]-m[1]-m[2],
        -m[0]+m[1]+m[2],
        -m[0]+m[1]-m[2],
        -m[0]-m[1]+m[2],
        -m[0]-m[1]-m[2],
    ))
    mn = p[:, 1].min()
    if mn + d.m_pos[1] < 0:
        c = np.array([x for x in p if x[1] - 1e-4 < mn])
        return True, np.average(c, axis=0) + d.m_pos
    return False, None


def SolveDiceAndPlane(d: dice.Dice, deltaTime):
    d.m_vel[1] -= 0.98 * deltaTime
    d.m_pos += d.m_vel * deltaTime
    rot = d.m_omega * deltaTime
    rotlen = np.linalg.norm(rot)
    if rotlen > 1e-4:
        d.m_rot = np.quaternion(np.cos(rotlen * 0.5), *(rot / rotlen * np.sin(rotlen * 0.5))) * d.m_rot
    col, impact = TestCollisionDiceAndPlane(d)
    if col:
        r1 = impact - d.m_pos
        norm = np.array((0,1,0))
        rot = diceInverseMMOI * np.cross(r1, norm)
        deno = 1.0 / diceMass + np.dot(np.cross(rot, r1), norm)
        J = (COR + 1.0) * np.dot(-d.m_vel - np.cross(d.m_omega, r1), norm) / deno
        d.m_vel += norm * (J / diceMass)
        d.m_omega += rot * J
        d.m_pos[1] -= impact[1]
        d.m_omega *= 0.9
        d.m_vel *= 0.9
