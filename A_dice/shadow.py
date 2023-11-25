import OpenGL.GL as GL
import numpy as np


SHADOW_MAP_SIZE = 1024

def CreateDepthTexture(num):
    tex = GL.glGenTextures(num)
    if type(tex) is not np.ndarray:
        tex = np.array((tex,))
    for t in tex:
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, t)
        for i in range(6):
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL.GL_DEPTH_COMPONENT, SHADOW_MAP_SIZE, SHADOW_MAP_SIZE, 0, GL.GL_DEPTH_COMPONENT, GL.GL_FLOAT, None)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST);
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST);
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP);
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP);
    return tex


def CreateShadowMapTexture(num):
    tex = GL.glGenTextures(num)
    if type(tex) is not np.ndarray:
        tex = np.array((tex,))
    for t in tex:
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, t)
        for i in range(6):
            GL.glTexImage2D(GL.GL_TEXTURE_CUBE_MAP_POSITIVE_X + i, 0, GL.GL_R16F, SHADOW_MAP_SIZE, SHADOW_MAP_SIZE, 0, GL.GL_RED, GL.GL_FLOAT, None)
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST);
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST);
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_S, GL.GL_CLAMP);
        GL.glTexParameteri(GL.GL_TEXTURE_CUBE_MAP, GL.GL_TEXTURE_WRAP_T, GL.GL_CLAMP);
    return tex


h = np.cos(np.pi * 0.25) / np.sin(np.pi * 0.25)
w = h
SHADOW_MAP_NEAR = 0.1
SHADOW_MAP_FAR = 20
PROJ_MATRIX = np.matrix(np.array([
    [w, 0, 0, 0],
    [0, h, 0, 0],
    [0, 0, SHADOW_MAP_FAR / (SHADOW_MAP_FAR - SHADOW_MAP_NEAR), SHADOW_MAP_FAR * SHADOW_MAP_NEAR / (SHADOW_MAP_NEAR - SHADOW_MAP_FAR)],
    [0, 0, 1, 0]]))

def LookAt(pos, forward, up):
    F = -forward
    R = np.cross(F, up)
    return np.matrix(((*(-R), np.dot(R, pos)),
                      (*(-up), np.dot(up,pos)),
                      (*(-F), np.dot(F,pos)),
                      (0,0,0,1)))

def SetupShadow(depthTex, shadowTex, lightPos):
    GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_DEPTH_ATTACHMENT, depthTex, 0)
    GL.glFramebufferTexture(GL.GL_FRAMEBUFFER, GL.GL_COLOR_ATTACHMENT0, shadowTex, 0)
    GL.glDrawBuffer(GL.GL_COLOR_ATTACHMENT0)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    trans = np.array((
        PROJ_MATRIX * LookAt(lightPos, np.array((-1,0,0)), np.array((0,-1,0))),
        PROJ_MATRIX * LookAt(lightPos, np.array((1,0,0)), np.array((0,-1,0))),
        PROJ_MATRIX * LookAt(lightPos, np.array((0,-1,0)), np.array((0,0,1))),
        PROJ_MATRIX * LookAt(lightPos, np.array((0,1,0)), np.array((0,0,1))),
        PROJ_MATRIX * LookAt(lightPos, np.array((0,0,-1)), np.array((0,-1,0))),
        PROJ_MATRIX * LookAt(lightPos, np.array((0,0,1)), np.array((0,-1,0))),
    ))
    GL.glUniformMatrix4fv(1, 6, GL.GL_TRUE, trans)
    GL.glUniform3fv(7, 1, lightPos)


def BindShadowMapTexture(shadowTex):
    for i in range(shadowTex.size):
        GL.glActiveTexture(GL.GL_TEXTURE1 + i)
        GL.glBindTexture(GL.GL_TEXTURE_CUBE_MAP, shadowTex[i])
        GL.glUniform1i(5 + i, i + 1)
