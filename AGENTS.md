# Contributor and automation guidance

M0 is project infrastructure, not implemented hardware emulation. Do not mark Orange Pi Zero LTS, WR703N or Mango as emulated yet.

Keep machine-specific changes upstreamable, add qtests for new devices and include boot logs proving claimed milestones. Do not commit firmware dumps, vendor blobs or proprietary ROMs. Preserve QEMU upstream SPDX headers in copied or modified upstream source and use QEMU's contributor guidelines for submission.
