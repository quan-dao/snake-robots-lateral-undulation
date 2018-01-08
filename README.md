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
Like their biological counterparts, snake-like robots periodically undulate their body side way to gain forward motion. This macroscopic motion is created when every joint oscillates at the same frequency with constant phase lag, compared to the adjacent joints (i.e. move rhythmically). To produce such motion among robots' joints, I used the network of Central Pattern Generators (CPG) [1,2] displayed in Fig.3.
<p align="center"> 
  <img src="https://i.imgur.com/RAeiYH6.png?3">
</p>
<p align="center">
  <em> Fig.3 CPG network </em>
</p>
In Fig.3, a circle is a CPG associated with the joint which name is written in it, while an arrow represents a connection go from the CPG i (in the arrow base) to the CPG j (in the arrow tip). This connection is described below.
<p align="center"> 
  <img src="https://latex.codecogs.com/gif.latex?\dot{\theta_{j}}&space;=&space;2\pi&space;v&space;&plus;&space;w&space;\sin(\theta_i&space;-&space;\theta_j&space;-\xi)">
</p>
<p>In this equation, <img src="https://latex.codecogs.com/gif.latex?\theta_i"> is the phase of CPG i. v, w are respectively frequency parameter and coupling strength. <img src="https://latex.codecogs.com/gif.latex?\xi"> is the phase lag of the connection and is equal to the value written on the arrow representing the connection. The output of CPG i (<img src="https://latex.codecogs.com/gif.latex?\phi_i">) which is used as the reference of the angular position of joint i is</p>
<p align="center">
  <img src="https://latex.codecogs.com/gif.latex?\phi_i&space;=&space;A&space;\sin(\theta_i)">
</p>

## Calculate robot's direction of motion
The direction of lateral undulation gait is the symmetrical line of snakes' body. Using this idea, I calculate the direction of my robot motion by finding the symmetrical line of the sets of center of mass (COM) of my robot's links. This symmetrical line can be found using the SVD on the matrix P defined below. The eigenvectors resulted by the singular value decomposition of matrix P form a local frame named the Virtual Chassis [3].
<p align="center"> 
  <img src="https://latex.codecogs.com/gif.latex?P&space;=&space;\begin{bmatrix}&space;x_1&space;-&space;\overline{x}&space;&&space;y_1&space;-&space;\overline{y}&space;\\&space;x_2&space;-&space;\overline{x}&space;&&space;y_2&space;-&space;\overline{y}&space;\\&space;\vdots&space;&&space;\vdots&space;\\&space;x_{N&plus;1}&space;-&space;\overline{x}&space;&&space;y_{N&plus;1}&space;-&space;\overline{y}&space;\\&space;\end{bmatrix}">
</p>
<p>
  In matrix P, <img src="https://latex.codecogs.com/gif.latex?(x_i,&space;y_i)"> denotes the coordinate of COM of link i, and <img src="https://latex.codecogs.com/gif.latex?(\overline{x},&space;\overline{y})"> is the mean of the set of all links' COM.</p>
All the coordinates presented in matrix P are computed relative to the robot first link because this calculation is based only on robot internal information which is the angular position of robot's joints. Such calculation can be carried out using Denavit-Hartenberg convention. 

## Steer robot crawling motion
Robot crawling direciton can be steered by chaning the symmetrical line of the whole robot body. This is done by integrating the Amplitude Modulation Method [4] into CPGs' output as following
<p align="center">
  <img src="https://latex.codecogs.com/gif.latex?\phi_i&space;=&space;A&space;\[1&space;&plus;&space;\Delta&space;Asign(\sin(\theta_i))]\sin(\theta_i)">
</p>
<p>The reason I used this method is the Linear-Time Invariant (LTI) relationsip between the control signal (<img src="https://latex.codecogs.com/gif.latex?\Delta&space;A">) and robot turning angle [4,5]. </p>

## Direction control scheme
At this point, I have derived the solution for the first 3 sub problems displayed in Fig.1, so I am going to integrate them into a control scheme to completely solve the direction control problem of snake robots' Lateral Undulation gait. This control scheme is shown in Fig.4.
<p align="center"> 
  <img src="https://i.imgur.com/9vSG9R5.png?1">
</p>
<p align="center">
  <em> Fig.4 Direction control scheme </em>
</p>
The Direction controller is a simple proportional controller as the equation below because of the LTI relationship mentioned in the previous section.
<p align="center">
  <img src="https://latex.codecogs.com/gif.latex?\Delta&space;A&space;=&space;K_P&space;\(\gamma_{VC}&space;-&space;\gamma_{ref}&space;\)">
</p>
<p>
  In this equation, <img src="https://latex.codecogs.com/gif.latex?\gamma_{VC},\gamma_{ref}"> are respectively the actual and the reference value of robot crawling direction. The significace of this control scheme is that it can abstract snake-like robots which have many degrees of freedom as a SISO system. This help us to steer snake robots as easy as steer a differential-drive wheeled vehicle.
</p>

## Performance of direction control scheme
The performance of the direction control scheme is demonstrated in the line following problem described by Fig.5.
<p align="center">
  <img src="https://i.imgur.com/qdFp6SP.png?3">
</p>
<p align="center">
  <em> Fig.5 Line following problem </em>
</p>
The robot progress of following the desired trajectory (the purple line) is shown in Fig.6.
<p align="center">
  <img src="https://i.imgur.com/swegPkW.png?1">
</p>
<p align="center">
  <em> Fig.6 Robot line following progress </em>
</p>
The evolution of the reference and actual value of robot crawling direction during this progress are respectively represented by the dash green and the solid blue line in Fig.7. In addition, the solid purple line in this figure denotes the value of the direction of robot head link (i.e. the first link). It can be seen that the purple and the green line are relatively match, which means the head of robot was being pointed toward the direction which robot was heading for. 
<p align="center">
  <img src="https://i.imgur.com/no2Hqj1.png?1">
</p>
<p align="center">
  <em> Fig.7 Robot line following performance </em>
</p>
  

#### References
[1] A. Crespi, A. Badertscher, A. Guignard, and A. J. Ijspeert, “AmphiBotI: An amphibious snake-like robot,”Robotics and Autonomous Systems,vol. 50, no. 4, pp. 163–175, 2005.

[2] A. J. Ijspeert and A. Crespi, “Online trajectory generation in anamphibious snake robot using a lamprey-like central pattern generatormodel,” inProceedings 2007 IEEE International Conference onRobotics and Automation. IEEE, apr 2007, pp. 262–268. 

[3] D. Rollinson, A. Buchan, and H. Choset, “Virtual chassis forsnake robots: Definition and applications,”Advanced Robotics,vol. 26, no. 17, pp. 1–22, 2012.

[4] Changlong Ye, Shugen Ma, Bin Li, and Yuechao Wang, “Turning andside motion of snake-like robot,” inIEEE International Conferenceon Robotics and Automation, 2004. Proceedings. ICRA ’04. 2004,vol. 5, no. January. IEEE, 2004, pp. 5075–5080. 

[5] X. Wu and S. Ma, “Neurally controlled steering for collision-freebehavior of a snake robot,”IEEE Transactions on Control SystemsTechnology, vol. 21, no. 6, pp. 2443–2449, 2013.

#### Note:

* This program runs on Windows.

* The vrep sence needs to be opened first. But, don't hit the play button. The snake_main_rev.py will activate this sence.
