## Implement a Basic Driving Agent
To begin, your only task is to get the smartcab to move around in the environment. 
At this point, you will not be concerned with any sort of optimal driving policy. 
Note that the driving agent is given the following information at each intersection:

- The next waypoint location relative to its current location and heading.
- The state of the traffic light at the intersection and the presence of oncoming vehicles from other directions.
- The current time left from the allotted deadline.

To complete this task, simply have your driving agent choose a random action 
from the set of possible actions (None, 'forward', 'left', 'right') at each intersection, disregarding the input information above. 
Set the simulation deadline enforcement, enforce_deadline to False and observe how it performs.

**QUESTION:** 

Observe what you see with the agent's behavior as it takes random actions. 
Does the smartcab eventually make it to the destination? Are there any other interesting observations to note?

**Answer:**

The angent's behaviour is, unsurprisingly, random. It would at times move in a circle (around the block) not really progressing 
in any net new direction. And it doesn't appear to have any logic behind its movement as rewards for previous states and actions are ignored.
Another item of the agent's behavior is the agent can also drive over the right edge of the world and turn up on the left edge of the world.
However, the smartcab does eventually make it to its destination on occasion.

## Inform the Driving Agent
Now that your driving agent is capable of moving around in the environment, 
your next task is to identify a set of states that are appropriate for modeling the smartcab and environment. 
The main source of state variables are the current inputs at the intersection, but not all may require representation. 
You may choose to explicitly define states, or use some combination of inputs as an implicit state. At each time step, 
process the inputs and update the agent's current state using the self.state variable. 

Continue with the simulation deadline enforcement enforce_deadline being set to False, 
and observe how your driving agent now reports the change in state as the simulation progresses.

**QUESTION:** 

What states have you identified that are appropriate for modeling the smartcab and environment? 
Why do you believe each of these states to be appropriate for this problem?

**Answer:**

At each state or waypoint we perceive 6 variables, left, right, oncoming, light, next_waypoint and deadline.
Since traffic coming from the right, doesn't affect the smartcab's decision, this variable was removed - e.g. if the 
light is green, traffic from the right has stopped and if light is red, smartcab can only go right and any traffic from the right
doesn't affect these options. Likewise, the input deadline was not utilized because at this point it does not provide
any significant information to the smartcab.

Each state identifies a situation and option for the smartcab, which results in a particular reward. With Q-learning implemented
the smartcab will be able to use these states to learn and best determine its path to the destination.
 
Final states used - light, oncoming, left, next_waypoint 

**OPTIONAL:** 

How many states in total exist for the smartcab in this environment? 
Does this number seem reasonable given that the goal of Q-Learning is to learn and make informed decisions about each state? Why or why not?

**Answer:**

Light: Red or green
Oncoming: None, left, right, forward
Left: None, left, right, forward
Next_waypoint: None, left, right, forward

Capturing 4 inputs per state with each input having a variation between 2-4, gives us 128 states in total that exist for the smartcab in this environment.


## Implement a Q-Learning Driving Agent
With your driving agent being capable of interpreting the input information and having a mapping of environmental states, 
your next task is to implement the Q-Learning algorithm for your driving agent to choose the best action at each time step, 
based on the Q-values for the current state and action. 

Each action taken by the smartcab will produce a reward which depends on the state of the environment. 
The Q-Learning driving agent will need to consider these rewards when updating the Q-values. Once implemented, 
set the simulation deadline enforcement enforce_deadline to True. Run the simulation and observe how the smartcab moves about the environment in each trial.

**QUESTION:**

What changes do you notice in the agent's behavior when compared to the basic driving agent when random actions were always taken? 
Why is this behavior occurring?

**Answer:**

At the beginning of trials the agent's behavior remains the same; however, as trials proceed, the agent no longer seems to act randomly but its movement
tends towards the destination.

Behvaior - learning from it's past experience, Q table starts off empty and as the agent explores its world each state, action and its reward,
it's q value, is stored. As more q values are stored the agent becomes at choosing the best action.

With no reward for making it to the destination sooner rather than later, the agent attempts to maximize reward following waypoints 
that may not result in the shortest path to the destination.


## Improve the Q-Learning Driving Agent
Your final task for this project is to enhance your driving agent so that, after sufficient training, 
the smartcab is able to reach the destination within the allotted time safely and efficiently. 
Parameters in the Q-Learning algorithm, such as the learning rate (alpha), 
the discount factor (gamma) and the exploration rate (epsilon) all contribute to the driving agent’s ability to learn the best action for each state. 
To improve on the success of your smartcab:

- Set the number of trials, n_trials, in the simulation to 100.
- Run the simulation with the deadline enforcement enforce_deadline set to True (you will need to reduce the update delay update_delay and set the display to False).
- Observe the driving agent’s learning and smartcab’s success rate, particularly during the later trials.
- Adjust one or several of the above parameters and iterate this process.

This task is complete once you have arrived at what you determine is the best combination of parameters required for your driving agent to learn successfully.

**QUESTION:** 

Report the different values for the parameters tuned in your basic implementation of Q-Learning. 
For which set of parameters does the agent perform best? How well does the final driving agent perform?

No. of Trials = 10, alpha = 0.5, epsilon = 0.5, gamma = 0.4
Reached Destination | Ran out of Time
--- | ---
31 | 19
30 | 20
35 | 15
27 | 23
33 | 17

No. of Trials = 10, alpha = 0.1, epsilon = 0.2, gamma = 0.3
Reached Destination | Ran out of Time
--- | ---
35 | 15
41 | 9
37 | 13
35 | 15
40 | 10

No. of Trials = 10, alpha = 0.1, epsilon = 0.2, gamma = 0.3



**QUESTION:**
Does your agent get close to finding an optimal policy, i.e. reach the destination in the minimum possible time, 
and not incur any penalties? How would you describe an optimal policy for this problem?

**Answer:**