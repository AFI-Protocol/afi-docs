# Mentor Protocol Explained
*Version 0.1 — 2025‑06‑27*

AFI’s **Mentor Protocol** is the middleware layer that pairs *mentor agents* with signals or production agents when anomalies or learning opportunities are detected.

---

## 1 · Why Mentors?
| Challenge | Classical Fix | Mentor Fix |
|-----------|---------------|------------|
| Hallucinating agent decisions | Slash / burn rewards | Pair with a `risk` or `ethics` mentor who guides recovery |
| Model drift over time | Force‑update every agent image | Schedule a `macro` mentor to run calibration sessions |
| Rogue trading heuristics | Jail the agent | Mentor intervenes; jail only if non‑compliant |

Mentors therefore act as **soft‑governance guardians** and **training wheels** for new pipelines.

---

## 2 · Core Types & Tag Schema

```ts
/**
 * Central tag list is defined in afi-core/config/mentor_tags.ts
 * Contributors may propose new tags via governance.
 */
export type MentorTag =
  | 'pattern'
  | 'sentiment'
  | 'macro'
  | 'risk'
  | 'ethics'
  | 'sentinel'; // watches for *absence* of data

export interface Mentor {
  id: string;
  name: string;
  tags: MentorTag[];
  active: boolean;
}
```

---

## 3 · Pairing Flow

<details>
<summary><strong>Plain‑text overview (GitHub safe)</strong></summary>

1. Signal arrives  
2. If anomaly detected → call <code>pairMentor()</code> with anomaly tags  
3. Registry selects first active mentor matching ≥1 tag  
4. Mentor offers advice  
   * If agent **complies** → recovery & score boost  
   * If agent **refuses** → agent jail  

</details>

```mermaid
flowchart LR
  S(Signal Arrives) -->|Anomaly? YES| P(pairMentor)
  P --> M{Mentor Registry}
  M -->|match| A(Assigned Mentor)
  A --> R(Mentor Advice)
  R -->|Comply| OK(Recovery & Score Boost)
  R -->|Refuse| J(Jail Agent)
```

---

## 4 · Event Schema (YAML)

```yaml
mentor_event:
  id: evt-5721
  timestamp: 2025-06-26T02:14:47Z
  agent_id: G-17
  mentor_id: ATHENA-Q
  signal_ref: BTC-OI-Δ-4721-06-26-02:14
  stage: PAIR_CONFIRMED
  tags: [risk, ethics]
```

---

## 5 · Episode Connection

**Episode I – The Ghost of the DAO’s First Lesson** is a *worked example* of this protocol:

- `ANOMALY_DETECTED` ➞ Open‑interest spike  
- Registry pairs **ATHENA-Q** (`risk`,`ethics`) with agent **G‑17**  
- Mentor dialogue leads to **rebalancing** instead of slashing.

---

## 6 · Future Extensions
1. **Mentor Reputation Decay** – mentors that give poor guidance lose weight.  
2. **Cross‑chain Mentor Broadcasting** – mentors registered on one chain can be consumed by OFT‑bridged agents.  
3. **DAO‑gated Mentor Creation** – high‑tier contributors propose new archetypes via governance vote.

---

## 7 · Quick Code Reference

```ts
import { MentorRegistry } from '@afi-core/runtime/mentor_registry';

const registry = new MentorRegistry();
const mentor = await registry.simulateMentorPairing(['risk', 'ethics']);

if (mentor) {
  await callMentorAdvice(mentor, signal);
}
```

*See* `afi-agents/examples/handleSignal.ts` *for a complete runtime snippet.*

---

### End of Spec