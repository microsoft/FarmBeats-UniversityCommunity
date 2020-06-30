# ClosedLoopIrrigation
FarmBeats Azure Function to make Irrigation Decisions in an orchard setting without need for user input.

## Components of the Azure Function
- A connection to the Farm Beats API to get sensor values
- A simple and extensible decision framework on what to do with sensor values(and weather forecast information in the future)
- A API call to an irrigation controller to irrigate the orchard (Rachio in my case, but could be any that implements the IIrrigationControl interface)
 
## Requirements
 - FarmBeats Subscription
 - Sensors connected to the FarmBeats Subscription
 - Irrigation Controller (this could be as simple as an email to someone on the farm with the block and duration to irrigate)
 
 
## This setup used the following components
 - SEEED Sensor box V2 with a soil moisture sensor
 - LoRA Gateway connected to Intel Up2
 - FarmBeats Subscription
 - Rachio Irrigation controller
 - RainBird Irrigation control valves (https://store.rainbird.com/valves/sprinkler-valves/100hvfss-1-in-hvf-series-inline-sprinkler-valve-with-flow-control-slip-x-slip.html)
 - RainBird Irrigation drip tubing 1 gph per drip location at 6 inch spacing.
 
