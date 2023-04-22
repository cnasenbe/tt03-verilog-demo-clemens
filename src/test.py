import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

sample_width = 24
samples = [[0xfffeff, 0xbecafe], [0x123456, 0xdeadbe], [0xf0f0f0, 0xf1f1f1], [0xfeefbe, 0xcafeca]]
LEFT = 0
RIGHT = 1

@cocotb.test()
async def test_i2s(dut):
    dut._log.info("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("init")
    dut.ws.value = 0
    dut.sd.value = 0
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.sck, 5)
    dut.rst.value = 0
    await ClockCycles(dut.sck, 5)

    for sample_id in range(len(samples)):
        dut._log.info("Shift data in with ws indicating new sample")
        dut._log.info("left: {:X}".format(samples[sample_id][LEFT]))
        dut._log.info("right {:X}".format(samples[sample_id][RIGHT]))

        dut.ws.value = 1
        dut.sd.value = (samples[sample_id][LEFT] >> 24) & 1
        await ClockCycles(dut.sck, 1)
        for i in range(sample_width):
            dut.sd.value = (samples[sample_id][LEFT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1)
            if i == sample_width-1:
                dut.ws.value = 0
        await ClockCycles(dut.sck, 1)

        #Can only check last sample once new sample has been started
        if sample_id > 0:
            ref_xor_right = 0; 
            for k in range(sample_width):
                ref_xor_right = ref_xor_right ^ ((samples[sample_id-1][RIGHT] >> k) & 1)
            assert ref_xor_right == dut.xor_data_right.value
        
        dut.sd.value = (samples[sample_id][RIGHT] >> 24) & 1
        for i in range(sample_width):
            dut.sd.value = (samples[sample_id][RIGHT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1)
        await ClockCycles(dut.sck, 10)

        ref_xor_left = 0; 
        for k in range(sample_width):
            ref_xor_left = ref_xor_left ^ ((samples[sample_id][LEFT] >> k) & 1)
        assert ref_xor_left == dut.xor_data_left.value
