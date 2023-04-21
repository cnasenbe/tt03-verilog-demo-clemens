import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

@cocotb.test()
async def test_shift_reg_perm_one(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    dut.data_in.value = 0
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0

    dut._log.info("check shift permanent data_in=1")
    
    dut.data_in.value = 1
    await ClockCycles(dut.clk, 1)
    compare_val = 1;
    for i in range(8):
        dut._log.info("check value after {} cycles".format(i))
        await ClockCycles(dut.clk, 1)
        dut.data_in.value = 1
        dut._log.info("check value after {} cycles, its {}, expect {}".format(i, dut.data_out.value, bin(compare_val)))
        assert bin(dut.data_out.value) == bin(compare_val)
        compare_val = compare_val << 1 | compare_val;
    
@cocotb.test()
async def test_shift_reg_single_pulse(dut):
    dut._log.info("start")
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.clk, 10)
    dut.rst.value = 0
    
    dut._log.info("check shift of only 1 cycle data_in=1")

    dut.data_in.value = 1
    await ClockCycles(dut.clk, 1)
    dut.data_in.value = 0
    compare_val = 1;
    for i in range(8):
        dut._log.info("check value after {} cycles".format(i))
        await ClockCycles(dut.clk, 1)
        dut._log.info("check value after {} cycles, its {}, expect {}".format(i, dut.data_out.value, bin(compare_val)))
        assert bin(dut.data_out.value) == bin(compare_val)
        compare_val = compare_val << 1;
