/* Part of GBADoom (https://github.com/doomhack/GBADoom), a modification of PrBoom.
 * This file carried no license notice in the GBADoom release. PrBoom is distributed
 * under the GNU General Public License, version 2 or (at your option) any later
 * version, and this file is redistributed here as part of that work under the same
 * terms. NXP claims no copyright in this file. See COPYING.
 * SPDX-License-Identifier: GPL-2.0-or-later
 */
#include <stdlib.h>
#include "global_data.h"

#include "z_zone.h"


globals_t* _g = NULL;

void InitGlobals()
{
    _g = Z_Malloc(sizeof(globals_t), PU_STATIC, NULL);

    memset(_g, 0, sizeof(globals_t));

    #include "global_init.h"
}
