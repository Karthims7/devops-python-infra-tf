# Live Coding Topic: Log Stream & Percentile Analyzer

## What the Interviewer Is Really Testing
1. **Handling Streaming Data:** Avoiding `file.readlines()` which loads everything into memory. Instead, accepting an `Iterator[str]` or generator so that 50GB log files can be processed in constant memory.
2. **Robust Parsing:** Using compiled regular expressions with named capture groups (`(?P<name>...)`) or structured string splitting.
3. **Statistical Mastery:** Knowing how P50, P90, P99 are calculated.
4. **Architectural Extension (Senior Level):**
   - In memory, keeping millions of floats takes memory. Mentioning **Reservoir Sampling** or **T-Digest / HdrHistogram** for streaming fixed-memory approximation shows senior-tier systems expertise.

## Useful Formula to Mention
$$k = (N - 1) \times \frac{P}{100}$$
Where $N$ is total sample count, and $P$ is target percentile.

