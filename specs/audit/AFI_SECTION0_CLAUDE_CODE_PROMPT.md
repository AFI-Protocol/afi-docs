# Claude Code Workflow — Section 0 Pre-flight (T1 Gate)

**Target:** [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) §0 + §0.1  
**Repo:** `/home/user/AFI-Protocol/afi-token` (Foundry)  
**Chain:** Base Sepolia (`84532`)  
**Mode:** Ultracode xhigh + workflows — sequential gates, no skip on failure

---

## Copy-paste prompt (start here)

```
# MISSION: AFI Testnet Section 0 Pre-flight (T1 Gate)

You are executing Section 0 of the AFI Base Sepolia Testnet E2E checklist.
Work ONLY in afi-token unless a read-only check in afi-docs is needed for addresses.

## Hard rules
1. NEVER commit, print, or log private keys. Read from .env only.
2. NEVER run mainnet commands or change foundry.toml chain defaults to mainnet.
3. If a human-only step blocks progress, STOP and output a clear HANDOFF block — do not guess.
4. Every checklist row must end PASS, FAIL, or HUMAN_REQUIRED with evidence (command output or tx hash).
5. Do not proceed to Section 1. This mission ends at T1 gate only.
6. If sanity script passes but coordinator/emissions-agent roles fail, run the supplemental cast checks below — the stock sanity script is incomplete.

## Human prerequisites (assume user completed BEFORE you start)
The user must have already:
- [ ] Created `afi-token/.env` from `.env.example` with real values (not committed)
- [ ] Set `BASE_SEPOLIA_RPC_URL`
- [ ] Set `PRIVATE_KEY_TESTNET` for an address that will act as **emissions agent** OR documented which key signs mints
- [ ] Funded emissions agent with ≥ 0.01 Sepolia ETH on Base Sepolia
- [ ] Chosen **test beneficiary** address (any funded or unfunded EOA is OK for mint test)
- [ ] If Treasury Safe is admin (not deployer): signed Safe txs to wire coordinator roles OR confirmed deployer still has coordinator EMISSIONS_ROLE

If `.env` is missing or empty placeholders remain, output HANDOFF: "User must complete .env" and stop.

## Canonical deployed addresses (verify first; redeploy only if missing on-chain)
AFITOKEN=0x43DC488caF49495d6abC0eEe021B725be38E81bd
RECEIPTS=0xD1aDC1Ca4A98B141D8f3a4fE2cb9638003E70e23
COORDINATOR=0xDd825a05EFe22668Ffbd627C586f19D08d62eA5e
TREASURY_SAFE=0x1Dd6705ff84Ecd5eaDc51A913Ad8e2c6C9E79aC4
DEPLOYER_EOA=0x732588589F72DDb67F9022E59Ab3f8cFB16455b6

## Workflow (execute in order)

### Gate 0 — Tooling
- cd /home/user/AFI-Protocol/afi-token
- Verify: `forge --version`, `cast --version`
- Verify: `test -f .env` and `BASE_SEPOLIA_RPC_URL` is non-empty (grep without printing secrets)
- Verify chain: `cast chain-id --rpc-url $BASE_SEPOLIA_RPC_URL` → must be 84532

### Gate 1 — Contracts exist on-chain
For each address, `cast code $ADDR --rpc-url $BASE_SEPOLIA_RPC_URL` must return non-empty bytecode.
If any address has no code: HANDOFF redeploy instructions OR run dry-run first:
  `forge script script/DeployAFITestnet.s.sol --rpc-url base_sepolia`
Only broadcast redeploy if user explicitly authorized in session; otherwise HUMAN_REQUIRED.

### Gate 2 — Run stock sanity script
`set -a && source .env && set +a && bash script/afitoken_testnet_sanity_checks.sh`
Capture full output. Expected: name tAFI, cap 86B, coordinator token/receipts addresses match.

### Gate 3 — Supplemental role checks (sanity script gaps)
The checklist requires checks the sanity script does NOT fully cover. Run all:

EMISSIONS_ROLE=$(cast keccak "EMISSIONS_ROLE")
MINT_COORDINATOR_ROLE=$(cast keccak "MINT_COORDINATOR_ROLE")

# Coordinator has EMISSIONS_ROLE on AFIToken (coordinator must mint via token)
cast call $AFITOKEN "hasRole(bytes32,address)(bool)" $EMISSIONS_ROLE $COORDINATOR --rpc-url $BASE_SEPOLIA_RPC_URL

# Coordinator has MINT_COORDINATOR_ROLE on receipts
cast call $RECEIPTS "hasRole(bytes32,address)(bool)" $MINT_COORDINATOR_ROLE $COORDINATOR --rpc-url $BASE_SEPOLIA_RPC_URL

# Emissions agent = address derived from PRIVATE_KEY_TESTNET
EMISSIONS_AGENT=$(cast wallet address --private-key $PRIVATE_KEY_TESTNET)
cast call $COORDINATOR "hasRole(bytes32,address)(bool)" $EMISSIONS_ROLE $EMISSIONS_AGENT --rpc-url $BASE_SEPOLIA_RPC_URL

# Emissions agent balance
cast balance $EMISSIONS_AGENT --rpc-url $BASE_SEPOLIA_RPC_URL

PASS criteria:
- Coordinator has EMISSIONS_ROLE on token: true
- Coordinator has MINT_COORDINATOR_ROLE on receipts: true  
- Emissions agent has EMISSIONS_ROLE on coordinator: true
- Emissions agent balance ≥ 10000000000000000 wei (0.01 ETH)

If emissions agent lacks coordinator role but Treasury/deployer is admin:
  HANDOFF with exact Safe calldata or cast send commands for grantRole — HUMAN_REQUIRED if only Safe can sign.

### Gate 4 — Manual mint smoke test (§0.1)
Use emissions agent key. Pick beneficiary from user or default to a fresh throwaway:
  BENEFICIARY=<user provided or cast wallet address --mnemonic "test test..." invalid - use second test key or user address>

Build minimal MintRequest:
- beneficiary: BENEFICIARY
- tokenAmount: 1000000000000000000 (1 ether)
- receiptId: 1
- receiptAmount: 1
- signalId: keccak256("section0-smoke-test") — use cast to compute bytes32
- epoch: 1
- extraData: 0x

Execute mintForSignal via cast send (tuple encoding). Example pattern:
  cast send $COORDINATOR "mintForSignal((address,uint256,uint256,uint256,bytes32,uint64,bytes))" "(...)" --rpc-url $BASE_SEPOLIA_RPC_URL --private-key $PRIVATE_KEY_TESTNET

Verify after tx:
- cast call $AFITOKEN "balanceOf(address)(uint256)" $BENEFICIARY
- cast call $AFITOKEN "totalSupply()(uint256)"
- Optional: cast receipt <txHash> and confirm MintCoordinated in logs via cast logs

PASS: balanceOf(beneficiary) increased; totalSupply > 0; tx succeeded.

### Gate 5 — Write results artifact
Create/update: afi-docs/specs/audit/SECTION0_RESULTS.md with:

| Checklist row | Status | Evidence |
|---------------|--------|----------|
| (every Section 0 row) | PASS/FAIL/HUMAN_REQUIRED | tx hash, cast output, addresses |

Fill role holder table:
- Treasury / admin Safe
- Emissions agent (derived address)
- Test beneficiary

## Definition of Done
All Section 0 rows PASS OR explicitly HUMAN_REQUIRED with remediation steps.
§0.1 mint smoke test tx hash recorded.
User can tick T1 in the checklist.

## Out of scope
- Anything beyond the T1 gate (Section 1 and later)
- Contract code changes
- Mainnet
- Committing .env or keys
```

---

## What Claude Code can do vs what you must do

| Section 0 item | Agent | You |
|----------------|-------|-----|
| Verify Foundry/cast installed | ✅ | — |
| Verify `.env` exists (not print secrets) | ✅ | Create `.env` |
| `BASE_SEPOLIA_RPC_URL` set | ✅ verify | Provide RPC URL (Alchemy etc.) |
| Contracts deployed | ✅ verify bytecode | Redeploy auth if addresses stale |
| Cap, wiring, token metadata | ✅ sanity script | — |
| Coordinator roles on token/receipts | ✅ supplemental cast | Safe signatures if admin ≠ deployer |
| Emissions agent role on coordinator | ✅ supplemental cast | Grant via Safe if missing |
| Fund emissions agent | ✅ check balance | Faucet / send Sepolia ETH |
| `mintForSignal` smoke test | ✅ `cast send` | Provide `PRIVATE_KEY_TESTNET`; pick beneficiary |
| Update `SECTION0_RESULTS.md` | ✅ | Review sign-off |

---

## Known gaps (why the prompt is explicit)

1. **`afitoken_testnet_sanity_checks.sh` does not check** coordinator→token `EMISSIONS_ROLE`, receipts→coordinator `MINT_COORDINATOR_ROLE`, or emissions agent→coordinator `EMISSIONS_ROLE`. Gate 3 fixes this.

2. **Treasury Safe is admin** per sanity script — mint caller needs `EMISSIONS_ROLE` on **coordinator**, not on token directly. Deploy script grants that to deployer only when `admin == deployer`. If your deploy used Safe as admin, you may need a one-time Safe tx.

3. **Env naming:** `DeployAFITestnet.s.sol` uses `PRIVATE_KEY_TESTNET`; `deployment-testnet.md` mentions `BASE_SEPOLIA_PRIVATE_KEY` — agent should use what's in `.env.example`.

4. **`cast send` tuple encoding** for `mintForSignal` is fiddly — xhigh workflow should retry with `forge script` smoke alternative if cast fails (optional fallback script).

---

## Optional: human handoff template (agent fills when blocked)

```markdown
## HANDOFF — Human action required

**Blocker:** <what failed>
**Why agent cannot proceed:** <e.g. Safe must sign grantRole>
**Exact action:**
1. ...
**Resume when:** <condition>
```

---

*Parent checklist: [`AFI_TESTNET_E2E_CHECKLIST.md`](./AFI_TESTNET_E2E_CHECKLIST.md) §0*
