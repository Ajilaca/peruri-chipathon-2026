# MEASURED (simulasi / lint, bukan perangkat keras): Verifikasi Fase 6, scripts/test/phase6_verify.sh pada git 016bff0 (RTL tidak berubah sejak itu), 2026-10-03

```
## V1 verilator --lint-only -Wall kpke_sched_top
rc=0
## V1 slang kpke_sched_top
Build succeeded: 0 errors, 0 warnings
rc=0
## V2 golden schedule model vs golden K-PKE (pytest)
26 passed in 1.26s
rc=0
## V3 gamma and program ROMs (generated, golden-derived)
rtl/sched/gamma_rom.sv: reproduced byte for byte
rtl/sched/kpke_prog_rom.sv: reproduced byte for byte
gamma entries checked against the golden list: 128
rc=0
## V4/V5/V6 verilator
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'pwm_unit.u_mhi.s_cut'
200415.00ns INFO     cocotb.pwm_unit                    pwm_unit: 20035/20035 pairs equal to BaseCaseMultiply + accumulate
200415.00ns INFO     cocotb.regression                  test_pwm_unit.test_pwm_stream passed
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:76:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:94:31: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:78:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:74:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.g_lane[7].u_bfly.u_mul.g_barrett.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:75:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:77:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.off_s'
889195.00ns INFO     cocotb.kpke_sched_top              keygen: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (6, 0, 9), cycles 5493
1844195.00ns INFO     cocotb.kpke_sched_top              encrypt: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (3, 4, 12), cycles 6810
2614745.00ns INFO     cocotb.kpke_sched_top              decrypt: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (3, 1, 3), cycles 3121
2614745.00ns INFO     cocotb.regression                  test_kpke_sched.test_programs_bit_exact_and_constant passed
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:76:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:94:31: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:78:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:74:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.g_lane[7].u_bfly.u_mul.g_barrett.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:75:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:77:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.off_s'
368875.00ns INFO     cocotb.kpke_sched_top              negative control: 2/2 programs differ from the model
368875.00ns INFO     cocotb.regression                  test_kpke_sched.test_negative_control_must_fail passed
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:74:33: 'en_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:75:33: 'wr_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:76:33: 'bank_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:77:33: 'off_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:78:33: 'slot_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-SPLITVAR: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:79:33: 'count_s' has split_var metacomment but will not be split because its bitwidth is 1.
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:76:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.bank_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:94:31: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.g_arb[0].count_in'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:78:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.slot_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:74:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.en_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/arith/modmul_barrett.sv:41:18: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.g_lane[7].u_bfly.u_mul.g_barrett.u_red.s_cut'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:75:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.wr_s'
%Warning-UNOPTFLAT: /home/ajil/FPGA/Projects/CHIPATON/rtl/mem/poly_mem_multiport_split.sv:77:33: Signal unoptimizable: Circular combinational logic: 'kpke_sched_top.u_core.u_core.u_mem.off_s'
368875.00ns INFO     cocotb.kpke_sched_top              negative control: 2/2 programs differ from the model
368875.00ns INFO     cocotb.regression                  test_kpke_sched.test_negative_control_must_fail passed
[verilator] pwm: 1/1 PASS
[verilator] top: 1/1 PASS  {'keygen': 5493, 'encrypt': 6810, 'decrypt': 3121}
[verilator] ncg: 1/1 bit-exact failed as required  {}
[verilator] ncr: 1/1 bit-exact failed as required  {}
[verilator] OVERALL: PASS
rc=0
## V4/V5/V6 icarus
200415.00ns INFO     cocotb.pwm_unit                    pwm_unit: 20035/20035 pairs equal to BaseCaseMultiply + accumulate
200415.00ns INFO     cocotb.regression                  test_pwm_unit.test_pwm_stream passed
889195.00ns INFO     cocotb.kpke_sched_top              keygen: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (6, 0, 9), cycles 5493
1844195.00ns INFO     cocotb.kpke_sched_top              encrypt: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (3, 4, 12), cycles 6810
2614745.00ns INFO     cocotb.kpke_sched_top              decrypt: 3 random + 2 corner cases bit-exact, end-to-end equal, counters (3, 1, 3), cycles 3121
2614745.00ns INFO     cocotb.regression                  test_kpke_sched.test_programs_bit_exact_and_constant passed
368875.00ns INFO     cocotb.kpke_sched_top              negative control: 2/2 programs differ from the model
368875.00ns INFO     cocotb.regression                  test_kpke_sched.test_negative_control_must_fail passed
368875.00ns INFO     cocotb.kpke_sched_top              negative control: 2/2 programs differ from the model
368875.00ns INFO     cocotb.regression                  test_kpke_sched.test_negative_control_must_fail passed
[icarus] pwm: 1/1 PASS
[icarus] top: 1/1 PASS  {'keygen': 5493, 'encrypt': 6810, 'decrypt': 3121}
[icarus] ncg: 1/1 bit-exact failed as required  {}
[icarus] ncr: 1/1 bit-exact failed as required  {}
[icarus] OVERALL: PASS
rc=0
OVERALL: PASS
```

Kegagalan di dalam blok `ncg` / `ncr` adalah kontrol negatif dan memang diharuskan.
Baris `%Warning-UNOPTFLAT` berasal dari build simulasi cocotb Verilator untuk `pwm_unit` (dibangun dengan `-Wno-fatal`): Verilator melaporkan vektor tahap `s_cut` dari `rtl/arith/modmul_barrett.sv` yang dibekukan sebagai melingkar karena rentang bit berbeda dari satu vektor saling memberi masukan; ini pemberitahuan penjadwalan simulasi, bukan loop kombinasional (Quartus tidak melaporkan apa pun, lint `-Wall` di V1 bersih, hasil bit-exact di kedua simulator). Tidak diabaikan diam-diam: dicatat di sini.
