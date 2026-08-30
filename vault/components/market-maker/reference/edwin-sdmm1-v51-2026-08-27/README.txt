SDMM-1 Reference Price — handoff package (v5.1, Aug 27 2026)

CONTENTS
  novo_engine.py       reference implementation (Python 3.10+, stdlib only)
  test_engine.py       acceptance suite — a port is correct when all 31 pass
  reference-spec.html  the specification (open in any browser)

RUN IT
  python3 novo_engine.py     -> prints the LSU t-zero calibration ($59.5350)
  python3 test_engine.py     -> runs the 31 acceptance tests (~30s)

No installs, no dependencies.
