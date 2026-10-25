/* Cortex-A7 ARMv7-A bare-metal execution probe.
 * SPDX-License-Identifier: MIT
 *
 * Entry address: 0x40000000 (must be explicitly configured by the loader).
 * Mailbox: 0x40001000. Does not enable IRQs.
 */
.syntax unified
.cpu cortex-a7
.arm
.section .text.boot, "ax", %progbits
.global _start
.type _start, %function
_start:
    ldr sp, =0x40010000
    ldr r0, =0x40001000
    ldr r1, =0x48325031  /* "H2P1" execution marker */
    str r1, [r0]
1:
    wfi
    b 1b
.size _start, . - _start
