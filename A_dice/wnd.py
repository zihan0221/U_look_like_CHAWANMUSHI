import numpy as np
import quaternion
import random
import OpenGL.GLUT as GLUT
import OpenGL.GL as GL
import camera
import shaderProgram
import dice
import physicsSolver
import shadow


class Wnd:
    def __init__(self):
        GLUT.glutInit()
        GLUT.glutInitDisplayMode(
            GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH)
        GLUT.glutInitWindowSize(800, 600)
        GLUT.glutCreateWindow(b"Roll a Dice!")
        GLUT.glutDisplayFunc(self.__DisplayFunc)
        GLUT.glutKeyboardFunc(self.__KeyboardFunc)
        GL.glClearColor(0, 0, 0, 1)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glEnable(GL.GL_DEPTH_TEST)
        self.m_camera = camera.Camera()
        self.__CreateObject()
        self.__CreateShader()
        self.__Redraw(0)
        GLUT.glutMainLoop()

    def __CreateShader(self):
        self.m_diceShader = shaderProgram.CreateDiceShader()
        GL.glUniformMatrix4fv(2, 1, GL.GL_TRUE, self.m_camera.GetProjectionMatrix())
        self.m_planeShader = shaderProgram.CreatePlaneShader()
        GL.glUniformMatrix4fv(2, 1, GL.GL_TRUE, self.m_camera.GetProjectionMatrix())
        self.m_depthTextures = shadow.CreateDepthTexture(len(shaderProgram.lights))
        self.m_shadowMapTextures = shadow.CreateShadowMapTexture(len(shaderProgram.lights))
        self.m_framebuffer = GL.glGenFramebuffers(1)
        self.m_shadowShader = shaderProgram.CreateShadowShader()
        self.timer = 0

    def RandomizeDices(self):
        for i in range(self.m_diceCnt):
            flag = True
            while flag:
                flag = False
                self.m_dices[i].m_pos = np.array((random.uniform(-5,5), random.uniform(1,8), random.uniform(-5,5)))
                self.m_dices[i].m_rot = quaternion.from_euler_angles((random.uniform(0, np.pi*2), random.uniform(0, np.pi * 2), random.uniform(0,np.pi * 2)))
                for j in range(0, i):
                    col, _, _ = physicsSolver.TestCollisionDiceAndDice(self.m_dices[i], self.m_dices[j])
                    if col:
                        flag = True
                        break
                    col, _, _ = physicsSolver.TestCollisionDiceAndDice(self.m_dices[j], self.m_dices[i])
                    if col:
                        flag = True
                        break

    def __CreateObject(self):
        self.m_dices = [dice.Dice() for _ in range(6)]
        self.m_diceCnt = 6
        self.RandomizeDices()

    def __Redraw(self, t):
        GLUT.glutPostRedisplay()
        GLUT.glutTimerFunc(16, self.__Redraw, 0)

    def __DisplayFunc(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        for i in range(self.m_diceCnt):
            physicsSolver.SolveDiceAndPlane(self.m_dices[i], 0.06)
        for i in range(self.m_diceCnt):
            for j in range(i + 1, self.m_diceCnt):
                physicsSolver.SolveDiceAndDice(self.m_dices[i], self.m_dices[j], 0.06)
                physicsSolver.SolveDiceAndDice(self.m_dices[j], self.m_dices[i], 0.06)
        # Draw shadow
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.m_framebuffer)
        GL.glUseProgram(self.m_shadowShader)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        GLUT.glutSwapBuffers()

    def __KeyboardFunc(self, c, x, y):
        if c == b'a':
            right = self.m_camera.GetRightward()
            self.m_camera.m_pos -= 0.1 * right
        elif c == b'd':
            right = self.m_camera.GetRightward()
            self.m_camera.m_pos += 0.1 * right
        elif c == b'w':
            forward = self.m_camera.GetForward()
            self.m_camera.m_pos += 0.1 * forward
        elif c == b's':
            forward = self.m_camera.GetForward()
            self.m_camera.m_pos -= 0.1 * forward
        elif c == b'k':
            self.m_camera.m_pitch += 0.1
        elif c == b'j':
            self.m_camera.m_pitch -= 0.1
        elif c == b'h':
            self.m_camera.m_yaw -= 0.1
        elif c == b'l':
            self.m_camera.m_yaw += 0.1
        elif c == b'e':
            self.m_camera.m_pos[1] += 0.1
        elif c == b'q':
            self.m_camera.m_pos[1] -= 0.1
        elif c == b'p':
            self.RandomizeDices()
        elif c == b'm':
            self.m_dices[0].m_pos[2]+=0.1
        elif c == b'n':
            self.m_dices[0].m_pos[2]-=0.1
        elif c == b'b':
            self.m_dices[1].m_pos=np.array((0.0,1.0,0.0))
