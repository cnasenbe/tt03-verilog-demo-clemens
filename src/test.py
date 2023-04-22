import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

reg_width = 96
overhead_runs = 5

sample_width = 24
input_samples = [[0xfffeff, 0x000100]]


@cocotb.test()
async def test_shift_reg_perm_one(dut):
    dut._log.info("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("init")
    dut.ws.value = 0
    dut.sd1.value = 0
    dut.sd2.value = 0
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.sck, 10)
    dut.rst.value = 0

    dut._log.info("Put some data in and change word line")
    dut._log.info("{:X}".format(input_samples[0][0]))
    dut._log.info("{:X}".format(input_samples[0][1]))
    dut._log.info("{}".format(bin(input_samples[0][0])))
    dut._log.info("{}".format(bin(input_samples[0][1])))
    dut.ws.value = 1
    value_out = 0x0
    await ClockCycles(dut.sck, 1)
    dut.sd1.value = (input_samples[0][0]) & 1
    dut.sd2.value = (input_samples[0][1]) & 1
    await ClockCycles(dut.sck, 1)
    for i in range(sample_width):
        dut.sd1.value = (input_samples[0][0] >> i) & 1
        dut.sd2.value = (input_samples[0][1] >> i) & 1
        await ClockCycles(dut.sck, 1)
        dut._log.info("i:{}, sd_out value: 0b{}".format(i, dut.sd_out.value))
        value_out = (dut.sd_out.value << i) | value_out
    await ClockCycles(dut.sck, 1)
    dut._log.info("i:{}, sd_out value: 0b{}".format(i, dut.sd_out.value))
    value_out = (dut.sd_out.value << i) | value_out
    dut._log.info("data_out value: 0x{:X}".format(value_out))
    
    ref_val = input_samples[0][0] + input_samples[0][1];
    dut._log.info("ref value: 0x{:X}".format(ref_val))
    
    assert ref_val == value_out
