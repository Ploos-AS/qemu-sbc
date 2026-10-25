# H2+ Cortex-A7 guest execution: next implementation milestone

## Current verified baseline

The independent `orangepi-zero-lts-h2` machine on pinned QEMU v10.0.0
has Cortex-A7, 256 MiB DRAM at `0x40000000`, GICv2 and UART0.
QTest verifies the UART0 THRE interrupt reaches SPI0 (interrupt ID 32),
is visible in GICC_HPPIR, is acknowledged in GICC_IAR, and returns to
spurious ID 1023 after UART interrupt disable and EOIR.

**Important:** QTest accesses device registers from the host. It does
not prove the guest CPU has executed an instruction or taken an IRQ.

## First guest-execution acceptance test

1. Define and document a deterministic reset entry point in mapped memory.
   Do not assume the Cortex-A7 reset PC points into DRAM.
2. Provide an explicit, minimal raw guest-image loading path in the
   independent machine, with a fixed entry address and no dependency on
   Allwinner H3 firmware or another board's boot ROM.
3. Cross-assemble a tiny ARMv7-A bare-metal image. It must install an
   exception vector table, initialize separate SVC and IRQ stacks, and
   enable IRQs only after the GIC distributor and CPU interface are ready.
4. The guest writes a distinct magic value into a reserved DRAM mailbox
   after reaching its entry point. QTest reads this mailbox and fails if
   the value is absent. This proves actual guest instruction execution.
5. The guest enables UART0 THRE interrupt and GIC SPI0, handles interrupt
   ID 32, writes a second mailbox value, disables the UART source,
   sends EOIR, and returns from the IRQ handler.
6. QTest checks both mailbox values and a bounded timeout; no test may
   pass solely because host-side QTest wrote the values.

## Implementation constraints

- Preserve the existing MMIO/register tests as a separate fast smoke test.
- Keep the pinned QEMU source and machine registration deterministic.
- Check reset vector placement and ARM exception mode explicitly before
  enabling interrupts.
- Avoid claiming Linux boot until a kernel is actually entered and emits
  observable output. Device tree, clock/reset control, storage and other
  peripherals remain outside the current hardware model.
- The next patch should implement the loader/reset path first, then the
  guest mailbox smoke test, and only then the guest IRQ test.
