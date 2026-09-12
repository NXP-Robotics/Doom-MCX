/* Emacs style mode select   -*- C++ -*-
 *-----------------------------------------------------------------------------
 *
 *
 *  Derived from gba_functions.h of GBADoom (https://github.com/doomhack/GBADoom),
 *  which carried no license notice and is redistributed under the terms of PrBoom,
 *  GNU GPL version 2 or (at your option) any later version.
 *  Modifications Copyright 2024 NXP.
 *
 *  This program is free software; you can redistribute it and/or
 *  modify it under the terms of the GNU General Public License
 *  as published by the Free Software Foundation; either version 2
 *  of the License, or (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
 *  02111-1307, USA.
 *
 * DESCRIPTION: Main game control interface.
 *-----------------------------------------------------------------------------*/

#ifndef OS_FUNCTIONS_H
#define OS_FUNCTIONS_H

#include <string.h>
#include "doomtype.h"
#include "m_fixed.h"


inline static CONSTFUNC int IDiv32 (int a, int b)
{
    return a / b;
}

inline static void BlockCopy(void* dest, const void* src, const unsigned int len)
{
    memcpy(dest, src, len & 0xfffffffc);
}

inline static void CpuBlockCopy(void* dest, const void* src, const unsigned int len)
{
    BlockCopy(dest, src, len);
}

inline static void BlockSet(void* dest, volatile unsigned int val, const unsigned int len)
{
    memset(dest, val, len & 0xfffffffc);
}

inline static void ByteCopy(byte* dest, const byte* src, unsigned int count)
{
    do
    {
        *dest++ = *src++;
    } while(--count);
}

inline static void ByteSet(byte* dest, byte val, unsigned int count)
{
    do
    {
        *dest++ = val;
    } while(--count);
}

inline static void* ByteFind(byte* mem, byte val, unsigned int count)
{
    do
    {
        if(*mem == val)
            return mem;

        mem++;
    } while(--count);

    return NULL;
}

inline static void SaveNonVolatile(const byte* eeprom, unsigned int size, unsigned int offset)
{
    //TODO Store to file
}

inline static void LoadNonVolatile(byte* eeprom, unsigned int size, unsigned int offset)
{
    //TODO Load from file
}

#define ScreenYToOffset(x) (x * SCREENWIDTH)

#endif // OS_FUNCTIONS_H
