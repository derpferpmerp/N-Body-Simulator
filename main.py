import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

plt.rcParams.update({
	"lines.color": "white",
	"patch.edgecolor": "white",
	"text.color": "white",
	"axes.facecolor": "white",
	"axes.edgecolor": "lightgray",
	"axes.labelcolor": "white",
	"xtick.color": "white",
	"ytick.color": "white",
	"grid.color": "lightgray",
	"figure.facecolor": "black",
	"figure.edgecolor": "black",
	"savefig.facecolor": "black",
	"savefig.edgecolor": "black"
})



CGRAV = 6.67408 * math.pow(10,-11)
PARTMASS = 2
m1pos = m1x, m1y, m1z = (0, 0, 0)
m2pos = m2x, m2y, m2z = (100, 200, 30)





class Particle(object):
	def __init__(self, mass, x, y, z):
		self.mass = mass
		self.pos = self.x, self.y, self.z = (x, y, z)
		self.timeDelay = 0.1
		self.pos = np.array(self.pos)
	
	def pForce(self, collider):
		return ((CGRAV)*(self.mass**2))/((self.pos-collider.pos)**2)

	def vectorMagnitude(self, collider):
		dx, dy, dz = self.pos - collider.pos
		diArray = np.array([dx,dy,dx])
		return math.sqrt(sum(diArray*diArray))

	def vectorAngle(self, collider):
		dist = dx, dy, dz = self.pos - collider.pos
		aNPLIST = ax, ay, az = dist
		bNPLIST = bx, by, bz = dist
		aNPLIST = np.array(aNPLIST)
		bNPLIST = np.array(bNPLIST)
		sA = math.sqrt(ax*ax + ay*ay + az*az)
		sB = math.sqrt(bx*bx + by*by + bz*bz)
		tupOut = np.array(dist)/sA
		tupOut2 = [math.acos(x) for x in tupOut]
		tupOut = [math.degrees(x) for x in tupOut2]
		for x in tupOut:
			#print("Apply A Force of {0} in the {1} direction".format(x,["X","Y","Z"][tupOut.index(x)]))
			pass
		return tupOut

	def show(self, collider):
		distances = dx, dy, dz = self.pos - collider.pos
		distances = np.array(distances)
		m1Forces = m1Fx, m1Fy, m1Fz = self.pForce(collider)
		m1Forces = np.array(m1Forces)
		theta = math.atan(m1Fy/m1Fx)
		forceXYZ = math.sqrt(sum(distances*distances))
		#print(self.vectorAngle(collider))

	def move(self, collider):
		td = 1
		res = self.vectorAngle(collider)
		#print(res)
		self.x += td * res[0]
		self.y += td * res[1]
		self.z += td * res[2]
		self.pos = np.array([self.x,self.y,self.z])
		#print("\n")
		return res + [self.x,self.y,self.z]



def smooth(mx,mn,xl,yl,axL,c="blue"):
	x_new = np.linspace(mn, mx, 1000)
	a_BSpline = interpolate.make_interp_spline(xl, yl)
	y_new = a_BSpline(x_new)
	axL.plot(x_new,y_new,color=c)

def calcMasses(mass,MASSES):
	for itr in MASSES:
		if itr == mass: continue
		res = mass.move(itr)
	return res

def mapAppend(lofLists,lst):
	for x in range(len(lst)):
		lofLists[x].append(lst[x])
	return lofLists

def graph(m1,m2,m3,m4,ITERATIONS=10,masses=[],outfile="out.png"):
	xl = []
	yl1, yl2, yl3, yl4, yl5, yl6 = [[] for x in range(6)]
	yl11, yl12, yl13, yl14, yl15, yl16 = [[] for x in range(6)]
	yl21, yl22, yl23, yl24, yl25, yl26 = [[] for x in range(6)]
	yl31, yl32, yl33, yl34, yl35, yl36 = [[] for x in range(6)]
	MASSES = [m1,m2,m3,m4]
	for x in range(ITERATIONS):
			xl.append(x)

			res = calcMasses(m1,MASSES)
			b = calcMasses(m2,MASSES)
			c = calcMasses(m3,MASSES)
			d = calcMasses(m4,MASSES)

			yl1, yl2, yl3, yl4, yl5, yl6 = mapAppend([yl1, yl2, yl3, yl4, yl5, yl6], res)

			yl11, yl12, yl13, yl14, yl15, yl16 = mapAppend([yl11, yl12, yl13, yl14, yl15, yl16], b)

			yl21, yl22, yl23, yl24, yl25, yl26 = mapAppend([yl21, yl22, yl23, yl24, yl25, yl26], c)

			yl31, yl32, yl33, yl34, yl35, yl36 = mapAppend([yl31, yl32, yl33, yl34, yl35, yl36], d)
	
	print("Finished Calculating Masses")

	fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(30,20))

	COLORS = ["red", "black", "blue", "orange"]
	LABELS = ["F_net(X)","F_net(Y)","F_net(Z)"]
	PARTS = [yl1,yl11,yl21,yl31]
	AXES = [ax1,ax2,ax3]

	TDPLOTAXES = [
		[np.array(yl4), np.array(yl5), np.array(yl6),"red"],
		[np.array(yl14),np.array(yl15),np.array(yl16),"black"],
		[np.array(yl24),np.array(yl25),np.array(yl26),"blue"],
		[np.array(yl34),np.array(yl35),np.array(yl36),"orange"]
	]

	for ax in range(len(AXES)):
		for g in range(len(PARTS)):
			smooth(0,ITERATIONS,xl,PARTS[g],AXES[ax],c=COLORS[g])
		AXES[ax].set_xlabel(LABELS[ax], color="w")

	ax4 = plt.subplot(212,projection ='3d')

	for aXval, aYval, aZval, color in TDPLOTAXES:
		ax4.plot3D(
			aXval,
			aYval,
			aZval,
			c=color
		)

	ax4.scatter3D(m1.x,m1.y,m1.z,color="red")
	ax4.scatter3D(m2.x,m2.y,m2.z,color="black")
	ax4.scatter3D(m3.x,m3.y,m3.z,color="blue")
	ax4.scatter3D(m4.x,m4.y,m4.z,color="orange")

	ax4.set_xlabel('$X$', fontsize=20, color="black")
	ax4.set_ylabel('$Y$', fontsize=20, color="black")

	ax4.yaxis._axinfo['label']['space_factor'] = 10.0
	print("Finished Graphing Masses")

	ticks = xticks, yticks, zticks = [ax4.xaxis.get_major_ticks(),ax4.yaxis.get_major_ticks(),ax4.zaxis.get_major_ticks()]
	for t in ticks:
		for x in t:
			x.label.set_fontsize(10)
			x.label.set_color("black")


	TITLEFONTSIZE = 50
	for axItm in [ax1,ax2,ax3,ax4,ax5,ax6]:
		axItm.xaxis.label.set_fontsize(TITLEFONTSIZE)

	plt.tight_layout()
	print("Finished Graph-Image Processing")

	plt.savefig(outfile)

def run(part1, part2, part3, part4, ITERMAX=20):
	graph(part1,part2,part3, part4, outfile="out1-2A.png",ITERATIONS=ITERMAX)

def mult():
	p1 = Particle(PARTMASS, 0, 0, 0)
	p2 = Particle(PARTMASS, 10, 20, 30)
	p3 = Particle(PARTMASS, 2000, 3000, 800)
	p4 = Particle(PARTMASS, 200, 150, 400)
	#graph(p1,p2,outfile="out1-2.png")
	#graph(p3,p4,outfile="out3-4.png",ITERATIONS=40)
	m1L, m2L, m3L, m4L = [[],[],[],[]]
	MASSES = [p1,p2,p3,p4]
	for x in range(25):
		res = calcMasses(p1,MASSES)
		b = calcMasses(p2,MASSES)
		c = calcMasses(p3,MASSES)
		d = calcMasses(p4,MASSES)
		m1L.append(res[0])
		m2L.append(b[0])
		m3L.append(c[0])
		m4L.append(d[0])
	#run(p1,p2,p3,p4)
	print(m1L,m2L,m3L,m4L,sep="\n\n\n")
	smooth(0,25,range(25),m1L,plt,c="blue")
	#plt.scatter(range(100),m1L)
	plt.savefig("out.png")
	print("Done")

mult()
