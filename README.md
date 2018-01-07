# snake-robots-lateral-undulation
This is the revised version of the programs I wrote for my Bachelor Thesis, which is about the control of snake-like robots **Lateral Undulation** gait. The simulation of my snake-like robot (Fig.1) controlled by this program is carried out in the Virtual Robotic Experiment Platform (**V-REP**). In Fig.1, blue rectangles denote passive wheels attached to links' belly to result in the anisotropic friction force exerted on the robot by terrains. 
<p align="center"> 
  <img src="https://i.imgur.com/zfdpEDk.png?1">
</p>
<p align="center">
  <em> Fig.1 My snake robot and its configuartion </em>
</p>

## Control Plan
To tackle the big problem of controlling snake-like robots Lateral Undulation gait, I first targeted four sub problems (listed in Fig.2) that makes up the big one. The solution of each sub problem is built on top of the previous in the order indicated by the blue arrow.
<p align="center"> 
  <img src="https://i.imgur.com/lMHTkZ0.png?1">
</p>
<p align="center">
  <em> Fig.2 Control plan </em>
</p>

## Create rhythmic motion among the robots' joints
Like their biological counterparts, snake-like robots periodically undulate their body side way to gain forward motion. This macroscopic motion is created when every joint oscillates at the same frequency with constant phase lag, compared to the adjacent joints (i.e. move rhythmically). To produce such motion among robots' joints, I used a network of Central Pattern Generators (CPG) displayed in Fig.3.
<p align="center"> 
  <img src="https://i.imgur.com/RAeiYH6.png?3">
</p>
<p align="center">
  <em> Fig.3 CPG network </em>
</p>
In Fig.3, an arrow represents a connection having the mathematics description of the Kuramoto oscillator. The symbol written on an arrow denotes the phase lag of this connection. A circle is a CPG associated with the joint which name written in it.

## Calculate robot's direction of motion
The direction of lateral undulation gait is the symmetrical line of snakes' body. Using this idea, I calculate the direction of my robot motion by finding the symmetrical line of the sets of center of mass (COM) of my robot's links. This symmetrical line can be found using the SVD on the matrix P defined below.
<p align="center"> 
  <img src="https://latex.codecogs.com/gif.latex?P&space;=&space;\begin{bmatrix}&space;x_1&space;-&space;\overline{x}&space;&&space;y_1&space;-&space;\overline{y}&space;\\&space;x_2&space;-&space;\overline{x}&space;&&space;y_2&space;-&space;\overline{y}&space;\\&space;\vdots&space;&&space;\vdots&space;\\&space;x_{N&plus;1}&space;-&space;\overline{x}&space;&&space;y_{N&plus;1}&space;-&space;\overline{y}&space;\\&space;\end{bmatrix}">
</p>
<p>
  In matrix P, <img src="https://latex.codecogs.com/gif.latex?(x_i,&space;y_i)"> denotes the coordinate of COM of link i, and <img src="https://latex.codecogs.com/gif.latex?(\overline{x},&space;\overline{y})"> is the mean of the set of all links' COM. All the coordinates presented in matrix P are computed relative to the robot first link because this calculation is based only on robot internal information which is the angular position of robot's joints. Such calculation can be carried out using Denavit-Hartenberg convention. 
</p>

#### Note:

This program runs on Windows.

The vrep sence needs to be opened first. But, don't hit the play button. The snake_main_rev.py will activate this sence.
