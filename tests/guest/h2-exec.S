/* Cortex-A7 ARMv7-A bare-metal execution probe.
 * SPDX-License-Identifier: MIT
 *
 * Entry address: 0x40000000 (must be explicitly configured by the loader).
 * Mailbox: 0x40001000. IRQ probe marker: 0x40001004.
 */
.syntax unified
.cpu cortex-a7
.arm
.section .text.boot, "ax", %progbits
.global _start
.type _start, %function
_start:
    b reset_entry
    b .                  /* undefined */
    b .                  /* SVC */
    b .                  /* prefetch abort */
    b .                  /* data abort */
    b .                  /* reserved */
    b irq_entry
    b .                  /* FIQ */
reset_entry:
    /* Set VBAR to the vector table at the ELF entry point. */
    ldr r0, =_start
    mcr p15, 0, r0, c12, c0, 0
    isb
    cps #0x12          /* IRQ mode: independent exception stack */
    ldr sp, =0x4000f000
    cps #0x13          /* SVC mode */
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
    /* GICv2: enable UART0 SPI32 and the CPU interface. */
    ldr r6, =0x01c81000
    mov r7, #1
    str r7, [r6, #0x104] /* ISENABLER1, SPI32 */
    str r7, [r6]         /* GICD_CTLR */
    ldr r6, =0x01c82000
    mov r7, #0xff
    str r7, [r6, #4]     /* GICC_PMR */
    mov r7, #1
    str r7, [r6]         /* GICC_CTLR */
    ldr r2, =0x01c28000
    mov r7, #2
    str r7, [r2, #4]     /* UART IER: THRE interrupt */
    cpsie i
4:
    /* IRQ handler writes marker before returning here. */
    ldr r8, =0x40001004
    ldr r9, =0x48324931
6:
    ldr r10, [r8]
    cmp r10, r9
    bne 7f
    ldr r8, =0x40001008
    ldr r9, =0x48325231 /* H2R1: IRQ return confirmed */
    str r9, [r8]
    /* Cortex-A7 physical generic timer: PPI30 (PPI index 14). */
    ldr r6, =0x01c81000
    mov r7, #1
    lsl r7, r7, #30
    str r7, [r6, #0x100] /* GICD_ISENABLER0 */
    ldr r7, =1000000
    mcr p15, 0, r7, c14, c2, 0 /* CNTP_TVAL */
    mov r7, #1
    mcr p15, 0, r7, c14, c2, 1 /* CNTP_CTL ENABLE */
8:
    wfi
    b 8b
7:
    wfi
    b 6b
.size _start, . - _start

.align 2
uart_message:
    .asciz "H2 UART OK\\n"

.align 2
irq_entry:
    sub lr, lr, #4
    push {r0-r3, r12, lr}
    ldr r0, =0x01c82000
    ldr r1, [r0, #0x0c] /* GICC_IAR */
    ubfx r2, r1, #0, #10
    cmp r2, #30
    beq timer_irq
    cmp r2, #32
    bne 5f
    ldr r2, =0x01c28000
    mov r3, #0
    str r3, [r2, #4]    /* Disable UART THRE IRQ */
    ldr r2, =0x40001004
    ldr r3, =0x48324931 /* H2I1 */
    str r3, [r2]
5:
    str r1, [r0, #0x10] /* GICC_EOIR */
    pop {r0-r3, r12, lr}
    subs pc, lr, #0

/* Timer handler shares the saved IRQ context and common EOI path. */
timer_irq:
    mov r3, #0
    mcr p15, 0, r3, c14, c2, 1 /* Disable CNTP_CTL */
    ldr r2, =0x4000100c
    ldr r3, =0x48325431 /* H2T1 */
    str r3, [r2]
    b 5b
