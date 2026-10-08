# ADR 0002: Lingkup dan kebijakan klaim - matematika dikunci

- Status: Accepted
- Tanggal: 2026-09-28
- Diputuskan oleh: tim J5 (dasar: pernyataan di Bagian 1-2 proposal tim: prinsip desain, "Batasan", tabel inti / tahap lanjut / di luar lingkup)

## Konteks
Proposal mengklaim kesesuaian dengan FIPS 203 dan perilaku waktu-konstan, dan memisahkan tahap inti
dari pekerjaan tahap lanjut. Juri menilai bukti; klaim tanpa dukungan mahal akibatnya.

## Keputusan
1. Parameter ML-KEM-768 (q, n, k, eta, du, dv, akar satuan) dan semua definisi aritmetika
   tidak diubah. Inovasi hanya di arsitektur perangkat keras.
2. Kata-kata keamanan: "dirancang mengikuti standar pasca-kuantum", tidak pernah "quantum-proof".
3. Ketahanan side-channel (daya/EM) tidak diklaim pada tahap inti. Klaim inti:
   waktu-konstan secara konstruksi, ditunjukkan lewat invarian jumlah siklus. TVLA dan masking
   adalah tahap lanjut.
4. Semua angka sumber daya, timing, dan kinerja berasal dari laporan Quartus atau pengukuran papan
   (`evidence/`); selain itu diberi label ESTIMATE.
5. Tingkat lingkup: inti / lanjut / di luar lingkup.

## Konsekuensi
Aturan ini dijaga lewat pemeriksaan parameter terkunci dan pemeriksa klaim.
Permintaan mengubah item yang dikunci memerlukan ADR baru yang menggantikan ADR ini.

## Bukti
Bagian 1-2 proposal.
