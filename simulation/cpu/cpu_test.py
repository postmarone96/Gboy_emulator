import cocotb
from cocotb.triggers import Timer, FallingEdge, RisingEdge, ReadOnly
from cocotb.clock import Clock
import os
import csv
import logging


@cocotb.test()
async def drive_cpu_with_csv(dut):
    """Nutzt die CSV, um die Steuersignale der CPU pro M-Zyklus zu setzen"""

    # Erzwinge INFO-Level für den Test-Logger
    dut._log.setLevel(logging.INFO)

    target_op_hex = os.environ.get("TEST_OPCODE", "0x00")

    microcode_steps = []
    with open('../../microcode/microcode.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Opcode'].lower() == target_op_hex.lower() or row['Opcode'].lower() == "0x00":
                microcode_steps.append(row)

    # simple test-Memory
    fake_rom = {
        # Programm-Bereich (Opcodes & Immediates)
        0x0000: 0x00,
        0x0001: int(target_op_hex, 16),
        0x0002: 0xDE,  # 'n'
        0x0003: 0xAD,  # 'nn'

        # Ziel-Adressen
        0xADDE: 0x12,  # nn
        0x0708: 0xFE,  # HL
        0x0203: 0xBE,  # BC
        0x0405: 0xEF,  # DE
        0xFF03: 0x11,  # IO-Bereich
        0xFFDE: 0x99  # Stack-Bereich
    }

    # 1. Setup
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())
    dut.rst.value = 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 0

    # 2. M-Cycle control
    for step in microcode_steps:
        for _ in range(4):
            await FallingEdge(dut.clk)

            addr = dut.addr_bus.value.to_unsigned()
            t_cycle = int(dut.t_cycle.value)
            mem_rd = 1 if dut.mem_rd.value == 1 else 0
            mem_wr = 1 if dut.mem_wr.value == 1 else 0

            if mem_rd == 1 and mem_wr == 0:
                dut.mem_data_in.value = fake_rom.get(addr, 0x00)
                cocotb.log.info(f"M{step['M_Cycle']}/T{t_cycle}: READ @ {hex(addr)}")
            elif mem_rd == 0 and mem_wr == 1:
                val_obj = dut.mem_data_out.value
                if val_obj.is_resolvable:
                    written_val = val_obj.to_unsigned()
                    fake_rom[addr] = written_val
                    cocotb.log.info(f"M{step['M_Cycle']}/T{t_cycle}: WRITE {hex(written_val)} @ {hex(addr)}")
                else:
                    cocotb.log.error(f"Schreibzugriff bei {hex(addr)} mit ungültigen Daten: {val_obj.binstr}")

            await RisingEdge(dut.clk)

        if step['Opcode'].lower() == target_op_hex.lower() and int(step['Is_Done']) == 1:
            break

    cocotb.log.info(f"Simulation für {target_op_hex} beendet.")
