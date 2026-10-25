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
    /* UART0 is 16550-compatible with 32-bit spaced registers. */
    ldr r2, =0x01c28000
    adr r3, uart_message
2:
    ldrb r4, [r3], #1
    cmp r4, #0
    beq 1f
3:
    ldr r5, [r2, #0x14]  /* LSR, reg 5 shifted by 2 */
    tst r5, #0x20        /* THRE */
    beq 3b
    strb r4, [r2]       /* THR */
    b 2b
1:
    wfi
    b 1b
.size _start, . - _start

.align 2
uart_message:
    .asciz "H2 UART OK\\n"
