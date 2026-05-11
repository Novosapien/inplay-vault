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
