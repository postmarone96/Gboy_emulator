# Blargg Test Checklist

Last updated: 2026-03-24

Use `[x]` for done and `[ ]` for not done.

## Emulator Capability Checklist

- [x] CPU core executes documented SM83 instruction set
- [x] CB-prefixed instruction table generated and wired
- [x] ROM mapping works for `0000-7FFF`
- [x] WRAM mapping works for `C000-DFFF`
- [x] HRAM mapping works for `FF80-FFFE`
- [x] `IF` register at `FF0F`
- [x] `IE` register at `FFFF`
- [x] Post-boot startup state available for simulation
- [x] Serial debug output captured through `SB=FF01` and `SC=FF02`
- [x] Minimal LCD shell for console output
- [x] `LY=FF44` faked well enough so console output does not hang
- [ ] Timer peripheral model (`DIV`, `TIMA`, `TMA`, `TAC`)
- [ ] Timer interrupt generation on `timer_irq`
- [ ] External interrupt sources modeled beyond manual IF writes
- [ ] HALT wake-up behavior verified with real interrupt source
- [ ] HALT bug behavior verified
- [ ] Accurate instruction timing
- [ ] Accurate memory access timing
- [ ] OAM bug behavior
- [ ] DMG APU behavior
- [ ] CGB double-speed behavior
- [ ] CGB APU behavior

## CPU Instruction Tests

Baseline needed for most of these:
- CPU core
- ROM/RAM/HRAM mapping
- `IF`/`IE`
- serial output
- minimal FFxx storage
- fake `LY`

- [ ] `cpu_instrs/cpu_instrs.gb`
  - Multi-ROM wrapper for all CPU instruction tests
  - Best used after most individual ROMs pass

- [x] `cpu_instrs/individual/01-special.gb`
  - Needs only the baseline shell
  - Current status: passed

- [ ] `cpu_instrs/individual/02-interrupts.gb`
  - Needs baseline shell
  - Also needs timer hardware behavior
  - Needs `timer_irq` generation and `IF` bit 2 behavior
  - Needs HALT wake-up from timer interrupt
  - Current status: fails with `Timer doesn't work`

- [x] `cpu_instrs/individual/03-op sp,hl.gb`
  - Needs only the baseline shell

- [x] `cpu_instrs/individual/04-op r,imm.gb`
  - Needs only the baseline shell

- [x] `cpu_instrs/individual/05-op rp.gb`
  - Needs only the baseline shell

- [x] `cpu_instrs/individual/06-ld r,r.gb`
  - Needs only the baseline shell

- [x] `cpu_instrs/individual/07-jr,jp,call,ret,rst.gb`
  - Needs only the baseline shell
  - Also checks control-flow correctness
  - Touches `RETI`, `DI`, `EI`, `IE`, but does not require a real timer

- [x] `cpu_instrs/individual/08-misc instrs.gb`
  - Needs only the baseline shell
  - Covers `LDH`, stack ops, immediate 16-bit loads, memory mapped FFxx access

- [x] `cpu_instrs/individual/09-op r,r.gb`
  - Needs only the baseline shell

- [x] `cpu_instrs/individual/10-bit ops.gb`
  - Needs only the baseline shell

- [ ] `cpu_instrs/individual/11-op a,(hl).gb`
  - Needs only the baseline shell

## Timing and Interrupt Timing Tests

- [ ] `instr_timing/instr_timing.gb`
  - Needs timer operation
  - Needs correct instruction timing
  - Needs taken/not-taken conditional timing

- [ ] `interrupt_time/interrupt_time.gb`
  - Needs timer operation
  - Needs interrupt timing to be correct
  - Needs CGB double-speed support
  - Needs timer start/stop behavior

## Memory Timing Tests

- [ ] `mem_timing/mem_timing.gb`
  - Needs timer operation
  - Needs correct memory access timing

- [ ] `mem_timing/individual/01-read_timing.gb`
  - Needs timer operation
  - Needs correct read timing

- [ ] `mem_timing/individual/02-write_timing.gb`
  - Needs timer operation
  - Needs correct write timing

- [ ] `mem_timing/individual/03-modify_timing.gb`
  - Needs timer operation
  - Needs correct read-modify-write timing

- [ ] `mem_timing-2/mem_timing.gb`
  - Same class as `mem_timing`
  - Use after the first memory timing suite is stable

- [ ] `mem_timing-2/rom_singles/01-read_timing.gb`
  - Needs timer operation
  - Needs correct read timing

- [ ] `mem_timing-2/rom_singles/02-write_timing.gb`
  - Needs timer operation
  - Needs correct write timing

- [ ] `mem_timing-2/rom_singles/03-modify_timing.gb`
  - Needs timer operation
  - Needs correct read-modify-write timing

## HALT and Interrupt Edge-Case Tests

- [ ] `halt_bug.gb`
  - CPU-focused
  - Needs correct HALT bug behavior
  - Needs `IME` / `IF` / `IE` interaction to be correct

## OAM / LCD Timing Tests

- [ ] `oam_bug/oam_bug.gb`
  - Needs LCD timing
  - Needs OAM corruption bug behavior on DMG

- [ ] `oam_bug/rom_singles/1-lcd_sync.gb`
  - Needs LCD timing

- [ ] `oam_bug/rom_singles/2-causes.gb`
  - Needs OAM bug behavior

- [ ] `oam_bug/rom_singles/3-non_causes.gb`
  - Needs OAM bug behavior

- [ ] `oam_bug/rom_singles/4-scanline_timing.gb`
  - Needs scanline timing

- [ ] `oam_bug/rom_singles/5-timing_bug.gb`
  - Needs scanline timing and bug timing window

- [ ] `oam_bug/rom_singles/6-timing_no_bug.gb`
  - Needs scanline timing and no-bug window

- [ ] `oam_bug/rom_singles/7-timing_effect.gb`
  - Needs scanline timing and corruption pattern correctness

- [ ] `oam_bug/rom_singles/8-instr_effect.gb`
  - Needs instruction-specific OAM bug behavior

## DMG Sound Tests

- [ ] `dmg_sound/dmg_sound.gb`
  - Needs DMG APU behavior

- [ ] `dmg_sound/rom_singles/01-registers.gb`
- [ ] `dmg_sound/rom_singles/02-len ctr.gb`
- [ ] `dmg_sound/rom_singles/03-trigger.gb`
- [ ] `dmg_sound/rom_singles/04-sweep.gb`
- [ ] `dmg_sound/rom_singles/05-sweep details.gb`
- [ ] `dmg_sound/rom_singles/06-overflow on trigger.gb`
- [ ] `dmg_sound/rom_singles/07-len sweep period sync.gb`
- [ ] `dmg_sound/rom_singles/08-len ctr during power.gb`
- [ ] `dmg_sound/rom_singles/09-wave read while on.gb`
- [ ] `dmg_sound/rom_singles/10-wave trigger while on.gb`
- [ ] `dmg_sound/rom_singles/11-regs after power.gb`
- [ ] `dmg_sound/rom_singles/12-wave write while on.gb`

## CGB Sound Tests

- [ ] `cgb_sound/cgb_sound.gb`
  - Needs CGB APU behavior
  - Needs CGB-specific sound behavior

- [ ] `cgb_sound/rom_singles/01-registers.gb`
- [ ] `cgb_sound/rom_singles/02-len ctr.gb`
- [ ] `cgb_sound/rom_singles/03-trigger.gb`
- [ ] `cgb_sound/rom_singles/04-sweep.gb`
- [ ] `cgb_sound/rom_singles/05-sweep details.gb`
- [ ] `cgb_sound/rom_singles/06-overflow on trigger.gb`
- [ ] `cgb_sound/rom_singles/07-len sweep period sync.gb`
- [ ] `cgb_sound/rom_singles/08-len ctr during power.gb`
- [ ] `cgb_sound/rom_singles/09-wave read while on.gb`
- [ ] `cgb_sound/rom_singles/10-wave trigger while on.gb`
- [ ] `cgb_sound/rom_singles/11-regs after power.gb`
- [ ] `cgb_sound/rom_singles/12-wave.gb`

## Suggested Bring-Up Order

- [x] `cpu_instrs/individual/01-special.gb`
- [ ] `cpu_instrs/individual/03-op sp,hl.gb`
- [ ] `cpu_instrs/individual/04-op r,imm.gb`
- [ ] `cpu_instrs/individual/05-op rp.gb`
- [ ] `cpu_instrs/individual/06-ld r,r.gb`
- [ ] `cpu_instrs/individual/08-misc instrs.gb`
- [ ] `cpu_instrs/individual/09-op r,r.gb`
- [ ] `cpu_instrs/individual/10-bit ops.gb`
- [ ] `cpu_instrs/individual/11-op a,(hl).gb`
- [ ] `cpu_instrs/individual/07-jr,jp,call,ret,rst.gb`
- [ ] `cpu_instrs/individual/02-interrupts.gb`
- [ ] `instr_timing/instr_timing.gb`
- [ ] `mem_timing/mem_timing.gb`
- [ ] `halt_bug.gb`
- [ ] `interrupt_time/interrupt_time.gb`
- [ ] `oam_bug/oam_bug.gb`
- [ ] `dmg_sound/dmg_sound.gb`
- [ ] `cgb_sound/cgb_sound.gb`

## Notes

- `01-special.gb` passing means the serial path and basic CPU shell are working.
- `02-interrupts.gb` is not a pure CPU-only test in this setup because it expects timer behavior.
- The `cpu_instrs` readme explicitly says console output is designed to work with minimal LCD support, so a fake `LY` is acceptable for those tests.
- The timing suites are not good next-step tests until the timer exists.
