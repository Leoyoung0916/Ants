#  -*- coding:utf-8 -*-

'''在本实验中，我尝试着用更加稀疏的数据结构，比如字典结构，来表达蚂蚁，信息素，位置等信息

这样,不但信息获取速度会增加，而且节约空间'''


import random
import math

class Ant(object):
 	"""docstring for Ant"""
 	def __init__(self,world,x=0,y=0,iffood=False):
 		super(Ant, self).__init__()
 		self.world = world
 		self.x = x
 		self.y = y
 		self.iffood = iffood
 		self.next = 0  # 0 表示水平方向，1 表示竖直方向 
 		try:
			self.world.locationWithAnts[self.x][self.y].append(self)
		except:
			try:
				self.world.locationWithAnts[self.x].update({self.y : [self] })
			except:
				self.world.locationWithAnts.update({self.x:{self.y : [self]}})

 	def updateants(self):

 		self.laypheromone()
	 	self.world.locationWithAnts[self.x][self.y].remove(self)
	 	
 		if not self.iffood:
	 		if self.next == 0:
	 			self.x+=1 #向右前进
	 		else:
	 			self.y+=1 #向上前进
	 	else:
	 		if self.next == 0:
	 			self.x-=1 #向左前进
	 		else:
	 			self.y-=1 #向下前进

	 	try:
	 		self.world.locationWithAnts[self.x][self.y].append(self)
	 	except:
	 		try:
	 			self.world.locationWithAnts[self.x].update({self.y : [self]})
	 		except:
	 			self.world.locationWithAnts.update({self.x:{self.y : [self]}})

	def decide(self):
		''' 我试图用字典来存储world上的pheromones，如果找不到对应的位置（没有记载），说明没有信息素'''

		if not self.iffood:
			try:
				pheromone0 = self.world.pheromone[self.x+1][self.y]    
			except:
				pheromone0 = 0

			try:
				pheromone1 = self.world.pheromone[self.x][self.y+1]
			except:
				pheromone1 = 0
		else:
			try:
				pheromone0 = self.world.pheromone[self.x-1][self.y]
			except:
				pheromone0 = 0
			try:
				pheromone1 = self.world.pheromone[self.x][self.y-1]
			except:
				pheromone1 = 0

		'''这是一个奇怪的算法，当然，可以调整。'''

		# print " compare ",pheromone0,pheromone1
		dice = random.random()
		try:
			prob = pheromone0 **2 / float( pheromone0**2 + pheromone1**2)
		except:
			prob = 0.5
		# print  "dice & prob" , dice, prob


		if  prob > dice:
			self.next = 0
		else:
			self.next = 1

	def laypheromone(self):
		if not self.iffood:
			pheromone = 1
		else:
			pheromone = 2
		try:
			self.world.pheromone[self.x][self.y] += pheromone
		except:
			try:
				self.world.pheromone[self.x].update({self.y : pheromone})
			except:
				self.world.pheromone.update({self.x : {self.y: pheromone}})


class Location(object):
	"""docstring for Location"""
	def __init__(self,world,x,y,pheromone,foodnum = 0):
		super(Location, self).__init__()
		self.world = world
		self.x = x
		self.y = y
		self.foodnum = foodnum
		self.pheromone = pheromone
		self.antlist = []

class World(object):
	"""docstring for World"""
	def __init__(self):
		super(World, self).__init__()
		self.locationWithAnts = {}
		self.pheromone = {}

	def addAnts(self):
		addnum = 10
		for i in range(addnum):
			ant = Ant(self)

	def updateworld(self):

		tempantlist= []
		for y in self.locationWithAnts.itervalues():
			for antlist in y.itervalues():
				for ant in antlist:
					ant.decide()
					tempantlist.append(ant)

		for ant in tempantlist:
			ant.updateants()
		 

	def evolution(self,n):
		steps = n
		for i in range(steps):
			self.addAnts()
			self.updateworld()

	def displayworld(self):
		for x, subdict in self.locationWithAnts.iteritems():
			for y,antlist in subdict.iteritems():
				for ant in antlist:
					print ant.x,ant.y

	def displaypheromone(self):
		for x, subdict in self.pheromone.iteritems():
			for y,pheromone in subdict.iteritems():
				print "pheromone",x,y,pheromone



def main():
	world = World()
	world.evolution(20)
	world.displayworld()


if __name__ == "__main__":
	main()


	