#!/usr/bin/env python3
"""Smoke-test independent H2+ RAM and GICv2 MMIO using QTest.

Interrupt delivery and guest boot are not covered.
"""
import argparse
import select
import subprocess
import os
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--qemu", required=True)
    args = p.parse_args()
    cmd = [args.qemu, "-machine", "orangepi-zero-lts-h2", "-m", "256M",
           "-qtest", "stdio", "-display", "none", "-monitor", "none",
           "-serial", "none", "-S", "-nodefaults"]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=False, bufsize=0)
    try:
        assert proc.stdin is not None and proc.stdout is not None
        proc.stdin.write(b"writel 0x40000000 0x1234abcd\n")
        proc.stdin.flush()
        # QTest is a long-lived protocol: do not wait for QEMU to exit on EOF.
        # Read one response, then terminate the emulator explicitly.
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ QTest RAM read timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if reply != "OK":
            raise RuntimeError(f"RAM write failed: {reply!r}")
        proc.stdin.write(b"readl 0x40000000\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ QTest RAM read timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if not reply.startswith("OK ") or int(reply.split()[1], 0) != 0x1234ABCD:
            raise RuntimeError(f"RAM readback mismatch: {reply!r}")
        # GICv2 distributor ID register: ARM GICv2 returns architecture ID.
        # This probes an actual MMIO device, not just an unmapped zero page.
        proc.stdin.write(b"readl 0x01c81fe8\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ GIC distributor ID read timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if not reply.startswith("OK "):
            raise RuntimeError(f"GIC distributor ID read failed: {reply!r}")
        gic_id = int(reply.split()[1], 0)
        if gic_id == 0:
            raise RuntimeError("GIC distributor ID is zero; device may be unmapped")
        # GIC distributor control: exercise a writable register before IRQ tests.
        # Disable, enable Group 0, and restore disabled state.
        for value in (0, 1, 0):
            proc.stdin.write(f"writel 0x01c81000 {value}\n".encode("ascii"))
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ GIC distributor control write timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if reply != "OK":
                raise RuntimeError(f"GIC distributor control write failed: {reply!r}")
            proc.stdin.write(b"readl 0x01c81000\n")
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ GIC distributor control read timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if not reply.startswith("OK ") or (int(reply.split()[1], 0) & 1) != value:
                raise RuntimeError(f"GIC distributor control mismatch: expected {value}, got {reply!r}")
        # SPI0 is GIC interrupt ID 32. Verify its distributor enable bit.
        # ISENABLER1 at 0x01c81104, ICENABLER1 at 0x01c81184.
        for command, expected in (
            (b"writel 0x01c81184 0x1\n", 0),
            (b"writel 0x01c81104 0x1\n", 1),
            (b"writel 0x01c81184 0x1\n", 0),
        ):
            proc.stdin.write(command)
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ GIC SPI0 enable write timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if reply != "OK":
                raise RuntimeError(f"GIC SPI0 enable write failed: {reply!r}")
            proc.stdin.write(b"readl 0x01c81104\n")
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ GIC SPI0 enable read timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if not reply.startswith("OK ") or (int(reply.split()[1], 0) & 1) != expected:
                raise RuntimeError(f"GIC SPI0 enable mismatch: expected {expected}, got {reply!r}")
        # SPI0 pending state: ISPENDR1 0x01c81204, ICPENDR1 0x01c81284.
        # Software-generated pending state validates distributor register semantics;
        # it does not yet prove that UART0 asserts its hardware IRQ output.
        for command, expected in (
            (b"writel 0x01c81284 0x1\n", 0),
            (b"writel 0x01c81204 0x1\n", 1),
            (b"writel 0x01c81284 0x1\n", 0),
        ):
            proc.stdin.write(command)
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ GIC SPI0 pending write timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if reply != "OK":
                raise RuntimeError(f"GIC SPI0 pending write failed: {reply!r}")
            proc.stdin.write(b"readl 0x01c81204\n")
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ GIC SPI0 pending read timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if not reply.startswith("OK ") or (int(reply.split()[1], 0) & 1) != expected:
                raise RuntimeError(f"GIC SPI0 pending mismatch: expected {expected}, got {reply!r}")
        # UART0 interrupt-enable register (IER), offset 1 with regshift 2.
        # This tests UART register behavior; hardware IRQ assertion is a later test.
        for value in (0, 2, 0):
            proc.stdin.write(f"writel 0x01c28004 {value}\n".encode("ascii"))
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ UART0 IER write timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if reply != "OK":
                raise RuntimeError(f"UART0 IER write failed: {reply!r}")
            proc.stdin.write(b"readl 0x01c28004\n")
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ UART0 IER read timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if not reply.startswith("OK ") or (int(reply.split()[1], 0) & 2) != value:
                raise RuntimeError(f"UART0 IER mismatch: expected {value}, got {reply!r}")
        # Hardware IRQ smoke test: enable GIC SPI0 and UART0 THRE interrupt.
        # A reset 16550-compatible UART has an empty transmit holding register.
        # The resulting UART IRQ should make SPI0 (GIC interrupt ID 32) pending.
        for command in (
            b"writel 0x01c81284 0x1\n",  # clear software pending SPI0
            b"writel 0x01c81104 0x1\n",  # enable SPI0
            b"writel 0x01c28004 0x2\n",  # enable UART THRE IRQ
        ):
            proc.stdin.write(command)
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ UART0 IRQ setup timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if reply != "OK":
                raise RuntimeError(f"UART0 IRQ setup failed: {reply!r}")
        proc.stdin.write(b"readl 0x01c81204\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ UART0 to GIC SPI0 pending read timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if not reply.startswith("OK ") or not (int(reply.split()[1], 0) & 1):
            raise RuntimeError(f"UART0 THRE IRQ did not set GIC SPI0 pending: {reply!r}")
        # GIC CPU interface: enable distributor Group 0 and CPU interface,
        # allow all priorities, then acknowledge UART0 SPI0 (interrupt ID 32).
        for command in (
            b"writel 0x01c81000 0x1\n",  # GICD_CTLR
            b"writel 0x01c82004 0xff\n",  # GICC_PMR
            b"writel 0x01c82000 0x1\n",  # GICC_CTLR
        ):
            proc.stdin.write(command)
            proc.stdin.flush()
            ready, _, _ = select.select([proc.stdout], [], [], 15)
            if not ready:
                raise RuntimeError("H2+ GIC CPU interface setup timed out")
            reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
            if reply != "OK":
                raise RuntimeError(f"GIC CPU interface setup failed: {reply!r}")
        proc.stdin.write(b"readl 0x01c8200c\n")  # GICC_IAR
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ GIC interrupt acknowledge timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if not reply.startswith("OK ") or (int(reply.split()[1], 0) & 0x3ff) != 32:
            raise RuntimeError(f"GIC did not deliver UART0 SPI0 interrupt ID 32: {reply!r}")
        proc.stdin.write(b"writel 0x01c82010 0x20\n")  # GICC_EOIR
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready or os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip() != "OK":
            raise RuntimeError("H2+ GIC end-of-interrupt write failed")
        proc.stdin.write(b"writel 0x01c28004 0x0\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready or os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip() != "OK":
            raise RuntimeError("H2+ UART0 IRQ cleanup failed")
        # 16550-compatible UART0 scratch register (offset 7, regshift 2).
        # A writable scratch register distinguishes UART MMIO from open bus.
        proc.stdin.write(b"writel 0x01c2801c 0x5a\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ UART0 scratch write timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if reply != "OK":
            raise RuntimeError(f"UART0 scratch write failed: {reply!r}")
        proc.stdin.write(b"readl 0x01c2801c\n")
        proc.stdin.flush()
        ready, _, _ = select.select([proc.stdout], [], [], 15)
        if not ready:
            raise RuntimeError("H2+ UART0 scratch read timed out")
        reply = os.read(proc.stdout.fileno(), 256).decode("ascii", errors="replace").strip()
        if not reply.startswith("OK ") or (int(reply.split()[1], 0) & 0xff) != 0x5a:
            raise RuntimeError(f"UART0 scratch readback mismatch: {reply!r}")


    finally:
        if proc.poll() is None:
            proc.terminate()
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()
    print("PASS: independent H2+ machine launched; RAM write/readback through QTest")
    print("PASS: GICv2 distributor ID, control, SPI0 enable and pending registers")
    print("PASS: UART0 IER and scratch register write/readback through QTest")
    print("PASS: UART0 THRE IRQ asserted GIC SPI0 pending")
    print("PASS: GIC CPU interface acknowledged UART0 interrupt ID 32")
    print("NOTE: Cortex-A7 IRQ pin level, UART TX/RX and guest boot not yet tested")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
