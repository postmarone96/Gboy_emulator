# --- Cocotb Setup ---
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl

# Pfade zu deinen VHDL-Dateien (Passe diese an dein Projekt an!)
VHDL_SOURCES += ../../gboy_emulator_hw/gboy_emulator_hw.srcs/sources_1/new/microcode_pkg.vhd
VHDL_SOURCES += ../../gboy_emulator_hw/gboy_emulator_hw.srcs/sources_1/new/cpu_control_unit.vhd

# Name der Top-Level Entity in deinem VHDL
TOPLEVEL = cpu_control_unit

# Name der Python-Testdatei (ohne .py)
MODULE = cpu_test

# --- Waveform Handling ---
# Falls von run_all.py nichts kommt, nutzen wir einen Standardnamen
WAVE_FILE ?= dump.ghw

# GHDL-spezifische Argumente:
# --wave=... schreibt die GHW Datei für Surfer
SIM_ARGS += --wave=$(WAVE_FILE)

# --- Cocotb Makefile Einbindung ---
include $(shell cocotb-config --makefiles)/Makefile.sim

# --- Hilfs-Regeln ---
.PHONY: clean_all
clean_all:
	rm -rf sim_build/
	rm -rf results/
	rm -f *.xml
