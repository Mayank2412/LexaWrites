### Chapter 7: Seven-Day Cumulative Depletion & Reserve Auditing

The logistics structure of the Roman military apparatus relies upon continuous auditing of supply schedules, grain consumption rates, and pack train payload limits. Operational survival across extended operational theaters requires strict mathematical accounting of daily resource expenditures against static reserve capacities. This chapter synthesizes the complete seven-day supply schedule matrix, quantifying the daily mass balance between grain consumption, regional foraging yields, and the resulting net reserve draw imposed upon the transport train. 

Every operational deployment calculates mass flows through deterministic parameters. The baseline active personnel count within the legion footprint ($N_{legion}$) remains fixed at 5,000 individuals. Each soldier requires a daily grain consumption baseline ($C_{daily}$) of 1.5 kilograms. Multiplying these baseline figures yields a constant daily consumption rate of 7,500 kilograms across the entire operational footprint. This total consumption represents an unavoidable thermodynamic and metabolic outflow that must be balanced either through local extraction within the maximum effective operational foraging radius ($R_{forage}$), set at 12.0 kilometers, or through direct withdrawals from the mobile logistics train.

The mobile logistics train itself possesses a finite carrying capacity. With 1,200 mules per legion carrying a maximum payload capacity of 100 kilograms each, the total initial transport capacity ($total\_train\_capacity\_kg$) is capped at 120,000 kilograms. Because the transport train must simultaneously carry water, repair equipment, military hardware, and structural tools, the grain reserves stored within the train diminish rapidly when local foraging yields drop below the daily consumption requirement of 7,500 kilograms. 

To evaluate systemic sustainability, the supply schedule matrix records daily metrics across a standard seven-day operational cycle. The variables tracked include daily marching distance, total grain consumed, local forage yield acquired, and the resulting net reserve draw. The marching velocity under full auxiliary load ($V_{march}$) is established at 25.0 kilometers per day, though tactical constraints or terrain variations occasionally throttle this rate downward to preserve personnel endurance and limit caloric burn.

The following Markdown table details the complete seven-day operational schedule, displaying the exact progression of consumption, yield, and reserve draw across the designated timeframe:

| Day | Marching Distance (km) | Grain Consumed (kg) | Forage Yield (kg) | Net Reserve Draw (kg) |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 25 | 7500 | 3200 | 4300 |
| 2 | 25 | 7500 | 2900 | 4600 |
| 3 | 20 | 7500 | 4100 | 3400 |
| 4 | 25 | 7500 | 1800 | 5700 |
| 5 | 15 | 7500 | 5200 | 2300 |
| 6 | 25 | 7500 | 2500 | 5000 |
| 7 | 20 | 7500 | 3800 | 3700 |

Analysis of the tabular matrix reveals distinct operational phases governed by local agricultural density and marching velocity adjustments. On Day 1, the legion executes a standard 25-kilometer march, consuming 7,500 kilograms of grain. Local foraging parties deployed within the 12-kilometer radius recover 3,200 kilograms of usable grain and feedstuffs. The deficit between consumption and local acquisition forces a net reserve draw of 4,300 kilograms from the transport train. 

On Day 2, foraging yields contract slightly to 2,900 kilograms while the marching distance remains at 25 kilometers. The consumption rate remains constant at 7,500 kilograms, resulting in an increased net reserve draw of 4,600 kilograms. Day 3 introduces a minor adjustment in marching distance down to 20 kilometers, which correlates with an increased foraging yield of 4,100 kilograms. Consequently, the net reserve draw drops to 3,400 kilograms, providing temporary relief to the pack train.

Day 4 presents an environmental contraction characterized by depleted local resources or arid corridor transit. Foraging yields plummet to 1,800 kilograms. Despite standard consumption, the net reserve draw spikes to 5,700 kilograms, representing the single highest daily depletion rate within the standard operational cycle. This steep draw significantly taxes the remaining inventory of the 120,000-kilogram train capacity.

Day 5 demonstrates the operational necessity of velocity throttling. The marching distance is reduced to 15 kilometers, which decreases overall physical fatigue and extends the duration available for foraging patrols. This operational pause yields a peak recovery of 5,200 kilograms of grain and supplies. The corresponding net reserve draw drops to a cycle low of 2,300 kilograms, partially replenishing the security margin of the logistics train.

Day 6 returns to a standard 25-kilometer marching velocity. Foraging yields contract back to 2,500 kilograms, forcing a heavy net reserve draw of 5,000 kilograms. Finally, Day 7 records a 20-kilometer march with a moderate foraging yield of 3,800 kilograms, concluding the weekly cycle with a net reserve draw of 3,700 kilograms.

Summing the net reserve draws across the seven-day period provides the aggregate depletion figure imposed upon the logistics train. The cumulative draw totals 29,000 kilograms of grain over the course of the week. Logistics commanders audit this cumulative figure against the remaining capacity of the 1,200 pack mules to determine whether intermediate supply depots must be established or if the legion must alter its route to intersect river transport networks.

The mathematical relationship governing cumulative reserve depletion ($D_{cumulative}$) can be expressed as the summation of daily consumption minus daily forage yield:

$$D_{cumulative} = \sum_{i=1}^{7} (C_{daily} \cdot N_{legion} - Y_{forage}(i))$$

Where $C_{daily} \cdot N_{legion}$ equals the constant 7,500 kilograms, and $Y_{forage}(i)$ represents the variable daily yield observed on day $i$. Substituting the tabulated values yields:

$$D_{cumulative} = 4300 + 4600 + 3400 + 5700 + 2300 + 5000 + 3700 = 29000 \text{ kg}$$

This total draw of 29,000 kilograms represents slightly over twenty-four percent of the initial 120,000-kilogram maximum transport capacity of the entire pack mule train. Under isolated operating conditions without resupply, a legion operating at this consumption and deficit rate exhausts its primary grain inventory within approximately twenty-nine days. Therefore, the audit data derived from this seven-day schedule dictates that operational planning must mandate a resupply interval or secondary agricultural requisition point well before the conclusion of a four-week march.

Variations in regional yield directly dictate the operational lifespan of the military force. If prolonged deployment through arid terrain causes sustained Day 4 conditions where forage yields remain below 2,000 kilograms for multiple consecutive cycles, the cumulative draw accelerates past the structural limits of the pack train. Logistics doctrine addresses this vulnerability through mandatory velocity throttling, detachment of secondary foraging cohorts, and the enforcement of strict nutritional rationing when reserve thresholds approach terminal boundaries.

The integration of marching velocity, foraging radii, and daily consumption matrices forms a closed-loop deterministic system. By continuously auditing net reserve draws against transport capacity, Roman logistics management maintains operational continuity across diverse geographical theaters. The data presented in the schedule above establishes the baseline parameters required for calculating long-range strategic deployment limits.