# Doom-MCX port of popular Doom game to run on NXP MCX microcontrollers

A port of prBoom to NXP MCXN MCU running Zephyr RTOS

![MCX-Doom](https://raw.githubusercontent.com/NXPHoverGames/Doom-MCX/refs/heads/main/assets/doom_mcx.jpg)

<!----- Boards ----->
[![License badge](https://img.shields.io/badge/License-see%20section%208-red)](#step8)
![Language badge](https://img.shields.io/badge/Language-C-yellow)
[![Board badge](https://img.shields.io/badge/Board-FRDM&ndash;MCXN947-blue)]()
[![Category badge](https://img.shields.io/badge/Category-RTOS-yellowgreen)](https://github.com/search?q=org%3Anxp-appcodehub+rtos+in%3Areadme&type=Repositories)
[![Category badge](https://img.shields.io/badge/Category-HMI-yellowgreen)](https://github.com/search?q=org%3Anxp-appcodehub+hmi+in%3Areadme&type=Repositories)
[![Category badge](https://img.shields.io/badge/Category-GRAPHICS-yellowgreen)](https://github.com/search?q=org%3Anxp-appcodehub+graphics+in%3Areadme&type=Repositories)

![Demo](https://raw.githubusercontent.com/NXPHoverGames/Doom-MCX/refs/heads/main/assets/demo.gif)

## Table of Contents
1. [Software](#step1)
2. [Hardware](#step2)
3. [Setup](#step3)
4. [Results](#step4)
5. [FAQs](#step5) 
6. [Support](#step6)
7. [Release Notes](#step7)
8. [License](#step8)

## 1. Software<a name="step1"></a>
- Zephyr 4.4.2
- Zephyr SDK version 1.0.1


## 2. Hardware<a name="step2"></a>

![FRDM-MCXN947](https://raw.githubusercontent.com/NXPHoverGames/Doom-MCX/refs/heads/main/assets/FRDM-MCXN947-TOP.avif) | ![LCD-PAR-S035](https://raw.githubusercontent.com/NXPHoverGames/Doom-MCX/refs/heads/main/assets/LCD-PAR-S035-TOP.avif)
:-------------------------:|:-------------------------:
[FRDM Development Board for MCX N947](https://www.nxp.com/design/design-center/development-boards-and-designs/general-purpose-mcus/frdm-development-board-for-mcx-n94-n54-mcus:FRDM-MCXN947)  |  [LCD-PAR-S035 480x320 IPS LCD](https://www.nxp.com/design/design-center/development-boards-and-designs/general-purpose-mcus/3-5-480x320-ips-tft-lcd-module:LCD-PAR-S035)

Optional [Joystick shield](https://duckduckgo.com/?t=h_&q=funduino+board+joystick+shield&ia=web) on FRDM-MCXN947 Arduino Header



## 3. Setup<a name="step3"></a>


Before getting started, make sure you have a proper Zephyr development
environment. Follow the official
[Zephyr Getting Started Guide](https://docs.zephyrproject.org/latest/getting_started/index.html).

> [!NOTE]  
> DOOM-MCX has been tested on Zephyr SDK version 1.0.1. When installing the sdk it's recommended to specify the version using `west sdk install --version 1.0.1`

### Initialization

The first step is to initialize the DOOM-MCX Zephyr workspace folder (``doom-mcx-workspace``) where ``doom-mcx`` and all Zephyr modules will be cloned. Run the following
command:

```shell
# initialize  for the example-application (main branch)
west init -m https://github.com/nxphovergames/doom-mcx --mr main doom-mcx-workspace
# update Zephyr modules
cd doom-mcx-workspace
west update
```

### The game data

The game data lives in `wad/doom1.wad`. It contains the game data of the Doom shareware
episode converted with [GbaWadUtil](https://github.com/doomhack/GbaWadUtil) into the
layout this engine reads (levels in the engine's native structures, sound lumps omitted),
so a stock `doom1.wad` cannot be used directly; other IWADs (registered Doom, Doom II,
Final Doom) can be converted with the same tool.
It is not linked into the firmware; it is a separate binary that is flashed to the
external QSPI flash at 0x90000000 and read in place from there. The game data is
copyright id Software; see `wad/doom-wad-shareware-license.txt` and section 8.

### Building

To build the application, run the following command:

```shell
cd doom-mcx
west build -p always -b frdm_mcxn947/mcxn947/cpu0
```

Besides the application, the build produces `build/zephyr/doom1.hex`, the IWAD converted
to an Intel hex at the external flash address.

Set `CONFIG_DOOM_SPLASH_TEXT` to change the text of the startup splash.

### Flashing

> [!NOTE]  
> [NXP Linkserver](https://www.nxp.com/design/design-center/software/development-software/mcuxpresso-software-and-tools-/linkserver-for-microcontrollers:LINKERSERVER) v1.5.30 or newer has to be installed. See [Zephyr LinkServer guide](https://docs.zephyrproject.org/latest/develop/flash_debug/host-tools.html#linkserver-debug-host-tools) for more information.

Flashing takes two steps. Connect a USB-C cable to the "MCU-Link" USB-C port, then flash
the application to the internal flash:

```shell
west flash
```

and the IWAD to the external flash at 0x90000000:

```shell
west flash --no-erase --hex-file build/zephyr/doom1.hex
```

`--no-erase` keeps the application that was just written; without it the runner mass
erases the device first. The IWAD only has to be re-flashed when `wad/doom1.wad` changes.


## 4. Results<a name="step4"></a>
On a successful flash the display (LCD-PAR-S035) should turn and you can start playing the game.

## 5. FAQs<a name="step5"></a>

### Doom-MCX Controls

Doom-MCX supports 2 types of control either through touchscreen or the [Joystick shield](https://duckduckgo.com/?t=h_&q=funduino+board+joystick+shield&ia=web).

#### Touchscreen controls
**Open doors/start:** Tap "Use Area"  
**Fire:** Tap "Fire Area"  
**Wake & Strafe** Tap and drag in the "Virtual Joystick Area"

![Doom-MXC Touch screen layout](https://raw.githubusercontent.com/NXPHoverGames/Doom-MCX/refs/heads/main/assets/doom_mcx_touch_screen_layout.jpg)

> [!CAUTION]  
> When using the Funduino shield make sure the switch is in 3V3 mode, otherwise you will damage the board.

#### Joytick Shield controls
**Fire:** D  
**Use:** C  
**Walk:** Joystick Y-axis  
**Strafe:** Joystick X-axis  
**Menu:** A

## 6. Support<a name="step6"></a>

Questions regarding the content/correctness of this example can be entered as Issues within this GitHub repository.

>**Warning**: For more general technical questions regarding NXP Microcontrollers and the difference in expected functionality, enter your questions on the [NXP Community Forum](https://community.nxp.com/)

[![Follow us on Youtube](https://img.shields.io/badge/Youtube-Follow%20us%20on%20Youtube-red.svg)](https://www.youtube.com/NXP_Semiconductors)
[![Follow us on LinkedIn](https://img.shields.io/badge/LinkedIn-Follow%20us%20on%20LinkedIn-blue.svg)](https://www.linkedin.com/company/nxp-semiconductors)
[![Follow us on Facebook](https://img.shields.io/badge/Facebook-Follow%20us%20on%20Facebook-blue.svg)](https://www.facebook.com/nxpsemi/)
[![Follow us on Twitter](https://img.shields.io/badge/X-Follow%20us%20on%20X-black.svg)](https://x.com/NXP)


# Simulation on PC

Zephyr RTOS also provides a native_posix target

To compile as native type:
```shell
west build -p always -b native_sim/native/64
```

To run type
```shell
cd doom-mcx
./build/zephyr/zephyr.exe --wad=wad/doom1.wad
```

`--wad` defaults to `wad/doom1.wad`, so a bare `./build/zephyr/zephyr.exe` started from
the repository root picks up the IWAD as well.

### native_posix controls
**Fire:** CTRL  
**Use:** Spacebar  
**Walk:** Up-arrow & Down-arrow  
**Strafe:** Left-arrow & Right-arrow  
**Menu:** ESC

![MCX-Doom Native](https://raw.githubusercontent.com/NXPHoverGames/Doom-MCX/refs/heads/main/assets/mcx_doom_zephyr_native_posix.png)

## 7. Release Notes<a name="step7"></a>
| Version | Description / Update                           | Date                        |
|:-------:|------------------------------------------------|----------------------------:|
| 1.0     | Initial release                                | September 12<sup>th</sup> 2026 |

## 8. License<a name="step8"></a>

This repository distributes source code and game data only; no firmware images are
distributed. Building an image and flashing it to a board is done by the developer. The
components that go into an image and their licenses are listed in `SCR.txt`.

- The game engine (`prboom2/`) is distributed under the GNU General Public License,
  version 2 or (at your option) any later version, as stated in the notices in its source
  files; see `COPYING`. It is derived from id Software's 1999 GPL release of the Doom
  source, PrBoom 2.5.0 and GBADoom. Files under `prboom2/` that carry a
  "Copyright 2024 NXP" line were modified by NXP for this port; the changes are recorded
  in the git history.
- NXP's own files (`src/`, build and board files, `scripts/`) are available under
  `Apache-2.0 OR GPL-2.0-or-later`.
- A build links Zephyr RTOS (Apache-2.0), the NXP HAL (BSD-3-Clause), CMSIS (Apache-2.0),
  picolibc (BSD-3-Clause, MIT) and libgcc (GPL-3.0-or-later with the GCC Runtime Library
  Exception). See `SCR.txt` for the component register and `LICENSES/` for the texts.
- `wad/doom1.wad` contains the game data of the Doom shareware episode, converted by the
  GBADoom project's tool [GbaWadUtil](https://github.com/doomhack/GbaWadUtil) into the
  layout this engine reads: levels in the engine's native structures, sound lumps
  omitted, plus the engine's own resource lumps from the GBADoom project. The game data is
  copyright id Software; the shareware license text that accompanies the shareware
  release is reproduced in `wad/doom-wad-shareware-license.txt`. The file is not part of
  the GPL-licensed engine and is flashed separately. An equivalent file can be generated
  from your own shareware or registered IWAD with GbaWadUtil.

Anyone who distributes a built image is responsible for determining and complying with
the license terms that apply to that combination.

DOOM is a trademark of id Software LLC. This project is not affiliated with, sponsored by,
or endorsed by id Software or ZeniMax Media. Zephyr is a trademark of The Linux
Foundation.
