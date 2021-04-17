import pygame
from pygame.locals import *

pygame.init()

FONT1 = pygame.font.SysFont('calibri',40,True)
FONT2 = pygame.font.SysFont('calibri',20,True)
FONT3 = pygame.font.SysFont('calibri',30,True)


width,height = 1536,801
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Settings")

class Settings:

	def __init__(self,screen,clock):

		self.screen = screen
		self.clock = clock
		self.get_typechoice_images()
		self.get_texts()
		self.checkbox_positions = {'ptype':[(690,150),(690,321),(690,492)],'ctype':[(955,265),(1300,265),(955,530),(1300,530)]}
		self.ptype = 3
		self.ctype = 3
		self.music = 1
		self.volume_value = 50 


	def get_typechoice_images(self):

		self.piece_type1 = pygame.transform.scale(pygame.image.load('Media/setting_ptype_1.png'),(600,151))
		self.piece_type2 = pygame.transform.scale(pygame.image.load('Media/setting_ptype_2.png'),(600,151))
		self.piece_type3 = pygame.transform.scale(pygame.image.load('Media/setting_ptype_3.png'),(600,151))

		self.color_type1 = pygame.transform.scale(pygame.image.load('Media/setting_ctype_1.png'),(310,151))
		self.color_type2 = pygame.transform.scale(pygame.image.load('Media/setting_ctype_2.png'),(310,151))
		self.color_type3 = pygame.transform.scale(pygame.image.load('Media/setting_ctype_3.png'),(310,151))
		self.color_type4 = pygame.transform.scale(pygame.image.load('Media/setting_ctype_4.png'),(310,151))

		self.select = pygame.image.load('Media/select.png')

	def get_texts(self):

		self.pappearance = FONT1.render("Pieces Appearance",True,(255,255,255))
		self.pappearance_rect = self.pappearance.get_rect()
		self.pappearance_rect.center = (400,70)

		self.boardtheme = FONT1.render("Board Theme",True,(255,255,255))
		self.boardtheme_rect = self.boardtheme.get_rect()
		self.boardtheme_rect.center = (1150,70)

		self.on = FONT2.render("ON",True,(0,0,0))
		self.on_rect = self.on.get_rect()
		self.on_rect.center = (378,717)

		self.off = FONT2.render("OFF",True,(0,0,0))
		self.off_rect = self.off.get_rect()
		self.off_rect.center = (322,717)
		
		self.m = FONT3.render("Music",True,(255,255,255))
		self.m_rect = self.m.get_rect()
		self.m_rect.center = (230,717)

		self.v = FONT3.render("Volume",True,(255,255,255))
		self.v_rect = self.v.get_rect()
		self.v_rect.center = (700,717)

		self.increase = FONT3.render("+",True,(0,255,0))
		self.increase_rect = self.increase.get_rect()
		self.increase_rect.center = (1264,715)

		self.decrease = FONT3.render("-",True,(255,0,0))
		self.decrease_rect = self.decrease.get_rect()
		self.decrease_rect.center = (1314,715)

	def update(self):

		while True:
			self.screen.fill("#17252A")
			#self.screen.fill((0,0,0))
			pos = pygame.mouse.get_pos()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					return

				if event.type == pygame.MOUSEBUTTONDOWN:
					if pos[0]<=400 and pos[0]>=300 and pos[1]<=730 and pos[1]>=700:
						self.music = not self.music

					elif pos[0]<=1280 and pos[0]>=1250 and pos[1]<=730 and pos[1]>=700:
						if self.volume_value < 100:
							self.volume_value += 10
							#print(self.volume_value)

					elif pos[0]<=1330 and pos[0]>=1300 and pos[1]<=730 and pos[1]>=700:
						if self.volume_value > 0:
							self.volume_value -= 10
							#print(self.volume_value)

					elif pos[0]<=725 and pos[0]>=695 and pos[1]<=195 and pos[1]>=165:
						self.ptype = 1

					elif pos[0]<=725 and pos[0]>=695 and pos[1]<=366 and pos[1]>=336:
						self.ptype = 2

					elif pos[0]<=725 and pos[0]>=695 and pos[1]<=537 and pos[1]>=507:
						self.ptype = 3

					elif pos[0]<=990 and pos[0]>=960 and pos[1]<=310 and pos[1]>=280:
						self.ctype = 1

					elif pos[0]<=1335 and pos[0]>=1305 and pos[1]<=310 and pos[1]>=280:
						self.ctype = 2

					elif pos[0]<=990 and pos[0]>=960 and pos[1]<=575 and pos[1]>=545:
						self.ctype = 3

					elif pos[0]<=1335 and pos[0]>=1305 and pos[1]<=575 and pos[1]>=545:
						self.ctype = 4

			#piece appearnce border
			pygame.draw.rect(self.screen,(255,255,255),[25,37.5,750,583],2)
			#board theme border
			pygame.draw.rect(self.screen,(255,255,255),[800,37.5,700,583],2)

			#options
			self.screen.blit(self.piece_type1,(45,107.5))
			self.screen.blit(self.piece_type2,(45,278.5))
			self.screen.blit(self.piece_type3,(45,449.5))

			self.screen.blit(self.color_type1,(820,107.5))
			self.screen.blit(self.color_type2,(820,370.5))
			self.screen.blit(self.color_type3,(1165,107.5))
			self.screen.blit(self.color_type4,(1165,370.5))

			self.screen.blit(self.pappearance,self.pappearance_rect)
			self.screen.blit(self.boardtheme,self.boardtheme_rect)

			#checkboxes
			pygame.draw.rect(self.screen,(255,255,255),[695,165,30,30],3)
			pygame.draw.rect(self.screen,(255,255,255),[695,336,30,30],3)
			pygame.draw.rect(self.screen,(255,255,255),[695,507,30,30],3)

			pygame.draw.rect(self.screen,(255,255,255),[960,280,30,30],3)
			pygame.draw.rect(self.screen,(255,255,255),[1305,280,30,30],3)
			pygame.draw.rect(self.screen,(255,255,255),[960,545,30,30],3)
			pygame.draw.rect(self.screen,(255,255,255),[1305,545,30,30],3)

			self.screen.blit(self.select,self.checkbox_positions['ptype'][self.ptype-1])
			self.screen.blit(self.select,self.checkbox_positions['ctype'][self.ctype-1])

			pygame.draw.rect(self.screen,(255,255,255),[300,700,100,30],2)

			if self.music:
				pygame.draw.rect(self.screen,(54,179,87),[302,702,57,27])
				pygame.draw.rect(self.screen,("#9147ff"),[359,702,40,27])
				self.screen.blit(self.on,self.on_rect)

			else:
				pygame.draw.rect(self.screen,(54,179,87),[302,702,40,27])
				pygame.draw.rect(self.screen,("#464649"),[342,702,57,27])		
				self.screen.blit(self.off,self.off_rect)

			self.screen.blit(self.m,self.m_rect)
			self.screen.blit(self.v,self.v_rect)
			

			if pos[0]<=1280 and pos[0]>=1250 and pos[1]<=730 and pos[1]>=700:
				pygame.draw.rect(self.screen,(186,103,35),[1250,700,30,30])

			if pos[0]<=1330 and pos[0]>=1300 and pos[1]<=730 and pos[1]>=700:
				pygame.draw.rect(self.screen,(186,103,35),[1300,700,30,30])

			pygame.draw.line(self.screen,(255,255,255),(800,715),(1200,715),3)

			# 985 ~ 1000  -->  scale position of pointer to 0-400 from 0-100		
			pygame.draw.rect(self.screen,(54,179,87),[785+(4*self.volume_value),700,30,30])
			
			#increase volume
			pygame.draw.rect(self.screen,(255,255,255),[1250,700,30,30],3)
			self.screen.blit(self.increase,self.increase_rect)

			#decrease volume
			pygame.draw.rect(self.screen,(255,255,255),[1300,700,30,30],3)
			self.screen.blit(self.decrease,self.decrease_rect)

			pygame.display.flip()
			clock.tick(60)

settings = Settings(screen,clock)
settings.update()

