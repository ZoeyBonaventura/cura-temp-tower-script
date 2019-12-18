# cura-temp-tower-script

### Installation

Copy TempTower.py into your cura directory like the following;

C:\Program Files\Ultimaker Cura \<version\>\plugins\PostProcessingPlugin\scripts

### Use

This script is based on the script written by [Okke Formsma](https://github.com/okke-formsma) here <https://github.com/okke-formsma/cura-temp-tower-script>

Five settings are available;

1. Start Height
2. Start Temperature
3. Layer Height
4. Height Increment
5. Temperature Increment

So, if you have a tower with a base layer **1.5mm** thick and goes down from **260 °C** (base) to **220 °C** (top) in steps of **5 °C** every **10mm** with a layer height of **0.2mm**, set:

* Start height: **1.5mm**
* Start Temperature **260 °C**
* Layer height: **0.2mm**
* Height Increment **10mm**
* Temperature Increment **-5 °C**