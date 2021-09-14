import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
import random
import PySimpleGUI as sg

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
	"savefig.edgecolor": "black",
})

sg.theme('DarkTeal12')

CGRAV = 6.67408 * math.pow(10,-11)
PARTMASS = 2





class Particle:
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
			pass
		return tupOut

	def show(self, collider):
		distances = dx, dy, dz = self.pos - collider.pos
		distances = np.array(distances)
		m1Forces = m1Fx, m1Fy, m1Fz = self.pForce(collider)
		m1Forces = np.array(m1Forces)
		math.atan(m1Fy/m1Fx)
		math.sqrt(sum(distances*distances))

	def move(self, collider):
		td = 1
		res = self.vectorAngle(collider)

		self.x += td * res[0]
		self.y += td * res[1]
		self.z += td * res[2]

		self.pos = np.array([self.x,self.y,self.z])
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

def generateMassTemplate(stage,lst=None,MASS=None,temp=None):
	TEMPLATE = {
		"NET":{
			"X": [],
			"Y": [],
			"Z": []
		},
		"POS": {
			"X": [],
			"Y": [],
			"Z": []
		},
		"MASS": "placeholder"
	}
	if temp != None: TEMPLATE = temp

	if stage == "GEN":
		TEMPLATE["MASS"] = MASS
	elif stage == "APP":
		TEMPLATE["NET"]["X"].append(lst[0])
		TEMPLATE["NET"]["Y"].append(lst[1])
		TEMPLATE["NET"]["Z"].append(lst[2])

		TEMPLATE["POS"]["X"].append(lst[3])
		TEMPLATE["POS"]["Y"].append(lst[4])
		TEMPLATE["POS"]["Z"].append(lst[5])

	return TEMPLATE

def generateColor(bounds=[0,255],amount=3,PLACES=2):
	outlist = []
	for x in range(amount):
		outlist.append(random.randrange(bounds[0],bounds[1]))
	
	return tuple(list(map(lambda x: round(x/bounds[1],PLACES), outlist)))

def graph(AMOUNTOFMASSES=50,ITERATIONS=10,PARTMASS=PARTMASS,outfile="out.png"):
	xl = []

	MASSES = []
	RANDOMRANGE = rLimX, rLimY = [0, 10000]
	for massCreator in range(AMOUNTOFMASSES):
		sg.one_line_progress_meter('Loading', massCreator+1, AMOUNTOFMASSES, 'key', 'Creating Particles')
		MASSES.append(
			Particle(
				PARTMASS,
				random.randrange(rLimX,rLimY),
				random.randrange(rLimX,rLimY),
				random.randrange(rLimX,rLimY)
			)
		)

	
	
	MASSDICTIONARY = []

	for mass in MASSES:
		MASSDICTIONARY.append(generateMassTemplate("GEN", MASS=mass))


	# 1: Fx, 2: Fy, 3: Fz, 4: Xpos, 5: YPos, 6: Zpos

	for x in range(ITERATIONS):
		sg.one_line_progress_meter('Loading', x+1, ITERATIONS, 'key', 'Creating Graph')
		xl.append(x)
		for massIter in range(AMOUNTOFMASSES):
			lstVal = calcMasses(MASSDICTIONARY[massIter]["MASS"],MASSES)
			MASSDICTIONARY[massIter] = generateMassTemplate(
				"APP",
				lst=lstVal,
				temp=MASSDICTIONARY[massIter],
			)

	print("Finished Calculating Masses")

	fig, ((ax1,ax2,ax3),(ax4,ax5,ax6)) = plt.subplots(2,3,figsize=(30,20))


	COLORS = [generateColor(amount=3) for x in range(AMOUNTOFMASSES)]
	LABELS = ["F_net(X)","F_net(Y)","F_net(Z)"]
	PARTS = [x["NET"] for x in MASSDICTIONARY]
	AXES = [ax1,ax2,ax3]

	TDPLOTAXES = []
	for g in range(AMOUNTOFMASSES):
		dct = MASSDICTIONARY[g]["POS"]
		TDPLOTAXES.append([
			np.array(dct["X"]),
			np.array(dct["Y"]),
			np.array(dct["Z"]),
			COLORS[g]
		])

	for ax in range(len(AXES)):
		for g in range(len(PARTS)):
			graphAxis = ["X","Y","Z"][ax]
			smooth(
				0,
				ITERATIONS,
				xl,
				PARTS[g][graphAxis],
				AXES[ax],
				c=COLORS[g]
			)
		AXES[ax].set_xlabel(LABELS[ax], color="w")

	ax4 = plt.subplot(212, projection="3d")

	for aXval, aYval, aZval, color in TDPLOTAXES:
		ax4.plot3D(
			aXval,
			aYval,
			aZval,
			c=color,
		)
	for x in MASSES:
		ax4.scatter3D(x.x,x.y,x.z,color=COLORS[MASSES.index(x)])

	
	ax4.set_xlabel("$X$", fontsize=20, color="black")
	ax4.set_ylabel("$Y$", fontsize=20, color="black")
	ax4.yaxis._axinfo["label"]["space_factor"] = 10.0

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

	#plt.savefig(outfile)
	plt.show(block=False)

def run(ITERMAX=20,AMOUNTOFMASSES=50,pMass=2):
	graph(outfile="out1-2A.png", ITERATIONS=ITERMAX, AMOUNTOFMASSES=AMOUNTOFMASSES,PARTMASS=pMass)
	print("Done")

layout = [
	[
		sg.Text('Amount of Particles: ', size=(20, 1)),
		sg.Slider(
			(5, 100),
			10,
			1,
			orientation="h",
			size=(20, 15),
			key="-PARTICLE SLIDER-",
			enable_events=True
		)
	],
	[
		sg.Text('Mass of Particles', size=(20, 1)),
		sg.Slider(
			(1, 100),
			2,
			1,
			orientation="h",
			size=(20, 15),
			key="-MASS SLIDER-",
			enable_events=True
		)
	],
	[
		sg.Text('Amount of Iterations', size=(20, 1)),
		sg.Slider(
			(1, 100),
			10,
			1,
			orientation="h",
			size=(20, 15),
			key="-ITER SLIDER-",
			enable_events=True
		)
	],
	[sg.Button("Generate Simulation")],
	[sg.Button("Exit")]
]
window = sg.Window(
	title="N-Body-Simulator",
	layout=layout,
	margins=(100, 50)
)
currentbutton = None
hasclickedbutton = False
matplotlibWindowOpen = False

while True:
	event, values = window.read()
	if not matplotlibWindowOpen and event == sg.WIN_CLOSED:
		break
	elif event == "Generate Simulation":
		amtParts, massParts, iterations = [values["-PARTICLE SLIDER-"], values["-MASS SLIDER-"], values["-ITER SLIDER-"]]
		amtParts = round(amtParts)
		massParts = round(massParts)
		iterations= round(iterations)
		run(
			ITERMAX=iterations,
			AMOUNTOFMASSES=amtParts,
			pMass=massParts
		)
		matplotlibWindowOpen=True
	elif matplotlibWindowOpen and event == sg.WIN_CLOSED:
		matplotlibWindowOpen=False

window.close()