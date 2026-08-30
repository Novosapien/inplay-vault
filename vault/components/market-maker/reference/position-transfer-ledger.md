# Position-Transfer Ledger — account 1797733477

> **Purpose:** the endpoint is one-way and NOT idempotent, and the venue
> has no position read-back — so this ledger is the only complete record
> of what was seeded (Hasan's rule, trading-ops guide §7). Every
> transfer, ever, goes here. A retry after a timeout is FORBIDDEN until
> the gateway journal has been checked against this table.

## 2026-08-07 — the supervised-test seed (George's direction; run by Claude)

100,000 shares per ticker, cost basis at Edwin's IPO-sheet prices.
All seven accepted (`UPTa`, gateway journal 16:57:28–16:57:34 UTC, FIX
seq 3126–3132). Verified behaviourally: a side-2 sell on IPTCEAGL —
"not long"-rejected the day before — was ACCEPTED then cancelled
(MMSEEDVER1).

| ClOrdID | Symbol | txfrQty | txfrCost | Basis | Reply |
|---|---|---|---|---|---|
| Thl4l1s77qa | IPTCEAGL | +100,000 | $7,779,000 | $77.79 | UPTa |
| Thl4l1st6a4 | IPTCPATR | +100,000 | $7,979,000 | $79.79 | UPTa |
| Thl4l1tf32v | IPTCBILL | +100,000 | $7,451,000 | $74.51 | UPTa |
| Thl4l1u0ytj | IPTCGIAN | +100,000 | $6,110,000 | $61.10 | UPTa |
| Thl4l1umuyx | IPTCCOWB | +100,000 | $7,618,000 | $76.18 | UPTa |
| Thl4l1v8rii | IPTCSTEE | +100,000 | $6,634,000 | $66.34 | UPTa |
| Thl4l1vunmo | IPTCJETS | +100,000 | $4,543,000 | $45.43 | UPTa |

**Running position per this ledger:** 100,000 of each of the seven.
(Plus the two 07-08 wash-probe fills on IPTCEAGL, +100/−100 = net 0.)

## 2026-08-11 — the full-book seed (George's ruled task 1; run by Claude)

100,000 shares per ticker for every symbol not already seeded: the 163
remaining production tickers + the ten `.TEST` twins (the gateway's full
180-symbol config, source `internal/config/symbols.go`). Cost basis =
the `Listed IPO` column of `reference/ipo-prices-170.csv` (a `.TEST`
symbol carries its production twin's price). **All 173 accepted** —
UPTa replies verified one-for-one against the submitted ClOrdIDs, qty
and cost (gateway journal 22:20–22:3x UTC; submission log
`~/seed-log-20260811.jsonl` on the gateway VM). The canary was
IPTCRAVE, sent alone and verified before the bulk run. ⚠ The `.TEST`
venue books accepted transfers — evidence the ten symbols are live at
the OMS, not just subscribed.

⚠ Basis note: the 08-07 seven were seeded at Edwin's IPO-sheet prices
(e.g. BILL $74.51); this run uses `ipo-prices-170.csv` `Listed IPO`
(BILL would be $77.27). The two sheets differ — the seven keep their
08-07 basis, unchanged by this run.

| ClOrdID | Symbol | txfrQty | txfrCost | Basis | Reply |
|---|---|---|---|---|---|
| Thl98qibt34 | IPTC49ER | +100,000 | $7,427,000 | $74.27 | UPTa |
| Thl98qiicjz | IPTCAFFC | +100,000 | $5,175,000 | $51.75 | UPTa |
| Thl98qiovu7 | IPTCAKRZ | +100,000 | $3,601,000 | $36.01 | UPTa |
| Thl98qivf29 | IPTCAPST | +100,000 | $4,575,000 | $45.75 | UPTa |
| Thl98qj1y9b | IPTCARKR | +100,000 | $4,567,000 | $45.67 | UPTa |
| Thl98qj8h31 | IPTCARMB | +100,000 | $5,623,000 | $56.23 | UPTa |
| Thl98qjf0b9 | IPTCAUBT | +100,000 | $4,859,000 | $48.59 | UPTa |
| Thl98qjljop | IPTCAZSD | +100,000 | $4,833,000 | $48.33 | UPTa |
| Thl98qjs2ua | IPTCAZWC | +100,000 | $5,124,000 | $51.24 | UPTa |
| Thl98qjylve | IPTCBADG | +100,000 | $4,923,000 | $49.23 | UPTa |
| Thl98qk54wf | IPTCBAMA | +100,000 | $6,045,000 | $60.45 | UPTa |
| Thl98qkbo8c | IPTCBAYB | +100,000 | $4,391,000 | $43.91 | UPTa |
| Thl98qki7h0 | IPTCBCEA | +100,000 | $2,765,000 | $27.65 | UPTa |
| Thl98qkoqga | IPTCBEAR | +100,000 | $6,753,000 | $67.53 | UPTa |
| Thl98qkv99k | IPTCBENG | +100,000 | $7,176,000 | $71.76 | UPTa |
| Thl98ql1s7i | IPTCBGFL | +100,000 | $3,892,000 | $38.92 | UPTa |
| Thl98ql8b0w | IPTCBLSC | +100,000 | $3,077,000 | $30.77 | UPTa |
| Thl98qleu08 | IPTCBOIL | +100,000 | $2,808,000 | $28.08 | UPTa |
| Thl98qlldbo | IPTCBRON | +100,000 | $6,961,000 | $69.61 | UPTa |
| Thl98qlrxt4 | IPTCBROW | +100,000 | $4,673,000 | $46.73 | UPTa |
| Thl98qlyh8o | IPTCBSST | +100,000 | $5,699,000 | $56.99 | UPTa |
| Thl98qm506p | IPTCBUCC | +100,000 | $6,071,000 | $60.71 | UPTa |
| Thl98qmbj9w | IPTCBUCK | +100,000 | $6,895,000 | $68.95 | UPTa |
| Thl98qmi29a | IPTCBUFB | +100,000 | $4,464,000 | $44.64 | UPTa |
| Thl98qmol0o | IPTCBYUC | +100,000 | $6,090,000 | $60.90 | UPTa |
| Thl98qmv4dn | IPTCCAGB | +100,000 | $4,518,000 | $45.18 | UPTa |
| Thl98qn1ngc | IPTCCARD | +100,000 | $3,566,000 | $35.66 | UPTa |
| Thl98qn869h | IPTCCCCH | +100,000 | $3,863,000 | $38.63 | UPTa |
| Thl98qnep97 | IPTCCH49 | +100,000 | $2,130,000 | $21.30 | UPTa |
| Thl98qnl8gv | IPTCCHAR | +100,000 | $6,926,000 | $69.26 | UPTa |
| Thl98qnrrkz | IPTCCHIE | +100,000 | $7,395,000 | $73.95 | UPTa |
| Thl98qnyafs | IPTCCINB | +100,000 | $3,941,000 | $39.41 | UPTa |
| Thl98qo4tjr | IPTCCLEM | +100,000 | $5,687,000 | $56.87 | UPTa |
| Thl98qobcnj | IPTCCMCH | +100,000 | $4,669,000 | $46.69 | UPTa |
| Thl98qohvk0 | IPTCCOLB | +100,000 | $3,507,000 | $35.07 | UPTa |
| Thl98qooeyc | IPTCCOLT | +100,000 | $5,824,000 | $58.24 | UPTa |
| Thl98qouy7q | IPTCCOMM | +100,000 | $5,736,000 | $57.36 | UPTa |
| Thl98qp1h4x | IPTCCONH | +100,000 | $4,179,000 | $41.79 | UPTa |
| Thl98qp80bu | IPTCCOSR | +100,000 | $3,213,000 | $32.13 | UPTa |
| Thl98qpejbu | IPTCDELB | +100,000 | $4,492,000 | $44.92 | UPTa |
| Thl98qpl2ci | IPTCDOLP | +100,000 | $3,838,000 | $38.38 | UPTa |
| Thl98qprl1o | IPTCDUKE | +100,000 | $4,243,000 | $42.43 | UPTa |
| Thl98qpy484 | IPTCECAP | +100,000 | $5,143,000 | $51.43 | UPTa |
| Thl98qq4ncy | IPTCEMEA | +100,000 | $4,411,000 | $44.11 | UPTa |
| Thl98qqb69r | IPTCFALC | +100,000 | $5,488,000 | $54.88 | UPTa |
| Thl98qqhp7z | IPTCFAOW | +100,000 | $4,405,000 | $44.05 | UPTa |
| Thl98qqo8ll | IPTCFIUP | +100,000 | $4,546,000 | $45.46 | UPTa |
| Thl98qquru5 | IPTCFLSS | +100,000 | $4,615,000 | $46.15 | UPTa |
| Thl98qr1azt | IPTCFRSB | +100,000 | $5,057,000 | $50.57 | UPTa |
| Thl98qr7uqu | IPTCGASP | +100,000 | $3,166,000 | $31.66 | UPTa |
| Thl98qredvl | IPTCGATO | +100,000 | $5,131,000 | $51.31 | UPTa |
| Thl98qrkwj0 | IPTCGOPH | +100,000 | $4,494,000 | $44.94 | UPTa |
| Thl98qrrftr | IPTCGSEA | +100,000 | $3,864,000 | $38.64 | UPTa |
| Thl98qrxyuk | IPTCGTYJ | +100,000 | $4,706,000 | $47.06 | UPTa |
| Thl98qs4hwv | IPTCHAWA | +100,000 | $5,302,000 | $53.02 | UPTa |
| Thl98qsb0z9 | IPTCHFRG | +100,000 | $4,990,000 | $49.90 | UPTa |
| Thl98qshkaq | IPTCHOOS | +100,000 | $6,822,000 | $68.22 | UPTa |
| Thl98qso39p | IPTCHOUC | +100,000 | $5,575,000 | $55.75 | UPTa |
| Thl98qsum5o | IPTCHUSK | +100,000 | $4,670,000 | $46.70 | UPTa |
| Thl98qt152x | IPTCIACL | +100,000 | $3,814,000 | $38.14 | UPTa |
| Thl98qt7o0z | IPTCIAHW | +100,000 | $5,498,000 | $54.98 | UPTa |
| Thl98qte72v | IPTCILLI | +100,000 | $4,980,000 | $49.80 | UPTa |
| Thl98qtkq83 | IPTCJAGU | +100,000 | $6,324,000 | $63.24 | UPTa |
| Thl98qtr950 | IPTCJKSC | +100,000 | $5,231,000 | $52.31 | UPTa |
| Thl98qtxs7j | IPTCJMDU | +100,000 | $6,042,000 | $60.42 | UPTa |
| Thl98qu4b1u | IPTCKSGF | +100,000 | $2,924,000 | $29.24 | UPTa |
| Thl98quau0z | IPTCKSJH | +100,000 | $4,450,000 | $44.50 | UPTa |
| Thl98quhd95 | IPTCKSOW | +100,000 | $4,529,000 | $45.29 | UPTa |
| Thl98qunvzw | IPTCKSWC | +100,000 | $5,793,000 | $57.93 | UPTa |
| Thl98quuez9 | IPTCKYWC | +100,000 | $3,831,000 | $38.31 | UPTa |
| Thl98qv0y50 | IPTCLARC | +100,000 | $5,163,000 | $51.63 | UPTa |
| Thl98qv7hej | IPTCLATB | +100,000 | $4,459,000 | $44.59 | UPTa |
| Thl98qve08l | IPTCLIBF | +100,000 | $5,804,000 | $58.04 | UPTa |
| Thl98qvkjbx | IPTCLION | +100,000 | $7,610,000 | $76.10 | UPTa |
| Thl98qvr240 | IPTCLOUC | +100,000 | $5,686,000 | $56.86 | UPTa |
| Thl98qvxkzy | IPTCLSUT | +100,000 | $5,954,000 | $59.54 | UPTa |
| Thl98qw43tm | IPTCMEMT | +100,000 | $5,377,000 | $53.77 | UPTa |
| Thl98qwamey | IPTCMIHU | +100,000 | $7,157,000 | $71.57 | UPTa |
| Thl98qwh5he | IPTCMIOH | +100,000 | $5,217,000 | $52.17 | UPTa |
| Thl98qwnoga | IPTCMISP | +100,000 | $3,504,000 | $35.04 | UPTa |
| Thl98qwu7em | IPTCMIWV | +100,000 | $5,726,000 | $57.26 | UPTa |
| Thl98qx0qle | IPTCMIZO | +100,000 | $4,813,000 | $48.13 | UPTa |
| Thl98qx79jo | IPTCMOST | +100,000 | $3,285,000 | $32.85 | UPTa |
| Thl98qxdsof | IPTCMRSH | +100,000 | $5,242,000 | $52.42 | UPTa |
| Thl98qxkbj1 | IPTCMSST | +100,000 | $3,579,000 | $35.79 | UPTa |
| Thl98qxquvl | IPTCMTBR | +100,000 | $3,302,000 | $33.02 | UPTa |
| Thl98qxxdm7 | IPTCNAVY | +100,000 | $5,822,000 | $58.22 | UPTa |
| Thl98qy3waz | IPTCNCTH | +100,000 | $3,899,000 | $38.99 | UPTa |
| Thl98qyafh8 | IPTCNCWP | +100,000 | $5,250,000 | $52.50 | UPTa |
| Thl98qygy3t | IPTCNDFI | +100,000 | $7,275,000 | $72.75 | UPTa |
| Thl98qynh76 | IPTCNDSU | +100,000 | $7,063,000 | $70.63 | UPTa |
| Thl98qyu0as | IPTCNEVW | +100,000 | $3,443,000 | $34.43 | UPTa |
| Thl98qz0jaq | IPTCNIHU | +100,000 | $2,980,000 | $29.80 | UPTa |
| Thl98qz72aj | IPTCNMLB | +100,000 | $5,680,000 | $56.80 | UPTa |
| Thl98qzdllx | IPTCNMSA | +100,000 | $3,528,000 | $35.28 | UPTa |
| Thl98qzk4pp | IPTCNTMG | +100,000 | $4,297,000 | $42.97 | UPTa |
| Thl98qzqnrg | IPTCNWWC | +100,000 | $4,012,000 | $40.12 | UPTa |
| Thl98qzx6ot | IPTCODMO | +100,000 | $5,357,000 | $53.57 | UPTa |
| Thl98r03pf6 | IPTCOHBO | +100,000 | $5,040,000 | $50.40 | UPTa |
| Thl98r0a8cq | IPTCOKST | +100,000 | $4,548,000 | $45.48 | UPTa |
| Thl98r0grbq | IPTCOLMR | +100,000 | $5,625,000 | $56.25 | UPTa |
| Thl98r0naaw | IPTCORDU | +100,000 | $6,862,000 | $68.62 | UPTa |
| Thl98r0tthc | IPTCORST | +100,000 | $3,337,000 | $33.37 | UPTa |
| Thl98r10cmo | IPTCPACK | +100,000 | $7,083,000 | $70.83 | UPTa |
| Thl98r16vmy | IPTCPANT | +100,000 | $5,453,000 | $54.53 | UPTa |
| Thl98r1dexq | IPTCPITT | +100,000 | $5,495,000 | $54.95 | UPTa |
| Thl98r1jy4p | IPTCPSNL | +100,000 | $6,251,000 | $62.51 | UPTa |
| Thl98r1qh53 | IPTCRAID | +100,000 | $4,913,000 | $49.13 | UPTa |
| Thl98r1wzxt | IPTCRAMS | +100,000 | $8,120,000 | $81.20 | UPTa |
| Thl98pme764 | IPTCRAVE | +100,000 | $7,746,000 | $77.46 | UPTa |
| Thl98r23iza | IPTCRAZR | +100,000 | $3,372,000 | $33.72 | UPTa |
| Thl98r2a2bo | IPTCRICE | +100,000 | $2,965,000 | $29.65 | UPTa |
| Thl98r2gl2g | IPTCRUTG | +100,000 | $3,753,000 | $37.53 | UPTa |
| Thl98r2n4cn | IPTCSACS | +100,000 | $4,994,000 | $49.94 | UPTa |
| Thl98r2tn7h | IPTCSAIN | +100,000 | $5,858,000 | $58.58 | UPTa |
| Thl98r3060i | IPTCSALJ | +100,000 | $4,397,000 | $43.97 | UPTa |
| Thl98r36oxl | IPTCSCGC | +100,000 | $4,571,000 | $45.71 | UPTa |
| Thl98r3d7vy | IPTCSDAZ | +100,000 | $4,934,000 | $49.34 | UPTa |
| Thl98r3jr1h | IPTCSEHW | +100,000 | $7,505,000 | $75.05 | UPTa |
| Thl98r3qaam | IPTCSHBK | +100,000 | $2,773,000 | $27.73 | UPTa |
| Thl98r3wtf4 | IPTCSJSP | +100,000 | $3,848,000 | $38.48 | UPTa |
| Thl98r43cj6 | IPTCSMGE | +100,000 | $3,156,000 | $31.56 | UPTa |
| Thl98r49vt8 | IPTCSMUM | +100,000 | $6,019,000 | $60.19 | UPTa |
| Thl98r4gem6 | IPTCSOON | +100,000 | $5,570,000 | $55.70 | UPTa |
| Thl98r4mxh0 | IPTCSTAN | +100,000 | $3,165,000 | $31.65 | UPTa |
| Thl98r4tg7z | IPTCSYRO | +100,000 | $3,635,000 | $36.35 | UPTa |
| Thl98r4zz3l | IPTCTEMP | +100,000 | $4,055,000 | $40.55 | UPTa |
| Thl98r56ie9 | IPTCTERP | +100,000 | $3,977,000 | $39.77 | UPTa |
| Thl98r5d14m | IPTCTEXS | +100,000 | $6,961,000 | $69.61 | UPTa |
| Thl98r5jk24 | IPTCTITA | +100,000 | $5,016,000 | $50.16 | UPTa |
| Thl98r5q2xz | IPTCTOLR | +100,000 | $5,497,000 | $54.97 | UPTa |
| Thl98r5wlpu | IPTCTROY | +100,000 | $4,992,000 | $49.92 | UPTa |
| Thl98r634sy | IPTCTULN | +100,000 | $5,184,000 | $51.84 | UPTa |
| Thl98r69np6 | IPTCTULS | +100,000 | $4,087,000 | $40.87 | UPTa |
| Thl98r6g6ha | IPTCTXAM | +100,000 | $5,819,000 | $58.19 | UPTa |
| Thl98r6mp92 | IPTCTXLH | +100,000 | $6,381,000 | $63.81 | UPTa |
| Thl98r6t83h | IPTCTXSB | +100,000 | $4,447,000 | $44.47 | UPTa |
| Thl98r6zrdo | IPTCTXTR | +100,000 | $7,410,000 | $74.10 | UPTa |
| Thl98r76aab | IPTCUABB | +100,000 | $2,998,000 | $29.98 | UPTa |
| Thl98r7ct7b | IPTCUCFK | +100,000 | $4,439,000 | $44.39 | UPTa |
| Thl98r7jbyn | IPTCUCLA | +100,000 | $4,600,000 | $46.00 | UPTa |
| Thl98r7puxw | IPTCUGAG | +100,000 | $6,874,000 | $68.74 | UPTa |
| Thl98r7wdwb | IPTCULMW | +100,000 | $3,004,000 | $30.04 | UPTa |
| Thl98r82wwf | IPTCUMAM | +100,000 | $2,600,000 | $26.00 | UPTa |
| Thl98r89g3g | IPTCUNLV | +100,000 | $5,736,000 | $57.36 | UPTa |
| Thl98r8fyx2 | IPTCUSCJ | +100,000 | $5,770,000 | $57.70 | UPTa |
| Thl98r8mi48 | IPTCUSFB | +100,000 | $5,739,000 | $57.39 | UPTa |
| Thl98r8t0zq | IPTCUTEP | +100,000 | $2,795,000 | $27.95 | UPTa |
| Thl98r8zjsa | IPTCUTES | +100,000 | $6,011,000 | $60.11 | UPTa |
| Thl98r962o7 | IPTCUTRN | +100,000 | $5,378,000 | $53.78 | UPTa |
| Thl98r9clxy | IPTCUTST | +100,000 | $3,807,000 | $38.07 | UPTa |
| Thl98r9j4pv | IPTCVACV | +100,000 | $5,488,000 | $54.88 | UPTa |
| Thl98r9pndt | IPTCVAND | +100,000 | $4,211,000 | $42.11 | UPTa |
| Thl98r9w6go | IPTCVATH | +100,000 | $5,074,000 | $50.74 | UPTa |
| Thl98ra2pb5 | IPTCVIKI | +100,000 | $6,246,000 | $62.46 | UPTa |
| Thl98ra98dc | IPTCVOLS | +100,000 | $5,401,000 | $54.01 | UPTa |
| Thl98rafr72 | IPTCWAHU | +100,000 | $5,595,000 | $55.95 | UPTa |
| Thl98ramac0 | IPTCWAST | +100,000 | $4,085,000 | $40.85 | UPTa |
| Thl98rastfs | IPTCWKFD | +100,000 | $4,169,000 | $41.69 | UPTa |
| Thl98razc8o | IPTCWKHT | +100,000 | $5,115,000 | $51.15 | UPTa |
| Thl98rb5vch | IPTCWMIB | +100,000 | $5,076,000 | $50.76 | UPTa |
| Thl98rbce19 | IPTCWVMN | +100,000 | $4,565,000 | $45.65 | UPTa |
| Thl98rbix00 | IPTCWYCO | +100,000 | $4,186,000 | $41.86 | UPTa |
| Thl98rbpfq4 | IPTCRAVE.TEST | +100,000 | $7,746,000 | $77.46 | UPTa |
| Thl98rbvyk6 | IPTCBILL.TEST | +100,000 | $7,727,000 | $77.27 | UPTa |
| Thl98rc2hcb | IPTCCOWB.TEST | +100,000 | $6,951,000 | $69.51 | UPTa |
| Thl98rc902x | IPTCLION.TEST | +100,000 | $7,610,000 | $76.10 | UPTa |
| Thl98rcfj8m | IPTCPACK.TEST | +100,000 | $7,083,000 | $70.83 | UPTa |
| Thl98rcm22o | IPTCTEXS.TEST | +100,000 | $6,961,000 | $69.61 | UPTa |
| Thl98rcsl3o | IPTCJAGU.TEST | +100,000 | $6,324,000 | $63.24 | UPTa |
| Thl98rcz40a | IPTCCHIE.TEST | +100,000 | $7,395,000 | $73.95 | UPTa |
| Thl98rd5n4u | IPTCEAGL.TEST | +100,000 | $7,288,000 | $72.88 | UPTa |
| Thl98rdc60u | IPTCCOMM.TEST | +100,000 | $5,736,000 | $57.36 | UPTa |

**Running position per this ledger:** 100,000 of each of the 180
symbols (170 production + ten `.TEST`), account 1797733477. (Plus the
two 07-08 wash-probe fills on IPTCEAGL, +100/−100 = net 0; minus
whatever the engine has since traded — the engine's journal, not this
ledger, tracks trading.)

## 2026-08-11 — the taker-account seed, account 4963224393 (the full-book joint run)

⚠ **Different account from the rest of this ledger** — these transfers
seed the TAKER's account `4963224393`, not the MM's `1797733477`.
5,000 shares per book (SNT-1's standard float) on the 175 symbols the
taker did not already hold — its original five QA books keep their
traded positions. Basis = `Listed IPO` (`ipo-prices-170.csv`), a
`.TEST` symbol at its twin's price. **All 175 accepted** (structured
gateway log `PositionTransfer reply accepted=true` — 175/175; canary
IPTC49ER first). Submission log `~/taker-seed-log-20260811.jsonl` on
the gateway VM. First live fills under the new floats passed T-S05
reconcile at 08-11 22:47 — the seed is venue-agreed.

| ClOrdID | Symbol | txfrQty | txfrCost | Basis | Reply |
|---|---|---|---|---|---|
| Thl994w4mv7 | IPTC49ER | +5,000 | $371,350 | $74.27 | UPTa |
| Thl9961quyz | IPTCAFFC | +5,000 | $258,750 | $51.75 | UPTa |
| Thl9961xebj | IPTCAKRZ | +5,000 | $180,050 | $36.01 | UPTa |
| Thl99623xhv | IPTCAPST | +5,000 | $228,750 | $45.75 | UPTa |
| Thl9962agje | IPTCARKR | +5,000 | $228,350 | $45.67 | UPTa |
| Thl9962gzj1 | IPTCARMB | +5,000 | $281,150 | $56.23 | UPTa |
| Thl9962nifz | IPTCAUBT | +5,000 | $242,950 | $48.59 | UPTa |
| Thl9962u192 | IPTCAZSD | +5,000 | $241,650 | $48.33 | UPTa |
| Thl99630kda | IPTCAZWC | +5,000 | $256,200 | $51.24 | UPTa |
| Thl9963736s | IPTCBADG | +5,000 | $246,150 | $49.23 | UPTa |
| Thl9963dm9e | IPTCBAMA | +5,000 | $302,250 | $60.45 | UPTa |
| Thl9963k4uv | IPTCBAYB | +5,000 | $219,550 | $43.91 | UPTa |
| Thl9963qnpe | IPTCBCEA | +5,000 | $138,250 | $27.65 | UPTa |
| Thl9963x6jw | IPTCBEAR | +5,000 | $337,650 | $67.53 | UPTa |
| Thl99643pek | IPTCBENG | +5,000 | $358,800 | $71.76 | UPTa |
| Thl9964a899 | IPTCBGFL | +5,000 | $194,600 | $38.92 | UPTa |
| Thl9964grb4 | IPTCBILL | +5,000 | $386,350 | $77.27 | UPTa |
| Thl9964naix | IPTCBLSC | +5,000 | $153,850 | $30.77 | UPTa |
| Thl9964ttsy | IPTCBOIL | +5,000 | $140,400 | $28.08 | UPTa |
| Thl99650cmf | IPTCBRON | +5,000 | $348,050 | $69.61 | UPTa |
| Thl99656vg9 | IPTCBROW | +5,000 | $233,650 | $46.73 | UPTa |
| Thl9965de7r | IPTCBSST | +5,000 | $284,950 | $56.99 | UPTa |
| Thl9965jx96 | IPTCBUCC | +5,000 | $303,550 | $60.71 | UPTa |
| Thl9965qg17 | IPTCBUCK | +5,000 | $344,750 | $68.95 | UPTa |
| Thl9965wyv4 | IPTCBUFB | +5,000 | $223,200 | $44.64 | UPTa |
| Thl99663hq4 | IPTCBYUC | +5,000 | $304,500 | $60.90 | UPTa |
| Thl9966a0li | IPTCCAGB | +5,000 | $225,900 | $45.18 | UPTa |
| Thl9966gj9n | IPTCCARD | +5,000 | $178,300 | $35.66 | UPTa |
| Thl9966n2jv | IPTCCCCH | +5,000 | $193,150 | $38.63 | UPTa |
| Thl9966tlsz | IPTCCH49 | +5,000 | $106,500 | $21.30 | UPTa |
| Thl996704ld | IPTCCHAR | +5,000 | $346,300 | $69.26 | UPTa |
| Thl99676npj | IPTCCHIE | +5,000 | $369,750 | $73.95 | UPTa |
| Thl9967d6nn | IPTCCINB | +5,000 | $197,050 | $39.41 | UPTa |
| Thl9967jqf3 | IPTCCLEM | +5,000 | $284,350 | $56.87 | UPTa |
| Thl9967q9qu | IPTCCMCH | +5,000 | $233,450 | $46.69 | UPTa |
| Thl9967wugp | IPTCCOLB | +5,000 | $175,350 | $35.07 | UPTa |
| Thl99683dbn | IPTCCOLT | +5,000 | $291,200 | $58.24 | UPTa |
| Thl99689w4j | IPTCCOMM | +5,000 | $286,800 | $57.36 | UPTa |
| Thl9968gf4f | IPTCCONH | +5,000 | $208,950 | $41.79 | UPTa |
| Thl9968mxyj | IPTCCOSR | +5,000 | $160,650 | $32.13 | UPTa |
| Thl9968tgz8 | IPTCDELB | +5,000 | $224,600 | $44.92 | UPTa |
| Thl9968zzvd | IPTCDOLP | +5,000 | $191,900 | $38.38 | UPTa |
| Thl99696in3 | IPTCDUKE | +5,000 | $212,150 | $42.43 | UPTa |
| Thl9969d1tw | IPTCECAP | +5,000 | $257,150 | $51.43 | UPTa |
| Thl9969jks8 | IPTCEMEA | +5,000 | $220,550 | $44.11 | UPTa |
| Thl9969q3ru | IPTCFALC | +5,000 | $274,400 | $54.88 | UPTa |
| Thl9969wmni | IPTCFAOW | +5,000 | $220,250 | $44.05 | UPTa |
| Thl996a35i0 | IPTCFIUP | +5,000 | $227,300 | $45.46 | UPTa |
| Thl996a9odl | IPTCFLSS | +5,000 | $230,750 | $46.15 | UPTa |
| Thl996ag7mo | IPTCFRSB | +5,000 | $252,850 | $50.57 | UPTa |
| Thl996amqbl | IPTCGASP | +5,000 | $158,300 | $31.66 | UPTa |
| Thl996at9fu | IPTCGATO | +5,000 | $256,550 | $51.31 | UPTa |
| Thl996azs7a | IPTCGOPH | +5,000 | $224,700 | $44.94 | UPTa |
| Thl996b6bej | IPTCGSEA | +5,000 | $193,200 | $38.64 | UPTa |
| Thl996bcujh | IPTCGTYJ | +5,000 | $235,300 | $47.06 | UPTa |
| Thl996bjdbj | IPTCHAWA | +5,000 | $265,100 | $53.02 | UPTa |
| Thl996bpwhg | IPTCHFRG | +5,000 | $249,500 | $49.90 | UPTa |
| Thl996bwfqb | IPTCHOOS | +5,000 | $341,100 | $68.22 | UPTa |
| Thl996c2ynv | IPTCHOUC | +5,000 | $278,750 | $55.75 | UPTa |
| Thl996c9hhc | IPTCHUSK | +5,000 | $233,500 | $46.70 | UPTa |
| Thl996cg0kl | IPTCIACL | +5,000 | $190,700 | $38.14 | UPTa |
| Thl996cmob4 | IPTCIAHW | +5,000 | $274,900 | $54.98 | UPTa |
| Thl996ct7f8 | IPTCILLI | +5,000 | $249,000 | $49.80 | UPTa |
| Thl996czq9x | IPTCJAGU | +5,000 | $316,200 | $63.24 | UPTa |
| Thl996d690c | IPTCJETS | +5,000 | $229,050 | $45.81 | UPTa |
| Thl996dcs1e | IPTCJKSC | +5,000 | $261,550 | $52.31 | UPTa |
| Thl996djav6 | IPTCJMDU | +5,000 | $302,100 | $60.42 | UPTa |
| Thl996dptqz | IPTCKSGF | +5,000 | $146,200 | $29.24 | UPTa |
| Thl996dwck4 | IPTCKSJH | +5,000 | $222,500 | $44.50 | UPTa |
| Thl996e2voc | IPTCKSOW | +5,000 | $226,450 | $45.29 | UPTa |
| Thl996e9ewv | IPTCKSWC | +5,000 | $289,650 | $57.93 | UPTa |
| Thl996efxrf | IPTCKYWC | +5,000 | $191,550 | $38.31 | UPTa |
| Thl996emgsy | IPTCLARC | +5,000 | $258,150 | $51.63 | UPTa |
| Thl996eszwp | IPTCLATB | +5,000 | $222,950 | $44.59 | UPTa |
| Thl996ezj4j | IPTCLIBF | +5,000 | $290,200 | $58.04 | UPTa |
| Thl996f61xy | IPTCLION | +5,000 | $380,500 | $76.10 | UPTa |
| Thl996fckv7 | IPTCLOUC | +5,000 | $284,300 | $56.86 | UPTa |
| Thl996fj3x5 | IPTCLSUT | +5,000 | $297,700 | $59.54 | UPTa |
| Thl996fpmu6 | IPTCMEMT | +5,000 | $268,850 | $53.77 | UPTa |
| Thl996fw62n | IPTCMIHU | +5,000 | $357,850 | $71.57 | UPTa |
| Thl996g2pb3 | IPTCMIOH | +5,000 | $260,850 | $52.17 | UPTa |
| Thl996g98hz | IPTCMISP | +5,000 | $175,200 | $35.04 | UPTa |
| Thl996gfrsl | IPTCMIWV | +5,000 | $286,300 | $57.26 | UPTa |
| Thl996gmanp | IPTCMIZO | +5,000 | $240,650 | $48.13 | UPTa |
| Thl996gstnr | IPTCMOST | +5,000 | $164,250 | $32.85 | UPTa |
| Thl996gzcdw | IPTCMRSH | +5,000 | $262,100 | $52.42 | UPTa |
| Thl996h5vef | IPTCMSST | +5,000 | $178,950 | $35.79 | UPTa |
| Thl996hceni | IPTCMTBR | +5,000 | $165,100 | $33.02 | UPTa |
| Thl996hixok | IPTCNAVY | +5,000 | $291,100 | $58.22 | UPTa |
| Thl996hpgyz | IPTCNCTH | +5,000 | $194,950 | $38.99 | UPTa |
| Thl996hw097 | IPTCNCWP | +5,000 | $262,500 | $52.50 | UPTa |
| Thl996i2j2b | IPTCNDFI | +5,000 | $363,750 | $72.75 | UPTa |
| Thl996i91y7 | IPTCNDSU | +5,000 | $353,150 | $70.63 | UPTa |
| Thl996ifkjo | IPTCNEVW | +5,000 | $172,150 | $34.43 | UPTa |
| Thl996im3b9 | IPTCNIHU | +5,000 | $149,000 | $29.80 | UPTa |
| Thl996ism0w | IPTCNMLB | +5,000 | $284,000 | $56.80 | UPTa |
| Thl996iz4ug | IPTCNMSA | +5,000 | $176,400 | $35.28 | UPTa |
| Thl996j5nho | IPTCNTMG | +5,000 | $214,850 | $42.97 | UPTa |
| Thl996jc5xc | IPTCNWWC | +5,000 | $200,600 | $40.12 | UPTa |
| Thl996jiovm | IPTCODMO | +5,000 | $267,850 | $53.57 | UPTa |
| Thl996jp7o7 | IPTCOHBO | +5,000 | $252,000 | $50.40 | UPTa |
| Thl996jvqel | IPTCOKST | +5,000 | $227,400 | $45.48 | UPTa |
| Thl996k29ab | IPTCOLMR | +5,000 | $281,250 | $56.25 | UPTa |
| Thl996k8sf7 | IPTCORDU | +5,000 | $343,100 | $68.62 | UPTa |
| Thl996kfb6v | IPTCORST | +5,000 | $166,850 | $33.37 | UPTa |
| Thl996kltul | IPTCPACK | +5,000 | $354,150 | $70.83 | UPTa |
| Thl996kschd | IPTCPANT | +5,000 | $272,650 | $54.53 | UPTa |
| Thl996kyvj8 | IPTCPITT | +5,000 | $274,750 | $54.95 | UPTa |
| Thl996l5e9i | IPTCPSNL | +5,000 | $312,550 | $62.51 | UPTa |
| Thl996lbx1c | IPTCRAID | +5,000 | $245,650 | $49.13 | UPTa |
| Thl996lig8d | IPTCRAMS | +5,000 | $406,000 | $81.20 | UPTa |
| Thl996loz24 | IPTCRAVE | +5,000 | $387,300 | $77.46 | UPTa |
| Thl996lvi3d | IPTCRAZR | +5,000 | $168,600 | $33.72 | UPTa |
| Thl996m20ki | IPTCRICE | +5,000 | $148,250 | $29.65 | UPTa |
| Thl996m8jan | IPTCRUTG | +5,000 | $187,650 | $37.53 | UPTa |
| Thl996mf29o | IPTCSACS | +5,000 | $249,700 | $49.94 | UPTa |
| Thl996mlkzr | IPTCSAIN | +5,000 | $292,900 | $58.58 | UPTa |
| Thl996ms3qo | IPTCSALJ | +5,000 | $219,850 | $43.97 | UPTa |
| Thl996mymoo | IPTCSCGC | +5,000 | $228,550 | $45.71 | UPTa |
| Thl996n55q1 | IPTCSDAZ | +5,000 | $246,700 | $49.34 | UPTa |
| Thl996nbolk | IPTCSEHW | +5,000 | $375,250 | $75.05 | UPTa |
| Thl996ni79j | IPTCSHBK | +5,000 | $138,650 | $27.73 | UPTa |
| Thl996noqea | IPTCSJSP | +5,000 | $192,400 | $38.48 | UPTa |
| Thl996nv98m | IPTCSMGE | +5,000 | $157,800 | $31.56 | UPTa |
| Thl996o1s2l | IPTCSMUM | +5,000 | $300,950 | $60.19 | UPTa |
| Thl996o8b38 | IPTCSOON | +5,000 | $278,500 | $55.70 | UPTa |
| Thl996oetye | IPTCSTAN | +5,000 | $158,250 | $31.65 | UPTa |
| Thl996olcsd | IPTCSYRO | +5,000 | $181,750 | $36.35 | UPTa |
| Thl996orvq9 | IPTCTEMP | +5,000 | $202,750 | $40.55 | UPTa |
| Thl996oyeh0 | IPTCTERP | +5,000 | $198,850 | $39.77 | UPTa |
| Thl996p4xib | IPTCTEXS | +5,000 | $348,050 | $69.61 | UPTa |
| Thl996pbh09 | IPTCTITA | +5,000 | $250,800 | $50.16 | UPTa |
| Thl996pi02b | IPTCTOLR | +5,000 | $274,850 | $54.97 | UPTa |
| Thl996poivl | IPTCTROY | +5,000 | $249,600 | $49.92 | UPTa |
| Thl996pv1vs | IPTCTULN | +5,000 | $259,200 | $51.84 | UPTa |
| Thl996q1l35 | IPTCTULS | +5,000 | $204,350 | $40.87 | UPTa |
| Thl996q83zg | IPTCTXAM | +5,000 | $290,950 | $58.19 | UPTa |
| Thl996qemsq | IPTCTXLH | +5,000 | $319,050 | $63.81 | UPTa |
| Thl996ql5yn | IPTCTXSB | +5,000 | $222,350 | $44.47 | UPTa |
| Thl996qrox1 | IPTCTXTR | +5,000 | $370,500 | $74.10 | UPTa |
| Thl996qy7rh | IPTCUABB | +5,000 | $149,900 | $29.98 | UPTa |
| Thl996r4qul | IPTCUCFK | +5,000 | $221,950 | $44.39 | UPTa |
| Thl996rb9n3 | IPTCUCLA | +5,000 | $230,000 | $46.00 | UPTa |
| Thl996rhsih | IPTCUGAG | +5,000 | $343,700 | $68.74 | UPTa |
| Thl996robly | IPTCULMW | +5,000 | $150,200 | $30.04 | UPTa |
| Thl996ruujs | IPTCUMAM | +5,000 | $130,000 | $26.00 | UPTa |
| Thl996s1dg7 | IPTCUNLV | +5,000 | $286,800 | $57.36 | UPTa |
| Thl996s7wc1 | IPTCUSCJ | +5,000 | $288,500 | $57.70 | UPTa |
| Thl996sefdv | IPTCUSFB | +5,000 | $286,950 | $57.39 | UPTa |
| Thl996sky9p | IPTCUTEP | +5,000 | $139,750 | $27.95 | UPTa |
| Thl996srh51 | IPTCUTES | +5,000 | $300,550 | $60.11 | UPTa |
| Thl996sy0f1 | IPTCUTRN | +5,000 | $268,900 | $53.78 | UPTa |
| Thl996t4jdx | IPTCUTST | +5,000 | $190,350 | $38.07 | UPTa |
| Thl996tb28b | IPTCVACV | +5,000 | $274,400 | $54.88 | UPTa |
| Thl996thleq | IPTCVAND | +5,000 | $210,550 | $42.11 | UPTa |
| Thl996to4ou | IPTCVATH | +5,000 | $253,700 | $50.74 | UPTa |
| Thl996tunol | IPTCVIKI | +5,000 | $312,300 | $62.46 | UPTa |
| Thl996u16y0 | IPTCVOLS | +5,000 | $270,050 | $54.01 | UPTa |
| Thl996u7q67 | IPTCWAHU | +5,000 | $279,750 | $55.95 | UPTa |
| Thl996ue9l8 | IPTCWAST | +5,000 | $204,250 | $40.85 | UPTa |
| Thl996uksf0 | IPTCWKFD | +5,000 | $208,450 | $41.69 | UPTa |
| Thl996urbl4 | IPTCWKHT | +5,000 | $255,750 | $51.15 | UPTa |
| Thl996uxuof | IPTCWMIB | +5,000 | $253,800 | $50.76 | UPTa |
| Thl996v4dd9 | IPTCWVMN | +5,000 | $228,250 | $45.65 | UPTa |
| Thl996vawiq | IPTCWYCO | +5,000 | $209,300 | $41.86 | UPTa |
| Thl996vhfno | IPTCRAVE.TEST | +5,000 | $387,300 | $77.46 | UPTa |
| Thl996vnywi | IPTCBILL.TEST | +5,000 | $386,350 | $77.27 | UPTa |
| Thl996vuhte | IPTCCOWB.TEST | +5,000 | $347,550 | $69.51 | UPTa |
| Thl996w10oo | IPTCLION.TEST | +5,000 | $380,500 | $76.10 | UPTa |
| Thl996w7jrl | IPTCPACK.TEST | +5,000 | $354,150 | $70.83 | UPTa |
| Thl996we2r2 | IPTCTEXS.TEST | +5,000 | $348,050 | $69.61 | UPTa |
| Thl996wklij | IPTCJAGU.TEST | +5,000 | $316,200 | $63.24 | UPTa |
| Thl996wr4fk | IPTCCHIE.TEST | +5,000 | $369,750 | $73.95 | UPTa |
| Thl996wxnk9 | IPTCEAGL.TEST | +5,000 | $364,400 | $72.88 | UPTa |
| Thl996x46hn | IPTCCOMM.TEST | +5,000 | $286,800 | $57.36 | UPTa |

**Running position, account 4963224393, per this ledger + journals:**
5,000 of each of the 175 seeded symbols; the five QA books carry their
traded state (journal `snt5` from floats COWB 3856 · EAGL 5406 ·
GIAN 4605 · PATR 5245 · STEE 5419 at the 08-11 22:43 cutover).

## 2026-08-19/20 — the full IPO seed + offering (George's direction; run by Claude)

Session: [[market-maker/sessions/2026-08-19-c-ipo-test-rig]] · runbook
[[market-maker/reference/ipo-seeding-runbook]]

⚠ **`txfrCost` in this run is a PRICE PER SHARE, not a total** — the unit was
settled by measurement on 19-08 and the earlier entries in this ledger use the
other reading. See the runbook §2.

**Read first.** Every one of the 170 books already held 79,000–108,000 shares
(17,820,524 in total), so each transfer is `float − held`, never the float.
Pre-seed positions: `/tmp/ipo/positions.json` on the gateway VM ⚠ (`/tmp` — not
durable).

| Batch | Books | Shares transferred | Ledger |
|---|---|---|---|
| Eagles, by hand (the proving run) | 1 | +840,298 @ 72.88 | — |
| The other 169 | 169 | +148,979,476 | `/tmp/ipo/seed-ledger.jsonl` |
| Top-ups after trading (AFFC/RAVE/HOOS/MISP) | 4 | +195,550 | — |
| The ten `.TEST` twins | 10 | +8,000,000 (to 900,000 each) | — |

**Result:** all 170 real books at float — 900,000 NFL · 1,000,000 NCAA,
166,800,000 shares — verified 170/170 by the asks' own `9383`. The ten twins at
900,000 each.

### UEPR entries (this ledger's first — the message was believed disabled)

| Account | Symbol | Qto | Why |
|---|---|---|---|
| 1797733477 | IPTCJAGU.TEST | 99,657 | ⚠ **repair** — a `Qto=0` "no-op" probe at 16:24:35Z zeroed the opening balance and destroyed **99,663 shares**. Restored to 101,665 |
| 4963224393 | IPTCAFFC | −42,225 | back to 7,887, undoing the Buy-ticket test |
| 4963224393 | IPTCRAVE | −41,320 | back to 3,855, same |

⚠ Both taker resets booked a **realized P&L artefact** — AFFC +$7,146.39, RAVE
+$11,074.87. Reducing a position always marks a P&L; a position can be reset, a
trade cannot be un-traded.

## 2026-08-26 — the TEST maker seed, account 2559580864 (George's direction; run by Claude)

⚠ **Different account from the rest of this ledger** — the **test
maker** `2559580864` (Hasan, 26-08), not the MM's `1797733477`. All
**170 `.TEST` twins**, 100,000 shares each, `txfrCost` = the base
ticker's vault v1.0 IPO price **per share** ("bought at the IPO price",
George). Read-first skipped on George's ruling: the account was created
this week and had never held anything. Canary `IPTCRAVE.TEST` first
(20:05:24Z, UPTa in 9 ms), then the other 169 at 2/s (20:06–20:07Z).
**170/170 `UPTa`, 0 `UPTx`, 0 unanswered**, every reply matched on
account, symbol and `9386=100000` against the intent ledger. Sent via
`inplay-fix-gateway` FHINPLAY01. Intent ledger:
`~/ipo-ledgers/test-seed-2559580864.jsonl` on the gateway VM (home dir,
not `/tmp`). Notional at basis ≈ $852,013,000.

| ClOrdID | Symbol | txfrQty | txfrCost (per share) | Reply |
|---|---|---|---|---|
| Thlpodnjucy | IPTC49ER.TEST | +100,000 | $74.27 | UPTa |
| Thlpodnuno2 | IPTCAFFC.TEST | +100,000 | $51.75 | UPTa |
| Thlpodo5h0a | IPTCAKRZ.TEST | +100,000 | $36.01 | UPTa |
| Thlpodogah9 | IPTCAPST.TEST | +100,000 | $45.75 | UPTa |
| Thlpodor3xw | IPTCARKR.TEST | +100,000 | $45.67 | UPTa |
| Thlpodp1xl1 | IPTCARMB.TEST | +100,000 | $56.23 | UPTa |
| Thlpodpcqvp | IPTCAUBT.TEST | +100,000 | $48.59 | UPTa |
| Thlpodpnkga | IPTCAZSD.TEST | +100,000 | $48.33 | UPTa |
| Thlpodpydvf | IPTCAZWC.TEST | +100,000 | $51.24 | UPTa |
| Thlpodq97db | IPTCBADG.TEST | +100,000 | $49.23 | UPTa |
| Thlpodqk14b | IPTCBAMA.TEST | +100,000 | $60.45 | UPTa |
| Thlpodquu70 | IPTCBAYB.TEST | +100,000 | $43.91 | UPTa |
| Thlpodr5nfj | IPTCBCEA.TEST | +100,000 | $27.65 | UPTa |
| Thlpodrggwm | IPTCBEAR.TEST | +100,000 | $67.53 | UPTa |
| Thlpodrrajw | IPTCBENG.TEST | +100,000 | $71.76 | UPTa |
| Thlpods2419 | IPTCBGFL.TEST | +100,000 | $38.92 | UPTa |
| Thlpodscx8p | IPTCBILL.TEST | +100,000 | $77.27 | UPTa |
| Thlpodsnqeh | IPTCBLSC.TEST | +100,000 | $30.77 | UPTa |
| Thlpodsyjov | IPTCBOIL.TEST | +100,000 | $28.08 | UPTa |
| Thlpodt9der | IPTCBRON.TEST | +100,000 | $69.61 | UPTa |
| Thlpodtk6ws | IPTCBROW.TEST | +100,000 | $46.73 | UPTa |
| Thlpodtv0gz | IPTCBSST.TEST | +100,000 | $56.99 | UPTa |
| Thlpodu5tvg | IPTCBUCC.TEST | +100,000 | $60.71 | UPTa |
| Thlpodugnd4 | IPTCBUCK.TEST | +100,000 | $68.95 | UPTa |
| Thlpodurh3z | IPTCBUFB.TEST | +100,000 | $44.64 | UPTa |
| Thlpodv2akb | IPTCBYUC.TEST | +100,000 | $60.90 | UPTa |
| Thlpodvd3rt | IPTCCAGB.TEST | +100,000 | $45.18 | UPTa |
| Thlpodvnxr2 | IPTCCARD.TEST | +100,000 | $35.66 | UPTa |
| Thlpodvyr7d | IPTCCCCH.TEST | +100,000 | $38.63 | UPTa |
| Thlpodw9kiv | IPTCCH49.TEST | +100,000 | $21.30 | UPTa |
| Thlpodwkdp5 | IPTCCHAR.TEST | +100,000 | $69.26 | UPTa |
| Thlpodwv6w9 | IPTCCHIE.TEST | +100,000 | $73.95 | UPTa |
| Thlpodx60il | IPTCCINB.TEST | +100,000 | $39.41 | UPTa |
| Thlpodxgu43 | IPTCCLEM.TEST | +100,000 | $56.87 | UPTa |
| Thlpodxrno3 | IPTCCMCH.TEST | +100,000 | $46.69 | UPTa |
| Thlpody2h75 | IPTCCOLB.TEST | +100,000 | $35.07 | UPTa |
| Thlpodydah4 | IPTCCOLT.TEST | +100,000 | $58.24 | UPTa |
| Thlpodyo4cq | IPTCCOMM.TEST | +100,000 | $57.36 | UPTa |
| Thlpodyyxvr | IPTCCONH.TEST | +100,000 | $41.79 | UPTa |
| Thlpodz9rby | IPTCCOSR.TEST | +100,000 | $32.13 | UPTa |
| Thlpodzkl02 | IPTCCOWB.TEST | +100,000 | $69.51 | UPTa |
| Thlpodzveh4 | IPTCDELB.TEST | +100,000 | $44.92 | UPTa |
| Thlpoe067v0 | IPTCDOLP.TEST | +100,000 | $38.38 | UPTa |
| Thlpoe0h13o | IPTCDUKE.TEST | +100,000 | $42.43 | UPTa |
| Thlpoe0rul0 | IPTCEAGL.TEST | +100,000 | $72.88 | UPTa |
| Thlpoe12ntt | IPTCECAP.TEST | +100,000 | $51.43 | UPTa |
| Thlpoe1dhbi | IPTCEMEA.TEST | +100,000 | $44.11 | UPTa |
| Thlpoe1oat1 | IPTCFALC.TEST | +100,000 | $54.88 | UPTa |
| Thlpoe1z496 | IPTCFAOW.TEST | +100,000 | $44.05 | UPTa |
| Thlpoe29xqr | IPTCFIUP.TEST | +100,000 | $45.46 | UPTa |
| Thlpoe2kr86 | IPTCFLSS.TEST | +100,000 | $46.15 | UPTa |
| Thlpoe2vki6 | IPTCFRSB.TEST | +100,000 | $50.57 | UPTa |
| Thlpoe36dxw | IPTCGASP.TEST | +100,000 | $31.66 | UPTa |
| Thlpoe3h7ep | IPTCGATO.TEST | +100,000 | $51.31 | UPTa |
| Thlpoe3s0vv | IPTCGIAN.TEST | +100,000 | $57.58 | UPTa |
| Thlpoe42uc2 | IPTCGOPH.TEST | +100,000 | $44.94 | UPTa |
| Thlpoe4dnpk | IPTCGSEA.TEST | +100,000 | $38.64 | UPTa |
| Thlpoe4ogwc | IPTCGTYJ.TEST | +100,000 | $47.06 | UPTa |
| Thlpoe4zah9 | IPTCHAWA.TEST | +100,000 | $53.02 | UPTa |
| Thlpoe5a4a3 | IPTCHFRG.TEST | +100,000 | $49.90 | UPTa |
| Thlpoe5kxbg | IPTCHOOS.TEST | +100,000 | $68.22 | UPTa |
| Thlpoe5vqqe | IPTCHOUC.TEST | +100,000 | $55.75 | UPTa |
| Thlpoe66k9q | IPTCHUSK.TEST | +100,000 | $46.70 | UPTa |
| Thlpoe6hdkr | IPTCIACL.TEST | +100,000 | $38.14 | UPTa |
| Thlpoe6s74r | IPTCIAHW.TEST | +100,000 | $54.98 | UPTa |
| Thlpoe730ex | IPTCILLI.TEST | +100,000 | $49.80 | UPTa |
| Thlpoe7dtvg | IPTCJAGU.TEST | +100,000 | $63.24 | UPTa |
| Thlpoe7omzl | IPTCJETS.TEST | +100,000 | $45.81 | UPTa |
| Thlpoe7zghv | IPTCJKSC.TEST | +100,000 | $52.31 | UPTa |
| Thlpoe8aa0j | IPTCJMDU.TEST | +100,000 | $60.42 | UPTa |
| Thlpoe8l3m3 | IPTCKSGF.TEST | +100,000 | $29.24 | UPTa |
| Thlpoe8vwy1 | IPTCKSJH.TEST | +100,000 | $44.50 | UPTa |
| Thlpoe96qi3 | IPTCKSOW.TEST | +100,000 | $45.29 | UPTa |
| Thlpoe9hjny | IPTCKSWC.TEST | +100,000 | $57.93 | UPTa |
| Thlpoe9sd1f | IPTCKYWC.TEST | +100,000 | $38.31 | UPTa |
| Thlpoea36no | IPTCLARC.TEST | +100,000 | $51.63 | UPTa |
| Thlpoeae0er | IPTCLATB.TEST | +100,000 | $44.59 | UPTa |
| Thlpoeaotx4 | IPTCLIBF.TEST | +100,000 | $58.04 | UPTa |
| Thlpoeazmy4 | IPTCLION.TEST | +100,000 | $76.10 | UPTa |
| Thlpoebagj9 | IPTCLOUC.TEST | +100,000 | $56.86 | UPTa |
| Thlpoebl9wr | IPTCLSUT.TEST | +100,000 | $59.54 | UPTa |
| Thlpoebw3lf | IPTCMEMT.TEST | +100,000 | $53.77 | UPTa |
| Thlpoec6x2h | IPTCMIHU.TEST | +100,000 | $71.57 | UPTa |
| Thlpoechqph | IPTCMIOH.TEST | +100,000 | $52.17 | UPTa |
| Thlpoecsk5b | IPTCMISP.TEST | +100,000 | $35.04 | UPTa |
| Thlpoed3d9a | IPTCMIWV.TEST | +100,000 | $57.26 | UPTa |
| Thlpoede6p1 | IPTCMIZO.TEST | +100,000 | $48.13 | UPTa |
| Thlpoedp08l | IPTCMOST.TEST | +100,000 | $32.85 | UPTa |
| Thlpoedztmj | IPTCMRSH.TEST | +100,000 | $52.42 | UPTa |
| Thlpoeeamvz | IPTCMSST.TEST | +100,000 | $35.79 | UPTa |
| Thlpoeelgau | IPTCMTBR.TEST | +100,000 | $33.02 | UPTa |
| Thlpoeew9j0 | IPTCNAVY.TEST | +100,000 | $58.22 | UPTa |
| Thlpoef72oe | IPTCNCTH.TEST | +100,000 | $38.99 | UPTa |
| Thlpoefhvx2 | IPTCNCWP.TEST | +100,000 | $52.50 | UPTa |
| Thlpoefsp2s | IPTCNDFI.TEST | +100,000 | $72.75 | UPTa |
| Thlpoeg3ice | IPTCNDSU.TEST | +100,000 | $70.63 | UPTa |
| Thlpoegebjc | IPTCNEVW.TEST | +100,000 | $34.43 | UPTa |
| Thlpoegp4n8 | IPTCNIHU.TEST | +100,000 | $29.80 | UPTa |
| Thlpoegzxs4 | IPTCNMLB.TEST | +100,000 | $56.80 | UPTa |
| Thlpoehar5a | IPTCNMSA.TEST | +100,000 | $35.28 | UPTa |
| Thlpoehlknz | IPTCNTMG.TEST | +100,000 | $42.97 | UPTa |
| Thlpoehwe2q | IPTCNWWC.TEST | +100,000 | $40.12 | UPTa |
| Thlpoei77sv | IPTCODMO.TEST | +100,000 | $53.57 | UPTa |
| Thlpoeii175 | IPTCOHBO.TEST | +100,000 | $50.40 | UPTa |
| Thlpoeisukf | IPTCOKST.TEST | +100,000 | $45.48 | UPTa |
| Thlpoej3nwr | IPTCOLMR.TEST | +100,000 | $56.25 | UPTa |
| Thlpoejeh6s | IPTCORDU.TEST | +100,000 | $68.62 | UPTa |
| Thlpoejpans | IPTCORST.TEST | +100,000 | $33.37 | UPTa |
| Thlpoek044o | IPTCPACK.TEST | +100,000 | $70.83 | UPTa |
| Thlpoekaxdr | IPTCPANT.TEST | +100,000 | $54.53 | UPTa |
| Thlpoeklqou | IPTCPATR.TEST | +100,000 | $72.25 | UPTa |
| Thlpoekwjyu | IPTCPITT.TEST | +100,000 | $54.95 | UPTa |
| Thlpoel7ddt | IPTCPSNL.TEST | +100,000 | $62.51 | UPTa |
| Thlpoeli72d | IPTCRAID.TEST | +100,000 | $49.13 | UPTa |
| Thlpoelt12g | IPTCRAMS.TEST | +100,000 | $81.20 | UPTa |
| Thlpodbwna3 | IPTCRAVE.TEST | +100,000 | $77.46 | UPTa |
| Thlpoem3uhl | IPTCRAZR.TEST | +100,000 | $33.72 | UPTa |
| Thlpoemenno | IPTCRICE.TEST | +100,000 | $29.65 | UPTa |
| Thlpoemph1a | IPTCRUTG.TEST | +100,000 | $37.53 | UPTa |
| Thlpoen0akl | IPTCSACS.TEST | +100,000 | $49.94 | UPTa |
| Thlpoenb45c | IPTCSAIN.TEST | +100,000 | $58.58 | UPTa |
| Thlpoenlxhv | IPTCSALJ.TEST | +100,000 | $43.97 | UPTa |
| Thlpoenwr42 | IPTCSCGC.TEST | +100,000 | $45.71 | UPTa |
| Thlpoeo7kh8 | IPTCSDAZ.TEST | +100,000 | $49.34 | UPTa |
| Thlpoeoidt9 | IPTCSEHW.TEST | +100,000 | $75.05 | UPTa |
| Thlpoeot73h | IPTCSHBK.TEST | +100,000 | $27.73 | UPTa |
| Thlpoep411e | IPTCSJSP.TEST | +100,000 | $38.48 | UPTa |
| Thlpoepeuye | IPTCSMGE.TEST | +100,000 | $31.56 | UPTa |
| Thlpoeppovu | IPTCSMUM.TEST | +100,000 | $60.19 | UPTa |
| Thlpoeq0igv | IPTCSOON.TEST | +100,000 | $55.70 | UPTa |
| Thlpoeqbbo0 | IPTCSTAN.TEST | +100,000 | $31.65 | UPTa |
| Thlpoeqm52a | IPTCSTEE.TEST | +100,000 | $62.28 | UPTa |
| Thlpoeqwyzx | IPTCSYRO.TEST | +100,000 | $36.35 | UPTa |
| Thlpoer7sc4 | IPTCTEMP.TEST | +100,000 | $40.55 | UPTa |
| Thlpoerilri | IPTCTERP.TEST | +100,000 | $39.77 | UPTa |
| Thlpoertf8b | IPTCTEXS.TEST | +100,000 | $69.61 | UPTa |
| Thlpoes48il | IPTCTITA.TEST | +100,000 | $50.16 | UPTa |
| Thlpoesf24r | IPTCTOLR.TEST | +100,000 | $54.97 | UPTa |
| Thlpoespvcz | IPTCTROY.TEST | +100,000 | $49.92 | UPTa |
| Thlpoet0oqz | IPTCTULN.TEST | +100,000 | $51.84 | UPTa |
| Thlpoetbhza | IPTCTULS.TEST | +100,000 | $40.87 | UPTa |
| Thlpoetmbap | IPTCTXAM.TEST | +100,000 | $58.19 | UPTa |
| Thlpoetx4lm | IPTCTXLH.TEST | +100,000 | $63.81 | UPTa |
| Thlpoeu7xyd | IPTCTXSB.TEST | +100,000 | $44.47 | UPTa |
| Thlpoeuirai | IPTCTXTR.TEST | +100,000 | $74.10 | UPTa |
| Thlpoeutkpt | IPTCUABB.TEST | +100,000 | $29.98 | UPTa |
| Thlpoev4e0h | IPTCUCFK.TEST | +100,000 | $44.39 | UPTa |
| Thlpoevf7d5 | IPTCUCLA.TEST | +100,000 | $46.00 | UPTa |
| Thlpoevq0ti | IPTCUGAG.TEST | +100,000 | $68.74 | UPTa |
| Thlpoew0uf6 | IPTCULMW.TEST | +100,000 | $30.04 | UPTa |
| Thlpoewbnug | IPTCUMAM.TEST | +100,000 | $26.00 | UPTa |
| Thlpoewmh7u | IPTCUNLV.TEST | +100,000 | $57.36 | UPTa |
| Thlpoewxaux | IPTCUSCJ.TEST | +100,000 | $57.70 | UPTa |
| Thlpoex84b0 | IPTCUSFB.TEST | +100,000 | $57.39 | UPTa |
| Thlpoexixk6 | IPTCUTEP.TEST | +100,000 | $27.95 | UPTa |
| Thlpoextqw4 | IPTCUTES.TEST | +100,000 | $60.11 | UPTa |
| Thlpoey4kor | IPTCUTRN.TEST | +100,000 | $53.78 | UPTa |
| Thlpoeyfe34 | IPTCUTST.TEST | +100,000 | $38.07 | UPTa |
| Thlpoeyq7pl | IPTCVACV.TEST | +100,000 | $54.88 | UPTa |
| Thlpoez11bh | IPTCVAND.TEST | +100,000 | $42.11 | UPTa |
| Thlpoezbumi | IPTCVATH.TEST | +100,000 | $50.74 | UPTa |
| Thlpoezmntj | IPTCVIKI.TEST | +100,000 | $62.46 | UPTa |
| Thlpoezxhj7 | IPTCVOLS.TEST | +100,000 | $54.01 | UPTa |
| Thlpof08awp | IPTCWAHU.TEST | +100,000 | $55.95 | UPTa |
| Thlpof0j4gj | IPTCWAST.TEST | +100,000 | $40.85 | UPTa |
| Thlpof0txkk | IPTCWKFD.TEST | +100,000 | $41.69 | UPTa |
| Thlpof14qye | IPTCWKHT.TEST | +100,000 | $51.15 | UPTa |
| Thlpof1fk1w | IPTCWMIB.TEST | +100,000 | $50.76 | UPTa |
| Thlpof1qdjc | IPTCWVMN.TEST | +100,000 | $45.65 | UPTa |
| Thlpof216nt | IPTCWYCO.TEST | +100,000 | $41.86 | UPTa |

**Running position per this ledger, account 2559580864:** 100,000 of
each of the 170 `.TEST` twins. No cash / buying power was set — bidding
needs a UEAR on this account first.
