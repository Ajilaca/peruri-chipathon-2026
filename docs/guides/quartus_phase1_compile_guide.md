# Panduan compile Quartus untuk Fase 1 (config C0) — ntt_core

**Ditulis untuk:** dipakai sendiri oleh Faza (Team J5), dan/atau ditempel ke ChatGPT supaya
ChatGPT bisa membimbing step-by-step di layar (Quartus Prime Lite, GUI, seperti screenshot yang
sudah dibuka). Berisi konteks proyek secukupnya supaya ChatGPT tidak perlu menebak-nebak.

## 0. Konteks (baca dulu, jangan skip)

- Proyek: akselerator ML-KEM-768 (FIPS 203) di Terasic DE10-Nano, chip **Cyclone V
  5CSEBA6U23I7**. Repo: `CHIPATON`, branch kerja saat ini: `phase1-ntt-baseline`.
- Yang mau dikompilasi: `rtl/ntt/ntt_core.sv` (dan modul-modul di bawahnya) — ini adalah
  **konfigurasi C0**: NTT/INTT baseline, 1 lane, 1 butterfly per siklus, memori belum di-bank.
  Semua sudah lolos simulasi (cocotb, Verilator + Icarus, 10/10) dan lolos lint
  (`verilator --lint-only -Wall`, `slang`) dan bukti formal (SymbiYosys). **Yang BELUM ada dan
  jadi tujuan compile ini: angka ALM, register, M10K, DSP, Fmax, slack dari Quartus.**
- **Aturan keras proyek (jangan dilanggar, ini bukan saran, ini rule):**
  1. Angka resource/timing FPGA **hanya boleh** berasal dari Quartus. Tidak ada Yosys, tidak ada
     estimasi, tidak ada tebakan. Kalau Quartus belum jalan, angkanya belum ada — titik.
  2. **Jangan hafalkan/isi manual** angka ALM dsb ke dokumen manapun. Semua ditulis ulang oleh
     skrip ekstraksi dari laporan Quartus asli (lihat Bagian 3).
  3. Ini kompilasi **kernel-only** (belum ada board, belum ada HPS): semua port harus jadi
     **Virtual Pin** supaya Quartus tidak memasang I/O buffer fisik yang mendistorsi angka ALM
     dan timing (lihat Bagian 2 langkah 6).
  4. Clock target **belum diputuskan resmi oleh tim** (belum ada ADR). Compile ini pakai clock
     **provisional** (sementara, akan dicatat sebagai ESTIMATE proses, bukan keputusan final).
     Jangan biarkan siapa pun (termasuk ChatGPT) menyimpulkan "clock final-nya X MHz" dari
     compile ini saja.
  5. File hasil compile Quartus (`output_files/`, `db/`, `.qws`, dst.) **TIDAK di-commit ke git**
     (sudah di `.gitignore`). Yang di-commit hanya **hasil ekstraksi** (file `.md`) yang dibuat
     skrip di Bagian 3.
  6. Kalau ada **Critical Warning** dari Quartus: jangan diabaikan diam-diam. Catat apa isinya,
     dan apakah itu bisa diterima (biasanya "boleh" hanya untuk hal yang memang diharapkan,
     seperti "unassigned pins" karena kita sengaja pakai virtual pin).
  7. **Timing tidak "closed"** kalau ada slack negatif (setup ATAU hold, di semua kondisi/corner).
     Kalau slack negatif, laporkan apa adanya — jangan bilang "timing closed".

## 1. Yang perlu disiapkan sebelum buka Quartus

Dari terminal (WSL/Linux tempat repo ini berada), buat folder proyek Quartus untuk revisi C0:

```bash
cd ~/FPGA/Projects/CHIPATON      # sesuaikan path repo Anda
mkdir -p quartus/phase01_ntt_c0
```

Buat 3 file di folder itu (bisa lewat `nano`/`vim`/VS Code, TIDAK perlu lewat GUI Quartus untuk
langkah ini — lebih cepat dan tidak salah ketik):

**`quartus/phase01_ntt_c0/phase01_ntt_c0.qpf`**
```
QUARTUS_VERSION = "25.1"
PROJECT_REVISION = "C0"
```

**`quartus/phase01_ntt_c0/C0.qsf`** — perhatikan: nama file HARUS sama dengan `PROJECT_REVISION`
di atas (`C0.qsf`), itu aturan Quartus, bukan pilihan bebas.
```tcl
set_global_assignment -name FAMILY "Cyclone V"
set_global_assignment -name DEVICE 5CSEBA6U23I7
set_global_assignment -name TOP_LEVEL_ENTITY ntt_core
set_global_assignment -name PROJECT_OUTPUT_DIRECTORY output_files
set_global_assignment -name SDC_FILE C0.sdc

set_global_assignment -name SYSTEMVERILOG_FILE ../../rtl/ntt/ntt_pkg.sv
set_global_assignment -name SYSTEMVERILOG_FILE ../../rtl/ntt/twiddle_rom.sv
set_global_assignment -name SYSTEMVERILOG_FILE ../../rtl/ntt/modmul_reduce.sv
set_global_assignment -name SYSTEMVERILOG_FILE ../../rtl/ntt/base_case_multiply.sv
set_global_assignment -name SYSTEMVERILOG_FILE ../../rtl/ntt/butterfly.sv
set_global_assignment -name SYSTEMVERILOG_FILE ../../rtl/ntt/poly_mem.sv
set_global_assignment -name SYSTEMVERILOG_FILE ../../rtl/ntt/ntt_core.sv

# Kernel-only: semua port jadi virtual pin (tidak dipasang ke pin fisik), supaya I/O buffer
# tidak mendistorsi ALM/timing (docs/ROADMAP.md, "Measurement protocol").
set_instance_assignment -name VIRTUAL_PIN ON -to clk_i
set_instance_assignment -name VIRTUAL_PIN ON -to rst_ni
set_instance_assignment -name VIRTUAL_PIN ON -to mode_i
set_instance_assignment -name VIRTUAL_PIN ON -to start_i
set_instance_assignment -name VIRTUAL_PIN ON -to host_addr_i[*]
set_instance_assignment -name VIRTUAL_PIN ON -to host_wdata_i[*]
set_instance_assignment -name VIRTUAL_PIN ON -to host_we_i
set_instance_assignment -name VIRTUAL_PIN ON -to host_rdata_o[*]
set_instance_assignment -name VIRTUAL_PIN ON -to busy_o
set_instance_assignment -name VIRTUAL_PIN ON -to done_o
```

**`quartus/phase01_ntt_c0/C0.sdc`**
```tcl
# Clock PROVISIONAL, belum ADR resmi tim (docs/ROADMAP.md: "constrain with a documented
# provisional period and report Fmax; never state a latency without its clock").
# 50 MHz dipilih hanya karena itu clock referensi FPGA on-board DE10-Nano (lihat
# scripts/smoke/quartus/smoke.sdc) -- BUKAN keputusan akhir clock C0.
create_clock -name clk_i -period 20.000 [get_ports {clk_i}]
derive_clock_uncertainty

# rst_ni asinkron, tidak ada relasi timing dengan clk_i -- didokumentasikan di sini, bukan
# dibiarkan tanpa penjelasan (CLAUDE.md aturan #7).
set_false_path -from [get_ports {rst_ni}]
```

## 2. Buka dan compile di Quartus GUI (sesuai screenshot Anda)

1. **File > Open Project...** → arahkan ke
   `quartus/phase01_ntt_c0/phase01_ntt_c0.qpf` → Open.
   (Karena file `.qpf`/`.qsf` sudah dibuat manual di Bagian 1, Anda TIDAK perlu memakai
   "New Project Wizard" — wizard itu untuk membuat proyek dari nol lewat GUI, hasilnya sama saja
   dengan file yang sudah kita tulis tangan, dan menulis tangan lebih mudah direproduksi/di-review
   tim.)
2. Setelah proyek terbuka, cek **Project Navigator > Hierarchy**: harus muncul `ntt_core` sebagai
   top-level (mungkin perlu klik kanan → "Refresh" kalau belum muncul).
3. **Processing > Start Compilation** (atau klik tombol segitiga hijau di toolbar, ini yang
   terlihat di toolbar screenshot Anda). Ini menjalankan seluruh alur: Analysis & Synthesis →
   Fitter (Place & Route) → Assembler → Timing Analysis, sesuai daftar di panel **Tasks** kiri
   bawah pada screenshot Anda.
4. **Tunggu.** Untuk modul sekecil ini (~256 titik memori, beberapa ratus baris logika) biasanya
   hanya beberapa menit, jauh lebih cepat dari compile IP besar.
5. **Perhatikan panel Messages** di bawah selama compile jalan:
   - Warna merah (Error) → compile gagal, baca pesannya, biasanya salah path file atau nama top
     level salah ketik.
   - Kuning dengan tanda seru merah (**Critical Warning**) → catat isinya persis, jangan
     diabaikan. Untuk kompilasi virtual-pin, wajar muncul critical warning soal "pin tidak
     ditempatkan" — itu memang disengaja (lihat Bagian 0 poin 3).
6. **Kalau Virtual Pin di langkah 1 (file .qsf) tidak terbaca/tidak berlaku** (kadang perlu
   compile sekali dulu supaya semua node dikenali Quartus): buka **Assignments > Assignment
   Editor**, klik **Node Finder**, filter kosongkan lalu klik List (menampilkan semua pin), pilih
   semua baris, lalu di kolom Assignment Name pilih **Virtual Pin**, Value **On**, lalu compile
   ulang.
7. Setelah selesai (Tasks di kiri semua bertanda centang hijau, atau minimal Fitter dan Timing
   Analysis), buka:
   - **Processing > Compilation Report** untuk lihat ringkasan ALM/register/M10K/DSP langsung di
     GUI (panel "Fitter > Summary").
   - **Processing > Compilation Report > Timing Analyzer > Fmax Summary** untuk Fmax.
   - **Processing > Compilation Report > Timing Analyzer > Slow 1100mV 0C Model > Setup/Hold
     Summary** untuk worst slack.

## 3. Ubah laporan Quartus jadi bukti MEASURED di repo (WAJIB, jangan skip)

Kembali ke terminal:

```bash
cd ~/FPGA/Projects/CHIPATON
. scripts/env.sh
python3 .claude/skills/quartus-report/scripts/extract_quartus_report.py \
    quartus/phase01_ntt_c0/output_files C0 \
    --log quartus/phase01_ntt_c0/output_files/C0.flow.rpt \
    --note "commit 5d5ee74, config C0 (L=1), clock provisional 50 MHz (BELUM ADR tim)"
```

(`--log` menunjuk ke `<revisi>.flow.rpt` di `output_files/` — file ini dibuat otomatis oleh
Quartus, baik lewat GUI maupun CLI, dan dipakai skrip untuk menghitung baris "Critical Warning".
Kalau nama filenya sedikit beda di instalasi Anda, cek isi folder `output_files/` dulu dengan
`ls quartus/phase01_ntt_c0/output_files/`.)

Ini akan membuat `docs/evidence/quartus/C0-<tanggal-UTC>.md` berisi: ringkasan fitter (ALM,
register, M10K, DSP — dikutip persis dari Quartus, termasuk denominator/total-nya), tabel slack,
worst setup/hold slack, panel Fmax kalau ketemu, dan jumlah Critical Warning/Warning/Error dari
log. **File inilah yang jadi bukti "MEASURED"** — bukan yang Anda ketik manual.

Kalau skrip bilang "Fmax not found" atau parsernya salah baca, itu memang disebutkan sebagai
keterbatasan yang diketahui (`.claude/skills/quartus-report/SKILL.md`, "Known limits" — parser
belum teruji di Quartus 25.1 asli). Kalau begitu: buka `output_files/C0.sta.rpt` secara manual,
cari panel "Fmax Summary", dan salin angkanya sendiri ke laporan — jangan hitung Fmax sendiri dari
slack.

## 4. Setelah dapat angka: langkah lanjutan (bukan bagian compile, tapi supaya tidak lupa)

1. **Buat ADR clock target** (belum ada; ini keputusan tim, bukan keputusan teknis semata).
   Pakai skill `/decision-record` di sesi Claude Code, atau catat manual di
   `docs/decisions/000X-target-clock-c0.md` mengikuti format ADR yang sudah ada.
2. Isi baris **C0** di tabel "Optimisation ablation matrix" (`docs/ROADMAP.md`, dekat akhir file)
   dengan angka dari file evidence di atas, plus kolom Evidence diisi path filenya.
3. Update `docs/results/result_phase1.md`: baris CRG-9 dari `MISSING` jadi `PASS` (evidence =
   path file di Bagian 3), baris "Target-clock ADR recorded" jadi `PASS` kalau ADR sudah dibuat.
   Validasi lagi:
   ```bash
   python3 .claude/skills/phase-gate/scripts/check_result.py docs/results/result_phase1.md
   ```
   Status baru boleh diubah ke `DONE` **hanya kalau semua baris di tabel kriteria PASS**.
4. **Centang kotak Approval** di `docs/results/result_phase1.md` bagian akhir sendiri (nama +
   tanggal) — ini harus tindakan manusia, bukan AI manapun.
5. Baru boleh mulai Fase 2 (`docs/ROADMAP.md`, memori/banking M10K).

## 5. Hal-hal yang sering salah (checklist sebelum lapor "sudah compile")

- [ ] Top-level entity yang dipilih benar **`ntt_core`** (bukan salah satu sub-modulnya).
- [ ] Semua 7 file `.sv` di `rtl/ntt/` masuk daftar Files proyek (cek **Project Navigator >
      Files**), termasuk `ntt_pkg.sv` (mudah lupa karena isinya cuma `package`, bukan `module`).
- [ ] Semua port memang Virtual Pin (cek Assignment Editor), bukan ke-assign pin fisik acak.
- [ ] SDC benar-benar ke-load (cek Compilation Report > TimeQuest Timing Analyzer, harus ada 1
      clock `clk_i` terdaftar, bukan "No user-specified sdc").
- [ ] Tidak ada **Error** merah di Messages (Critical Warning boleh, Error tidak boleh).
- [ ] Angka ALM/M10K/DSP yang dilaporkan **dikutip dari fitter**, dengan denominator (total
      tersedia) yang JUGA dikutip dari fitter yang sama — jangan campur dengan angka datasheet
      Intel (`CLAUDE.md`: keduanya bisa beda, dan itu boleh terjadi, tapi harus konsisten sumber).
- [ ] Sudah jalankan `extract_quartus_report.py` dan file `docs/evidence/quartus/C0-*.md` benar
      ada isinya (bukan kosong/error parsing).
- [ ] Belum ada klaim "timing closed" kalau slack negatif di mana pun.
