import logging
import os
from pathlib import Path
from collections import deque
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge


POST_BOOT_PC = 0x0100


def load_rom(rom_path: str) -> bytearray:
    rom_bytes = Path(rom_path).read_bytes()
    memory = bytearray(0x10000)
    memory[: min(len(rom_bytes), 0x8000)] = rom_bytes[:0x8000]
    return memory


def init_dmg_io(memory: bytearray) -> None:
    defaults = {
        0xFF05: 0x00,
        0xFF06: 0x00,
        0xFF07: 0x00,
        0xFF10: 0x80,
        0xFF11: 0xBF,
        0xFF12: 0xF3,
        0xFF14: 0xBF,
        0xFF16: 0x3F,
        0xFF17: 0x00,
        0xFF19: 0xBF,
        0xFF1A: 0x7F,
        0xFF1B: 0xFF,
        0xFF1C: 0x9F,
        0xFF1E: 0xBF,
        0xFF20: 0xFF,
        0xFF21: 0x00,
        0xFF22: 0x00,
        0xFF23: 0xBF,
        0xFF24: 0x77,
        0xFF25: 0xF3,
        0xFF26: 0xF1,
        0xFF40: 0x91,
        0xFF42: 0x00,
        0xFF43: 0x00,
        0xFF44: 0x90,
        0xFF45: 0x00,
        0xFF47: 0xFC,
        0xFF48: 0xFF,
        0xFF49: 0xFF,
        0xFF4A: 0x00,
        0xFF4B: 0x00,
    }
    for addr, value in defaults.items():
        memory[addr] = value


@cocotb.test()
async def run_blargg_rom(dut):
    dut._log.setLevel(logging.INFO)

    rom_path = os.environ.get("TEST_ROM")
    if not rom_path:
        raise AssertionError("TEST_ROM is required")
    last_write_key = None
    memory = load_rom(rom_path)
    init_dmg_io(memory)
    serial_chars: list[str] = []
    recent_trace = deque(maxlen=64)
    trace_live = os.environ.get("TRACE_OPCODES", "0") == "1"
    trace_imm = os.environ.get("TRACE_IMM", "0") == "1"
    trace_state = os.environ.get("TRACE_STATE", "0") == "1"
    max_cycles = int(os.environ.get("BLARGG_TIMEOUT_CYCLES", "20000000"))

    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst.value = 1
    dut.mem_data_in.value = 0xFF
    dut.vblank_irq.value = 0
    dut.lcd_stat_irq.value = 0
    dut.timer_irq.value = 0
    dut.serial_irq.value = 0
    dut.joypad_irq.value = 0

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 0

    dut.mem_data_in.value = memory[POST_BOOT_PC]

    for _ in range(max_cycles):
        await FallingEdge(dut.clk)

        addr = int(dut.addr_bus.value)
        mem_rd = int(dut.mem_rd.value)
        mem_wr = int(dut.mem_wr.value)
        bus_byte = memory[addr]

        if mem_rd and not mem_wr:
            last_write_key = None
            dut.mem_data_in.value = bus_byte

        elif mem_wr and not mem_rd:
            value = int(dut.mem_data_out.value)
            write_key = (
                int(dut.cb_exec.value),
                int(dut.current_ir.value),
                int(dut.m_cycle.value),
                addr,
                value,
            )

            if write_key != last_write_key:
                if 0x8000 <= addr <= 0xFFFF:
                    memory[addr] = value

                if addr == 0xFF01:
                    memory[addr] = value
                elif addr == 0xFF02:
                    memory[addr] = value
                    if value == 0x81:
                        ch = chr(memory[0xFF01])
                        serial_chars.append(ch)
                        serial_text = "".join(serial_chars)
                        dut._log.info("SERIAL: %s", serial_text)
                        memory[0xFF02] = 0x00

                        if "Passed" in serial_text:
                            return
                        if "Failed" in serial_text:
                            raise AssertionError(serial_text)

                last_write_key = write_key
        else:
            last_write_key = None

        if trace_imm and int(dut.current_ir.value) in (0x11, 0x21):
            dut._log.info(
                "IMM IR=%02X M=%d T=%d PC=%04X ADDR=%04X RD=%d WR=%d BUS=%02X DIN=%02X IBUS=%02X DEST=%d SRC=%d ALU=%d IDU=%d BC=%04X DE=%04X HL=%04X",
                int(dut.current_ir.value),
                int(dut.m_cycle.value),
                int(dut.t_cycle.value),
                int(dut.pc.value) & 0xFFFF,
                addr,
                mem_rd,
                mem_wr,
                bus_byte,
                int(dut.mem_data_in.value),
                int(dut.internal_bus.value),
                int(dut.dbg_mc_reg_dest.value),
                int(dut.dbg_mc_reg_src.value),
                int(dut.dbg_mc_alu_op.value),
                int(dut.dbg_mc_idu_op.value),
                int(dut.bc.value) & 0xFFFF,
                int(dut.de.value) & 0xFFFF,
                int(dut.hl.value) & 0xFFFF,
            )

        await RisingEdge(dut.clk)

        if int(dut.m_cycle.value) == 1 and int(dut.t_cycle.value) == 2:
            pc = int(dut.pc.value) & 0xFFFF
            op = int(dut.current_ir.value)

            if op == 0x100:
                op_name = "INT"
            elif int(dut.cb_exec.value):
                op_name = f"CB {op:02X}"
            else:
                op_name = f"{op:02X}"

            trace_line = f"PC={pc:04X} OP={op_name}"
            if trace_state and pc in (0x0208, 0x0209, 0x020B, 0x020C, 0x020D, 0x020F):
                dut._log.info(
                    "STATE PC=%04X OP=%s AF=%04X BC=%04X DE=%04X HL=%04X WZ=%04X M=%d T=%d",
                    pc,
                    op_name,
                    int(dut.af.value) & 0xFFFF,
                    int(dut.bc.value) & 0xFFFF,
                    int(dut.de.value) & 0xFFFF,
                    int(dut.hl.value) & 0xFFFF,
                    int(dut.temp_wz.value) & 0xFFFF,
                    int(dut.m_cycle.value),
                    int(dut.t_cycle.value),
                )
            recent_trace.append(trace_line)

            if trace_live:
                dut._log.info("FETCH %s", trace_line)

    trace_dump = "\n".join(recent_trace)
    raise AssertionError(
        f"Timeout waiting for Blargg result. Serial output: {''.join(serial_chars)}\n"
        f"Recent fetch trace:\n{trace_dump}"
    )
