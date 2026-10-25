### Chapter 3: The 10,000-Volt Copper Spine and Seawater Grounding
Optically pure silica glass can transport photons across intercontinental distances, but the optical amplifiers spaced along the route require electrical power to function. Without active power feeding, every repeater on the ocean floor falls dark within milliseconds. Pumping electricity across a distance of thousands of kilometers requires a closed electrical circuit. Undersea cable engineers solve this physics problem by using the global ocean itself as a return path, completing a planetary-scale electrical loop driven by land-based generators.

#### The Power Feeding Equipment Architecture
Shore stations house Power Feeding Equipment that pushes 10,000V DC at 1.1 Amps into the core of the transmission line. The central element responsible for conducting this high-voltage current is a welded copper tube positioned just beneath the outer protective layers. This copper spine acts as a continuous series bus, delivering electrical energy directly to the optical amplifiers positioned at regular intervals along the seabed. 

The electrical circuit relies on a dual-ended feed during normal operations. Both shore ends of the cable inject voltage into the copper conductor, meeting somewhere in the middle of the ocean. Because the circuit draws a constant 1.1 Amps, the voltage drop scales predictably with the total resistance of the thousands of kilometers of copper conductor. 

#### Seawater as the Electrical Return Path
To complete the circuit without dedicating half of the cross-sectional area to a return wire, the system exploits the conductive properties of seawater. 

> A high-voltage subsea power system does not care about the origin of its ground loop; it cares only that the earth and the ocean remain a lower-resistance path back to the shore station than any stray structural metal on the continental shelf.

At each terminal station, massive copper plates or titanium mesh electrodes are sunk deep into the seabed or buried in the coastal surf zone. These ground beds sink or source the 1.1 Amps directly into the ocean water. The conductivity of saline water handles the return current over the thousands of miles between repeaters, dropping the need for a dedicated return conductor inside the 17 mm cable profile and preserving precious physical space for optical fiber pairs.

#### Surviving Insulation Breaches and Ground Faults
Marine environments are inherently hostile to high voltages, and insulation failure is a statistical certainty over a 25-year design lifespan. When an anchor strike, abrasion, or component fatigue breaches the outer polyethylene insulation, the 10,000V DC conductor makes direct electrical contact with seawater. 

This event creates a ground fault, causing the current to leak into the ocean at the point of damage rather than completing the full transit to the opposite shore. When a fault occurs, the power system shifts from dual-ended feeding to single-end power feeding. The surviving shore station ramps up its output voltage to maintain the required 1.1 Amps through the truncated circuit, pushing power as far down the line as the fault location allows. While repeaters beyond the fault point power down, the segment between the functional shore station and the fault remains operational. This tolerance ensures that a localized insulation breach does not take down the entire intercontinental trunk, buying operators days or weeks to mobilize a repair ship while maintaining partial data flow.