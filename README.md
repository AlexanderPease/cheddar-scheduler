A generalizable scheduling algorithm. Takes a brute force iteration approach and then determines ideal schedule via value-weightd optimizations.

Implemented for scheduling Cheddar's on-screen talent.

## Hard requirements
- Available anchors vary each day
- Two anchors per show
- Min 1 hr blocks, except specialty
- Max 3 consecutive hrs, optimize as few as possible
- Max 4 hours per day not including hits
- 9-5pm or 9-6pm daily
- Some shows have always have specific anchors, ex. Politics show: Baker or Tim in nyc and JD in DC
- Some shows are only applicable to a subgroup of anchors
- Can’t do hit and show at same time


## Optimizations
- Fewest consecutive hours for an anchor - TO-DO: Not only true
- Shortest end to end time
- Everyone starts by 12
- TO-DO: Anchors prefer certain shows: opening bell Kristen Tim, between Nora Baker, closing Brad hope
- TO-DO: Hits w 1 hr in between full shows is hard
- TO-DO: Certain adjacent blocks containing same anchors

Other TO-DOs:
- Distinguish between anchor and hit for each block
