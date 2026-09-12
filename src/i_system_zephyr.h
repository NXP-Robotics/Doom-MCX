/* Emacs style mode select   -*- C++ -*-
 *-----------------------------------------------------------------------------
 *
 *  Copyright 2024 NXP
 *
 *  SPDX-License-Identifier: Apache-2.0 OR GPL-2.0-or-later
 *
 *-----------------------------------------------------------------------------
 */

#ifndef HEADER_I_SYSTEM_ZEPHYR
#define HEADER_I_SYSTEM_ZEPHYR

#ifdef __cplusplus
extern "C" {
#endif

typedef unsigned char byte;

void I_InitScreen_zephyr();

void I_CreateBackBuffer_zephyr();

int I_GetVideoWidth_zephyr();

int I_GetVideoHeight_zephyr();

void I_FinishUpdate_zephyr(const byte* srcBuffer, const byte* pallete, const unsigned int width, const unsigned int height);

void I_SetPallete_zephyr(const byte* pallete);

void I_ProcessKeyEvents();

void I_InitIwad_zephyr(void);

void I_Error (const char *error, ...);

void I_Quit_zephyr();

unsigned short* I_GetBackBuffer();

unsigned short* I_GetFrontBuffer();

#ifdef __cplusplus
}
#endif


#endif
