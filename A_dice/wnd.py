import numpy as np
from random import *
import time
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
        self.now_sum=[]
        self.score=0
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
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        self.m_camera = camera.Camera()
        self.m_camera.m_pos=np.array(np.array((0.60108362,2,-0.36730854)))
        self.m_camera.m_yaw=3.1415926
        self.m_camera.m_pitch=-0.5
        self.__CreateObject()
        self.__CreateShader()
        self.__Redraw(0)
        self.__CurrentScene = self.DrawMenu
        self.__CurrentKeyboard = self.MenuKeyboard
        GLUT.glutMainLoop()

    def __CreateShader(self):
        self.m_diceShader = shaderProgram.CreateDiceShader()
        GL.glUniformMatrix4fv(2, 1, GL.GL_TRUE, self.m_camera.GetProjectionMatrix())
        self.m_alphabatShader = shaderProgram.CreateAlphabat()
        self.m_ACShader = shaderProgram.CreateACShader()
        self.m_WAShader = shaderProgram.CreateWAShader()
        self.m_planeShader = shaderProgram.CreatePlaneShader()
        GL.glUniformMatrix4fv(2, 1, GL.GL_TRUE, self.m_camera.GetProjectionMatrix())
        self.m_depthTextures = shadow.CreateDepthTexture(len(shaderProgram.lights))
        self.m_shadowMapTextures = shadow.CreateShadowMapTexture(len(shaderProgram.lights))
        self.m_framebuffer = GL.glGenFramebuffers(1)
        self.m_shadowShader = shaderProgram.CreateShadowShader()
        self.m_skyboxShader = shaderProgram.CreateSkyboxShader()
        GL.glUniformMatrix4fv(2, 1, GL.GL_TRUE, self.m_camera.GetProjectionMatrix())
        self.timer = 0
    def PrintText(self,string,xx=0,yy=0,size=1,color=(0,0,0)):
        for i in range(len(string)):
            GL.glUniform1i(1,ord(string[i]))
            GL.glUniform2f(3,xx,yy)
            GL.glUniform1f(4,size)
            GL.glUniform3fv(5,1,color)
            GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
            xx+=0.03*(size)

    def PrintAC(self,xx=0,yy=0,size=1):
        GL.glUniform2f(3,xx,yy)
        GL.glUniform1f(4,size)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
    
    def PrintWA(self,xx=0,yy=0,size=1):
        GL.glUniform2f(3,xx,yy)
        GL.glUniform1f(4,size)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)

    def RandomizeDices(self):
        self.m_diceCnt=randint(1,6)
        for i in range(self.m_diceCnt):
            flag = True
            self.m_dices[i].m_omega = np.array([0.0, 0.0, 0.0])
            self.m_dices[i].m_vel = np.array([0.0, 0.0, 0.0])
            while flag:
                flag = False
                self.m_dices[i].m_pos = np.array((random.uniform(-5,5), random.uniform(6,8), random.uniform(-5,5)))
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
        self.m_diceCnt = randint(1,6)
        self.RandomizeDices()

    def __Redraw(self, t):
        GLUT.glutPostRedisplay()
        GLUT.glutTimerFunc(16, self.__Redraw, 0)

    def DrawMenu(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        theta = time.time() * 0.2
        c = np.cos(theta)
        s = np.sin(theta)
        self.m_camera.m_pos[0] = 8 * c
        self.m_camera.m_pos[2] = 8 * s
        self.m_camera.m_yaw = theta + 3.1415926
        for i in range(self.m_diceCnt):
            physicsSolver.SolveDiceAndPlane(self.m_dices[i], 0.06)
        for i in range(self.m_diceCnt):
            for j in range(i + 1, self.m_diceCnt):
                physicsSolver.SolveDiceAndDice(self.m_dices[i], self.m_dices[j], 0.06)
                physicsSolver.SolveDiceAndDice(self.m_dices[j], self.m_dices[i], 0.06)
        # Draw shadow
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.m_framebuffer)
        GL.glUseProgram(self.m_shadowShader)
        GL.glDisable(GL.GL_BLEND)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glEnable(GL.GL_BLEND)
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        self.target=0
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)#plane
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        # Draw Skybox
        GL.glUseProgram(self.m_skyboxShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        # Draw Text
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_alphabatShader)
        ss = 4 + 0.5 * np.sin(time.time() * 2)
        self.PrintText("Dice Math !", -ss/11 - 0.25 , 0.8, ss, (1,1,0))
        self.PrintText("[Space] to roll dices!",-0.5,-0.4,1.5)
        self.PrintText("[H] to see the rule!",-0.45,-0.5,1.5)
        self.PrintText("[Enter] to start!",-0.4,-0.6,1.5)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GLUT.glutSwapBuffers()

    def DrawGame(self):
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
        GL.glDisable(GL.GL_BLEND)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glEnable(GL.GL_BLEND)
        
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        self.target=0
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)#plane
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        # Draw Skybox
        GL.glUseProgram(self.m_skyboxShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        # Draw Text
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_alphabatShader)
        sum=str(b''.join(self.now_sum),'utf-8')
        self.PrintText(f"Enter the sum :{sum}",-1,-1+0.1,1.0)
        self.PrintText(f"{max(30-max(int(time.time())-int(self.begin_time),0),0)}",-0.1,1.0,2.0)
        self.PrintText(f"Score:{self.score}",0.3,1.0,2.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GLUT.glutSwapBuffers()
        if max(30-max(int(time.time())-int(self.begin_time),0),-1)==-1:
            self.__CurrentScene = self.EndGame
            self.__CurrentKeyboard = self.EndGameKeyboard
            self.m_camera.m_pos=np.array((0.60108362,12.07439748,-0.36730854))
            self.m_camera.m_pitch=-1.6000000000000003
            self.m_camera.m_yaw=-1.4707963267948965

    def EndGame(self):
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
        GL.glDisable(GL.GL_BLEND)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glEnable(GL.GL_BLEND)
        
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        self.target=0
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)#plane
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        # Draw Skybox
        GL.glUseProgram(self.m_skyboxShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        # Draw Text
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_alphabatShader)
        self.PrintText(f"Your score:{self.score}",-0.8,0.5,4.2)
        self.PrintText("[M] to go back to menu!",-0.5,-0.4,1.5)
        self.PrintText("[R] to replay!",-0.45,-0.5,1.5)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GLUT.glutSwapBuffers()

    def EndGameKeyboard(self, c):
        if c==b'r':
            self.score=0
            self.begin_time=time.time()
            self.__CurrentScene=self.DrawLoadGame
            self.__CurrentKeyboard=self.DoNothingKeyboard
            self.m_camera.m_pos=np.array((9.66514424,3.33536864,1.41968903))
            self.m_camera.m_pitch=-2.7755575615628914e-17
            self.m_camera.m_yaw=-3.070796326794898
            self.RandomizeDices()
        elif c==b'm':
            self.score=0
            self.begin_time=time.time()
            self.__CurrentScene=self.DrawMenu
            self.__CurrentKeyboard=self.MenuKeyboard
            self.m_camera.m_pos=np.array((9.66514424,3.33536864,1.41968903))
            self.m_camera.m_pitch=-2.7755575615628914e-17
            self.m_camera.m_yaw=-3.070796326794898
            self.RandomizeDices()
    
    def DrawRule(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        theta = time.time() * 0.2
        c = np.cos(theta)
        s = np.sin(theta)
        self.m_camera.m_pos[0] = 8 * c
        self.m_camera.m_pos[2] = 8 * s
        self.m_camera.m_yaw = theta + 3.1415926
        for i in range(self.m_diceCnt):
            physicsSolver.SolveDiceAndPlane(self.m_dices[i], 0.06)
        for i in range(self.m_diceCnt):
            for j in range(i + 1, self.m_diceCnt):
                physicsSolver.SolveDiceAndDice(self.m_dices[i], self.m_dices[j], 0.06)
                physicsSolver.SolveDiceAndDice(self.m_dices[j], self.m_dices[i], 0.06)
        # Draw shadow
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.m_framebuffer)
        GL.glUseProgram(self.m_shadowShader)
        GL.glDisable(GL.GL_BLEND)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glEnable(GL.GL_BLEND)
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        self.target=0
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)#plane
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        # Draw Skybox
        GL.glUseProgram(self.m_skyboxShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        # Draw Text
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_alphabatShader)
        ss = 4 + 0.5 * np.sin(time.time() * 2)
        self.PrintText("Dice Math !", -ss/11 - 0.25 , 0.8, ss, (1,1,0))
        self.PrintText("Add up the sides of all the dice displayed on the screen.",-0.95,-0.05,1.1)
        self.PrintText("You have 30 seconds to answer as many as possible.",-0.85,-0.2,1.1)
        self.PrintText("You get 4 points for each correct answer.",-0.7,-0.35,1.1)
        self.PrintText("You lose 1 point for each incorrect answer.",-0.73,-0.5,1.1)
        self.PrintText("[H] return menu!",-0.3,-0.65,1.1)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GLUT.glutSwapBuffers()

    def DrawLoadGame(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        theta = time.time() * 0.2
        c = np.cos(theta)
        s = np.sin(theta)
        self.m_camera.m_pos[0] = 8 * c
        self.m_camera.m_pos[2] = 8 * s
        self.m_camera.m_yaw = theta + 3.1415926
        for i in range(self.m_diceCnt):
            physicsSolver.SolveDiceAndPlane(self.m_dices[i], 0.06)
        for i in range(self.m_diceCnt):
            for j in range(i + 1, self.m_diceCnt):
                physicsSolver.SolveDiceAndDice(self.m_dices[i], self.m_dices[j], 0.06)
                physicsSolver.SolveDiceAndDice(self.m_dices[j], self.m_dices[i], 0.06)
        # Draw shadow
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, self.m_framebuffer)
        GL.glUseProgram(self.m_shadowShader)
        GL.glDisable(GL.GL_BLEND)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glEnable(GL.GL_BLEND)
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        self.target=0
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)#plane
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        # Draw Skybox
        GL.glUseProgram(self.m_skyboxShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        # Draw Text
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_alphabatShader)
        ss = 4 + 0.5 * np.sin(time.time() * 2)
        self.PrintText("Dice Math !", -ss/11 - 0.25 , 0.8, ss, (1,1,0))
        self.PrintText(f"{max(3-max(int(time.time())-int(self.begin_time),0),0)}",-0.3,0.3,10.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GLUT.glutSwapBuffers()
        if max(3-max(int(time.time())-int(self.begin_time),0),0)==0:
            self.__CurrentScene = self.DrawGame
            self.__CurrentKeyboard = self.GameKeyboard
            self.m_camera.m_pos=np.array((0.60108362,12.07439748,-0.36730854))
            self.m_camera.m_pitch=-1.6000000000000003
            self.m_camera.m_yaw=-1.4707963267948965
            self.begin_time=time.time()

    def DrawAC(self):
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
        GL.glDisable(GL.GL_BLEND)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glEnable(GL.GL_BLEND)
        
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        self.target=0
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)#plane
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        # Draw Skybox
        GL.glUseProgram(self.m_skyboxShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        # Draw Text
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_alphabatShader)
        sum=str(b''.join(self.now_sum),'utf-8')
        self.PrintText(f"Enter the sum :{sum}",-1,-1+0.1,1.0)
        self.PrintText(f"{max(30-max(int(time.time())-int(self.begin_time),0),0)}",-0.1,1.0,2.0)
        self.PrintText("Correct:D",-0.7,0.5,5.0,(0,256,0))
        self.PrintText(f"Score:{self.score}",0.3,1.0,2.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        #Draw AC.png
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_ACShader)
        self.PrintAC(-0.4,0.2,15.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GLUT.glutSwapBuffers()
        if max(2-max(int(time.time())-int(self.pre_time),0),0)==0:
            self.__CurrentScene = self.DrawGame
            self.__CurrentKeyboard = self.GameKeyboard
            self.m_camera.m_pos=np.array((0.60108362,12.07439748,-0.36730854))
            self.m_camera.m_pitch=-1.6000000000000003
            self.m_camera.m_yaw=-1.4707963267948965

    def DrawWA(self):
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
        GL.glDisable(GL.GL_BLEND)
        GL.glViewport(0,0,shadow.SHADOW_MAP_SIZE,shadow.SHADOW_MAP_SIZE)
        for i in range(self.m_depthTextures.size):
            shadow.SetupShadow(self.m_depthTextures[i], self.m_shadowMapTextures[i], shaderProgram.lights[i])
            for j in range(self.m_diceCnt):
                self.m_dices[j].Draw()
        GL.glBindFramebuffer(GL.GL_FRAMEBUFFER, 0)
        GL.glEnable(GL.GL_BLEND)
        
        GL.glViewport(0,0,800,600)
        viewMatrix = self.m_camera.GetViewMatrix()
        # Draw Dice
        self.target=0
        GL.glUseProgram(self.m_diceShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        for i in range(self.m_diceCnt):
            self.m_dices[i].Draw()
        # Draw Plane
        GL.glUseProgram(self.m_planeShader)
        shadow.BindShadowMapTexture(self.m_shadowMapTextures)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)#plane
        GL.glUniform3fv(4, 1, self.m_camera.m_pos)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 6)
        # Draw Skybox
        GL.glUseProgram(self.m_skyboxShader)
        GL.glUniformMatrix4fv(1, 1, GL.GL_TRUE, viewMatrix)
        # Draw Text
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, 36)
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_alphabatShader)
        sum=str(b''.join(self.now_sum),'utf-8')
        self.PrintText(f"Enter the sum :{sum}",-1,-1+0.1,1.0)
        self.PrintText(f"{max(30-max(int(time.time())-int(self.begin_time),0),0)}",-0.1,1.0,2.0)
        self.PrintText("Incorrect:(",-0.8,0.5,5.0,(256,0,0))
        self.PrintText(f"Score:{self.score}",0.3,1.0,2.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        #Draw WA.png
        GL.glDisable(GL.GL_DEPTH_TEST)
        GL.glUseProgram(self.m_WAShader)
        self.PrintWA(-0.4,0.2,15.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GLUT.glutSwapBuffers()
        if max(2-max(int(time.time())-int(self.pre_time),0),0)==0:
            self.__CurrentScene = self.DrawGame
            self.__CurrentKeyboard = self.GameKeyboard
            self.m_camera.m_pos=np.array((0.60108362,12.07439748,-0.36730854))
            self.m_camera.m_pitch=-1.6000000000000003
            self.m_camera.m_yaw=-1.4707963267948965


    def __DisplayFunc(self):
        self.__CurrentScene()

    def MenuKeyboard(self, c):
        if c == b' ':
            self.RandomizeDices()
        elif c == b'\r':
            self.begin_time=time.time()
            self.__CurrentScene = self.DrawLoadGame
            self.__CurrentKeyboard = self.DoNothingKeyboard
            self.RandomizeDices()
        elif c == b'h':
            self.__CurrentScene=self.DrawRule
            self.__CurrentKeyboard=self.RuleKeyboard
    
    def RuleKeyboard(self, c):
        if c==b'h':
            self.begin_time=time.time()
            self.__CurrentScene=self.DrawMenu
            self.__CurrentKeyboard=self.MenuKeyboard

    def DoNothingKeyboard(self,c):
        print("Do nothing.")
    
    def GameKeyboard(self, c):
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
            self.m_dices[0].m_rot = quaternion.from_euler_angles(0,0.1,0) * self.m_dices[0].m_rot
        elif c == b'n':
            self.m_dices[0].m_pos[2]-=0.1
        elif c == b'b':
            self.m_dices[1].m_pos=np.array((0.0,1.0,0.0))
        elif c == b'i': #取得當前camera資訊
            print(self.m_camera.m_pos)
            print(self.m_camera.m_pitch)
            print(self.m_camera.m_yaw)
        elif c == b'r':
            self.m_camera.m_pos=np.array((0.60108362,12.07439748,-0.36730854))
            self.m_camera.m_pitch=-1.6000000000000003
            self.m_camera.m_yaw=-1.4707963267948965
        elif c == b'c':# 側邊
            self.m_camera.m_pos=np.array((9.66514424,3.33536864,1.41968903))
            self.m_camera.m_pitch=-2.7755575615628914e-17
            self.m_camera.m_yaw=-3.070796326794898
        if c == b'\x08':#backspace
            if(len(self.now_sum)!=0):
                self.now_sum.pop()
        elif c >= b'0' and c <= b'9':
            self.now_sum.append(c)
        elif c == b'\r':#enter
            self.target=0
            for i in range(self.m_diceCnt):
                self.target += self.m_dices[i].GetPoint()
            sum=0
            for i in self.now_sum:
                sum=sum*10+int(i)-int(b'0')
            self.now_sum=[]
            if sum==self.target:
                self.score+=4
                self.begin_time+=1.75
                self.pre_time=time.time()
                self.__CurrentScene=self.DrawAC
                self.__CurrentKeyboard=self.DoNothingKeyboard
            else : 
                self.score-=1
                self.begin_time+=1.75
                self.pre_time=time.time()
                self.__CurrentScene=self.DrawWA
                self.__CurrentKeyboard=self.DoNothingKeyboard
            self.m_camera.m_pos=np.array((9.66514424,3.33536864,1.41968903))
            self.m_camera.m_pitch=-2.7755575615628914e-17
            self.m_camera.m_yaw=-3.070796326794898
            self.RandomizeDices()
        elif c == b'g':
            acc = 0
            for i in range(self.m_diceCnt):
                acc += self.m_dices[i].GetPoint()
            print(acc)

    def __KeyboardFunc(self, c, x, y):
        self.__CurrentKeyboard(c)




'''
正上方camera資訊
m_pos->[ 0.60108362 12.07439748 -0.36730854]
m_pitch-1.6000000000000003
m_yaw-1.4707963267948965

旁邊camera資訊
m_pos->[ 2.67276163  3.51072055 -8.99496325]
m_pitch->-3.1000000000000014
m_yaw->-1.4707963267948965
'''
