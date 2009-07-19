#!/usr/bin/python
# -*- coding: utf-8 -*-

from XiboTransition import XiboTransition
from threading import Thread, Semaphore

class FlyTransition(XiboTransition):

    def run(self):
	self.lock = Semaphore()
	self.lock.acquire()

	if self.media1 != None:
		if self.options1['transOutDuration'] > 0:
			self.outDuration = int(self.options1['transOutDuration'])
		else:
			self.outDuration = 1000

		self.log.log(5,"info","Running FlyOut transition")
		self.__animate__(self.media1.getName(),self.media1.getX(),self.media1.getY(),self.media1.getWidth(),self.media1.getHeight(),self.options1["transOutDirection"],self.outDuration,self.next)
		self.lock.acquire()

	if self.media2 != None:
		if self.options2['transInDuration'] > 0:
			self.inDuration = int(self.options2['transInDuration'])
		else:
			self.inDuration = 1000

		self.__animate__(self.media2.getName(),0 - self.media2.getWidth(), 0 - self.media2.getHeight(),self.media2.getX(),self.media2.getY(),self.options2["transInDirection"],self.inDuration,self.next)
		self.lock.acquire()

	self.callback()

    def next(self):
	self.lock.release()

    def __animate__(self,name,currentX,currentY,w,h,direction,duration,callback):
	if direction == "N":
		self.p.enqueue('anim',('linear',name,duration,'y',currentY,(-10 -h),callback))
		return

	if direction == "NE":
		self.p.enqueue('anim',('linear',name,duration,'y',currentY,(-10 -h),None))
		self.p.enqueue('anim',('linear',name,duration,'x',currentX,(-10 -w),callback))
		return

	if direction == "E":
		self.p.enqueue('anim',('linear',name,duration,'x',currentX,(-10 -w),callback))
		return

	if direction == "SE":
		self.p.enqueue('anim',('linear',name,duration,'y',currentY,(10 + h),None))
		self.p.enqueue('anim',('linear',name,duration,'x',currentX,(-10 -w),callback))
		return

	if direction == "S":
		self.p.enqueue('anim',('linear',name,duration,'y',currentY,(10 + h),callback))
		return

	if direction == "SW":
		self.p.enqueue('anim',('linear',name,duration,'x',currentX,(10 + w),None))
		self.p.enqueue('anim',('linear',name,duration,'y',currentY,(10 + h),callback))
		return

	if direction == "W":
		self.p.enqueue('anim',('linear',name,duration,'x',currentX,(10 + w),callback))
		return

	if direction == "NW":
		self.p.enqueue('anim',('linear',name,duration,'x',currentX,(10 + w),None))
		self.p.enqueue('anim',('linear',name,duration,'y',currentY,(-10 -h),callback))
		return
		
