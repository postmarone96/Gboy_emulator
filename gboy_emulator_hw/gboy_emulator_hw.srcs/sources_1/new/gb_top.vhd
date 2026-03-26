library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gb_top is 
    Port(

    );
end gb_top;

architecture rtl of gb_top is
    signal cpu_mem_data_in  : std_logic_vector(7 downto 0);
    signal cpu_mem_data_out : std_logic_vector(7 downto 0);
    signal cpu_addr_bus     : std_logic_vector(15 downto 0);
    signal cpu_mem_rd       : std_logic;
    signal cpu_mem_wr       : std_logic;


    signal timer_data_out   : std_logic_vector(7 downto 0);
    signal timer_irq        : std_logic;

    -- type rom_t is array (0 to 16#7FFF#) of std_logic_vector(7 downto 0);
    -- type ram_t is array (0 to 16#1FFF#) of std_logic_vector(7 downto 0);

    -- signal rom : rom_t := (others => x"00");
    -- signal wram : ram_t := (others => x"00");

    -- signal rom_sel   : std_logic;
    -- signal wram_sel  : std_logic;
    signal timer_sel : std_logic;

begin
    -- rom_sel   <= '1' when unsigned(cpu_addr_bus) <= x"7FFF" else '0';
    -- wram_sel  <= '1' when unsigned(cpu_addr_bus) >= x"C000" and unsigned(cpu_addr_bus) <= x"DFFF" else '0';
    timer_sel <= '1' when unsigned(cpu_addr_bus) >= x"FF04" and unsigned(cpu_addr_bus) <= x"FF07" else '0';

    cpu_i: entity work.cpu_control_unit
        generic map(
            SIM_POST_BOOT => true
        );
        port map(
            clk             => clk,
            rst             => rst,

            mem_data_in     => cpu_mem_data_in,
            mem_data_out    => cpu_mem_data_out,

            addr_bus        => cpu_addr_bus,
            mem_rd          => cpu_mem_rd,
            mem_wr          => cpu_mem_wr,

            vblank_irq      => '0',
            lcd_stat_irq    => '0',
            timer_irq       => timer_irq,
            serial_irq      => '0',
            joypad_irq      => '0'

        );
    
    timer_i: entity work.gb_timer
        port map(
            clk             => clk,
            rst             => rst,

            addr_bus        => cpu_addr_bus,
            data_in         => cpu_mem_data_out,
            data_out        => timer_data_out,

            rd_from_timer   => cpu_mem_rd and timer_sel,
            wr_to_timer     => cpu_mem_wr and timer_sel,

            timer_irq       =>timer_irq
        );
    
    -- Read-data mux back into the CPU
    process(all)
    begin
        cpu_mem_data_in <= x"FF";
        -- if rom_sel = '1' then
        --     cpu_mem_data_in <= rom(to_integer(unsigned(cpu_addr_bus(14 downto 0))));
        -- elsif wram_sel = '1' then
        --     cpu_mem_data_in <= wram(to_integer(unsigned(cpu_addr_bus(12 downto 0))));
        if timer_sel = '1' then
            cpu_mem_data_in <= timer_rd_data;
        end if;
    end process;



end rtl;