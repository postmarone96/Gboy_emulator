import csv
from microcode_utils import generate_ld_r_r

# The standard 3-bit register mapping for SM83
registers = {
    0: "B",
    1: "C",
    2: "D",
    3: "E",
    4: "H",
    5: "L",
    6: "HL_MEM",  # (HL) points to memory, handled differently later
    7: "A"
}

header_row = ["Opcode", "M_Cycle", "Label", "Reg_Dest", "Reg_Src", "Mem_Read", "Mem_Write", "PC_Inc", "Is_Done"]

with open('microcode.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header_row)

    # LD r, r’: Load register
    generate_ld_r_r(registers, writer)



