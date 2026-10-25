/* Fixed guest DRAM layout for the first H2+ execution probe. */
ENTRY(_start)
SECTIONS
{
    . = 0x40000000;
    .text : { KEEP(*(.text.boot)) *(.text*) }
    .rodata : { *(.rodata*) }
    .data : { *(.data*) }
    .bss (NOLOAD) : { *(.bss*) *(COMMON) }
    /DISCARD/ : { *(.comment*) *(.note*) }
}
