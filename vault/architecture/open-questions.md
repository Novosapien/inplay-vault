# Open Questions

> **Architecture:** [[architecture]]
> **Status:** Active

| Question | Impact | Who Answers | Status |
|----------|--------|-------------|--------|
| Where is tZERO's matching engine physically? | Determines FIX Gateway VM location and network link to GCP. Co-location required for <1ms latency. | tZERO / Edwin | Open |
| FIX 4.2 or FIX 4.4? PDFs say 4.2, online docs say 4.4. | Affects FIX Gateway implementation. Different message formats. | tZERO | Open |
| Does tZERO support multiple concurrent OE FIX sessions? | Could enable parallel order processing during spikes, multiplying throughput. | tZERO | Open |
| tZERO REST API full endpoint list? | Determines what non-real-time operations can bypass FIX Gateway. API explorer is JS-rendered, couldn't scrape. | tZERO (request docs) | Open |
| tZERO order throughput limit? | Determines whether order queuing causes noticeable delay during game spikes. | tZERO | Open |
| Sport Radar delivery method -- push feed or polling API? | Push = simpler, lower latency. Poll = more control but higher latency. Affects Market Data Service and event trigger engine for ads. | Sport Radar | Open |
| Which API gateway does Brett prefer / have experience with? | Shortcut the gateway selection. His operational experience is more valuable than our analysis. | Brett | Open |
| Centrifugo MIG VM sizing and connection limits per instance? | Determines VM machine type (e2-standard-4? e2-standard-8?) and min/max scaling targets. | Load testing | Open |
| tZERO sandbox access timeline? | Blocks FIX Gateway integration testing. Everything else can be built and unit tested, but end-to-end requires sandbox. | tZERO / Edwin | Open |
| App Store first submission -- how early? | Apple review can take 1-7 days and may reject. Need 2-3 weeks buffer before launch. | Planning | Open |
| **CRITICAL: What does tZERO manage for the simulated challenge?** | Determines whether InPlay needs to store trade data, positions, wallet balances, and P&L in PostgreSQL -- or if tZERO handles all of this. If tZERO manages wallets and positions, the Trading Service becomes a simple passthrough, no Fill Processor is needed, and PostgreSQL scope shrinks to just users/referrals/ads/preferences. If InPlay manages wallets, we need wallet validation on every order, a Fill Processor to update balances on every fill, and Redis caching of wallet state. This is the single biggest open question affecting architecture complexity. | tZERO / Edwin | **Open -- BLOCKING** |
| Does the Trading Service need to validate wallet balance, or does tZERO? | If tZERO validates "can this user afford this trade", Trading Service is a passthrough. If InPlay validates, Trading Service needs Redis wallet cache + PostgreSQL writes + Fill Processor. | tZERO / Edwin | Open |
| Do we need a Fill Processor service? | Only needed if InPlay stores trade data in PostgreSQL. If tZERO owns all trade state, fills just flow through NATS to Centrifugo (user notification) and Leaderboard Service (rankings). No database write needed on our side. | Depends on tZERO answer above | Open |
