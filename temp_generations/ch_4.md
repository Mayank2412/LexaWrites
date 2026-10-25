### Chapter 4: Wavelength Division Multiplexing and 384-Terabit Capacity

Physical silica glass does not care about data packets, IP addresses, or streaming video; it cares only about the frequency of the electromagnetic waves injected into it. To maximize the return on a capital expenditure spanning thousands of kilometers of ocean floor, modern transoceanic infrastructure exploits the optical properties of the 1550 nm C-band window, where silica attenuation reaches its absolute minimum. Pushing raw binary data through a single laser beam leaves massive swaths of optical bandwidth unused. The solution is Wavelength Division Multiplexing, a method that slices the spectrum into distinct color wavelengths, turning a single strand of glass into a multi-lane optical highway.

#### Spectrum Splitting within the C-Band

The 1550 nm window offers a low-loss transmission band, but lasers tuned to a single frequency would bottleneck the entire multi-billion-dollar asset. Wavelength Division Multiplexing solves this by deploying specialized transceivers at the cable landing stations that emit dozens of discrete laser frequencies simultaneously into the same glass core. Each wavelength acts as an independent carrier channel, separated by precise nanometer or gigahertz spacings to prevent optical cross-talk and signal degradation. 

> Optical bandwidth is cheap to multiply via multiplexing, but terminal electronics at the shore stations remain painfully expensive. You do not buy capacity by the meter; you pay for every gigahertz of laser modulation terminating on the beach.

At the transmitting terminal, a multiplexer combines these distinct laser colors into a single composite beam before injection into the fiber. At the receiving terminal, a matching array of prisms or diffraction gratings acts as a demultiplexer, separating the composite beam back into individual wavelengths and routing them to dedicated photodetectors. The physical glass strand remains unaltered, yet its utility multiplies by the number of active laser channels sharing the medium.

#### Multiplying Pairs for Aggregate Yield

Scaling total capacity requires scaling the physical architecture inside the cable bundle. A standard intercontinental trunk contains 16 fiber pairs per cable. Each individual fiber pair is engineered to sustain a throughput of 24 Tbps. 

The arithmetic of modern undersea bandwidth relies on two primary variables operating in parallel:
- The color count of distinct laser wavelengths multiplexed into the C-band window
- The total count of active fiber pairs housed within the central protection tubes

Multiplying the capacity of a single pair by the total system pairs yields a total system capacity of 384 Tbps across the complete transoceanic assembly. Every single gigabit of this capacity must share the electrical power budget supplied by the copper spine and the physical constraints of the optical amplifiers spaced along the abyssal plain.

#### The Thermal and Optical Ceiling

Pushing 384 Tbps through an intercontinental pipeline is not constrained by the glass itself, but by the physics of signal-to-noise ratios and nonlinear optical effects in silica. As laser power increases to support higher modulation formats like 64-QAM, nonlinear phenomena such as Four-Wave Mixing and Stimulated Brillouin Scattering begin to distort the phase of the light signals. 

These distortions introduce bit errors that repeaters cannot easily filter out. Engineers must balance launch power against the noise figure of the Erbium-Doped Fiber Amplifiers. Exceeding the linear limits of the glass turns the fiber into a chaotic optical mixer, corrupting the very data streams it was deployed to carry.