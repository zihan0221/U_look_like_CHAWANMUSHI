import numpy as np
import quaternion
import dice

diceMass = 1.0
diceMMOI = diceMass / 6.0
diceInverseMMOI = 1.0 / diceMMOI
COR = 0.5


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
        d.m_rot = np.quaternion(np.cos(rotlen * 0.5), * (rot / rotlen * np.sin(rotlen * 0.5))) * d.m_rot
    col, impact = TestCollisionDiceAndPlane(d)
    if col:
        d.m_colliding = -1
        r1 = impact - d.m_pos
        rot = diceInverseMMOI * np.array((-r1[2], 0, r1[0]))
        deno = 1.0 / diceMass + rot[2] * r1[0] - rot[0] * r1[2]
        J = (COR + 1.0) * (-d.m_vel[1] + d.m_omega[0] * r1[2] - d.m_omega[2] * r1[0]) / deno
        d.m_vel[1] += (J / diceMass)
        d.m_omega += rot * J
        d.m_pos[1] -= impact[1]
        d.m_omega *= 0.9
        d.m_vel *= 0.9


def TestCollisionDiceAndDice(a: dice.Dice, b: dice.Dice):
    rota = quaternion.as_rotation_matrix(a.m_rot)
    m = np.matrix([[*x, 0] for x in rota] + [[0, 0, 0, 1]])
    m[0, 3], m[1, 3], m[2, 3] = a.m_pos[0] - b.m_pos[0], a.m_pos[1] - b.m_pos[1], a.m_pos[2] - b.m_pos[2]
    rotb = quaternion.as_rotation_matrix(b.m_rot)
    rotbT = rotb.T
    m = np.matrix([[*x, 0] for x in rotbT] + [[0, 0, 0, 1]]) * m
    p = (m * np.array(((0.5,  0.5,  0.5,  0.5, -0.5, -0.5, -0.5, -0.5),
                       (0.5,  0.5, -0.5, -0.5,  0.5,  0.5, -0.5, -0.5),
                       (0.5, -0.5,  0.5, -0.5,  0.5, -0.5,  0.5, -0.5),
                       (  1,    1,    1,    1,    1,    1,    1,    1)))).T
    edge = np.array(((0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7)))
    c = []
    for i, j in edge:
        p1 = p[i][0, :-1]
        d = p[j][0, :-1] - p1
        m = 1 / d
        n = np.multiply(m, p1)
        k = np.abs(m) * 0.5
        t1 = -n - k
        t2 = -n + k
        tN = t1.max()
        tF = t2.min()
        if tN < tF and tF > 0 and tN < 1:
            ltF = tF
            if tN > 0:
                c.append(p1 + d * tN)
            if tF < 1:
                c.append(p1 + d * tF)
    c = np.array(c)
    if c.size != 0:
        impact = ((np.average(c, axis=0)) @ rotbT)[0]
        if ltF > 1 or c.size < 2:
            d = np.abs(impact).argmax()
            norm = np.zeros(3)
            norm[d] = np.sign(impact[d])
        else:
            s = c[0, 0] + c[1, 0]
            d = c[0, 0] - c[1, 0]
            if np.abs(s[0]) > 0.49:
                if np.abs(s[1]) > 0.49:
                    # [1 1 0]
                    norm = np.array((d[1], -d[0], 0))
                else:
                    # [1 0 1]
                    norm = np.array((-d[2], 0, d[0]))
            else:
                # [0 1 1]
                norm = np.array((0, d[2], -d[1]))
        norm = (norm / np.linalg.norm(norm)) @ rotbT
        if np.dot(norm, a.m_pos - b.m_pos) < 0:
            norm = -norm
        return True, impact + b.m_pos, norm
    return False, None, None


def SolveDiceAndDice(a: dice.Dice, b: dice.Dice, deltaTime):
    col, impact, norm = TestCollisionDiceAndDice(a, b)
    if col:
        if a.m_colliding == b.m_id:
            a.m_pos += norm * deltaTime
            b.m_pos -= norm * deltaTime
            return
        a.m_colliding = b.m_id
        b.m_colliding = a.m_id
        r1 = impact - a.m_pos
        r2 = impact - b.m_pos
        rot1 = (diceInverseMMOI * np.cross(r1, norm))
        rot2 = (diceInverseMMOI * np.cross(r2, norm))
        deno =  1 / diceMass + np.dot(np.cross(rot1, r1), norm) + 1 / diceMass + np.dot(np.cross(rot2, r2), norm)
        J = ((COR + 1) * np.dot(b.m_vel + np.cross(b.m_omega, r2) - a.m_vel - np.cross(a.m_omega, r1),norm) / deno)
        a.m_vel += norm * (J / diceMass)
        b.m_vel -= norm * (J / diceMass)
        a.m_omega += J * rot1
        b.m_omega -= J * rot2
        a.m_omega *= 0.9
        a.m_vel *= 0.9
        b.m_omega *= 0.9
        b.m_vel *= 0.9
    else:
        a.m_colliding = -1
        b.m_colliding = -1



