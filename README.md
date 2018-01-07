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

#### Note:

This program runs on Windows.

The vrep sence needs to be opened first. But, don't hit the play button. The snake_main_rev.py will activate this sence.
