# --- Cocotb Setup ---
SIM ?= ghdl
TOPLEVEL_LANG ?= vhdl
EXTRA_ARGS += --std=08

# Pfade zu deinen VHDL-Dateien (Passe diese an dein Projekt an!)
VHDL_SOURCES += ../../gboy_emulator_hw/gboy_emulator_hw.srcs/sources_1/new/microcode_pkg.vhd
VHDL_SOURCES += ../../gboy_emulator_hw/gboy_emulator_hw.srcs/sources_1/new/cpu_control_unit.vhd

# Name der Top-Level Entity in deinem VHDL
TOPLEVEL = cpu_control_unit

# Name der Python-Testdatei (ohne .py)
MODULE ?= blargg_test

# --- Waveform Handling ---
# Falls von run_all.py nichts kommt, nutzen wir einen Standardnamen
WAVE_FILE ?= dump.ghw
TEST_ROM ?=
BLARGG_TIMEOUT_CYCLES ?= 60000000
COCOTB_PYTHON := $(abspath ../../.venv/bin/python3)
PYTHON_BIN := $(COCOTB_PYTHON)
COCOTB_CONFIG := $(COCOTB_PYTHON) -m cocotb_tools.config
export PATH := $(abspath ../../.venv/bin):$(PATH)

# GHDL-spezifische Argumente:
# --wave=... schreibt die GHW Datei für Surfer
SIM_ARGS += --wave=$(WAVE_FILE)
SIM_ARGS += -gSIM_POST_BOOT=true

export TEST_ROM
export BLARGG_TIMEOUT_CYCLES

# --- Cocotb Makefile Einbindung ---
include $(shell $(COCOTB_CONFIG) --makefiles)/Makefile.sim

# --- Hilfs-Regeln ---
.PHONY: clean_all

clean_all:
	rm -rf sim_build/
	rm -rf results/
	rm -f *.xml
