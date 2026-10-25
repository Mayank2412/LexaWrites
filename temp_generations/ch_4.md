### Chapter 4: Wavelength Division Multiplexing and 384-Terabit Capacity

Undersea fiber optic cables form the physical backbone of global internet traffic, carrying 99 percent of intercontinental data. To achieve a total system capacity of 384 Tbps within a cable core measuring only millimeters across, modern transoceanic networks rely on advanced optical engineering. Instead of transmitting a single stream of data down each strand of glass, systems use Wavelength Division Multiplexing (WDM) to pack massive volumes of information through a finite optical path.

#### Harnessing the C-Band Window

Silica glass is exceptionally transparent to infrared light, but it is not uniformly permeable across all frequencies. Optical engineers target the 1550 nm C-band window, where attenuation drops to 0.15 dB/km. Operating within this narrow optical window allows laser pulses to travel tens of kilometers before requiring regeneration. 

However, sending just one laser beam through a fiber pair would underutilize the medium's carrying capacity. WDM solves this bottleneck by splitting the 1550 nm window into dozens of distinct color wavelengths. Each wavelength operates as an independent optical carrier channel. A single fiber pair can transport multiple data streams simultaneously without interference, provided the laser frequencies maintain precise spacing. 

#### Scaling to Terabit Speeds

A typical deep-sea cable contains 16 fiber pairs per cable. By routing independent WDM channels across every fiber pair, capacity scales exponentially. 

> **System Specs:**
> - Fiber pairs per cable: 16
> - Capacity per pair: 24 Tbps
> - Total system capacity: 384 Tbps
> - Target operational window: 1550 nm C-band

Achieving 24 Tbps per pair requires tight control over optical dispersion and signal-to-noise ratios. As multiple high-power laser wavelengths travel down the core of the silica optical fibers, nonlinear optical effects can occur. Photons interact with the glass lattice and with each other, causing phase shifts and cross-talk between adjacent channels. Transmitters must employ advanced coherent detection schemes and digital signal processing (DSP) at the cable landing stations to compensate for these distortions upon arrival.

#### Managing Thermal and Power Constraints

Packing dense laser arrays into underwater systems introduces strict operational parameters. The laser sources and transceivers located at terminal stations generate substantial heat, requiring precise temperature regulation. Meanwhile, the optical amplifiers spaced across the ocean floor must boost every wavelength simultaneously without introducing excessive thermal noise or signal degradation. 

By multiplexing distinct color channels through the 1550 nm C-band window, subsea infrastructure maximizes the physical limits of silica glass. This optical multiplexing strategy ensures that intercontinental networks can handle escalating global data demands without requiring an expansion of the physical cable footprint on the ocean floor.