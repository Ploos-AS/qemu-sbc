/* Static initramfs /init for eventual Linux handoff. SPDX-License-Identifier: MIT */
#include <stddef.h>
#include <stdint.h>

#if !defined(__arm__)
#error "This init is intended for 32-bit ARM Linux"
#endif

static long sys_write(int fd, const void *buf, unsigned long len)
{
    register long r0 __asm__("r0") = fd;
    register const void *r1 __asm__("r1") = buf;
    register unsigned long r2 __asm__("r2") = len;
    register long r7 __asm__("r7") = 4; /* ARM EABI write */
    __asm__ volatile("svc 0" : "+r"(r0) : "r"(r1), "r"(r2), "r"(r7) : "memory");
    return r0;
}

static void sys_exit(int status)
{
    register long r0 __asm__("r0") = status;
    register long r7 __asm__("r7") = 1;
    __asm__ volatile("svc 0" : : "r"(r0), "r"(r7) : "memory");
    for (;;) {}
}

void _start(void)
{
    static const char message[] = "H2 LINUX INIT OK\n";
    sys_write(1, message, sizeof(message) - 1);
    sys_exit(0);
}
