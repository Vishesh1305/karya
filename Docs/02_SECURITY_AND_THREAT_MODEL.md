# 02_SECURITY_AND_THREAT_MODEL.md

## 1. Document Control and Status

| Item | Value |
| --- | --- |
| Document | Third of eight pre-production documents |
| Version and date | 1.4, 2026-09-30 (supersedes 1.3 of 2026-09-29, 1.2 of 2026-09-29, 1.1 of 2026-09-28, 1.0 of 2026-09-27, and 0.1 of 2026-09-24) |
| Status | Approved by the product owner; v1.0 approved 2026-09-27 after the gap audit (section 27), v1.1 changes approved 2026-09-28 (section 27.1); v1.2 and v1.3 changes approved 2026-09-29 (section 28, the hardened isolation and confidentiality baseline, and section 29, the independent audit fixes); binding security baseline for `03` to `07`. Upstream `00` and `01` are both at version 1.3; version 1.4 changes (section 30) directed by the product owner on 2026-09-30, text awaiting the owner's review |
| Authority | Latest user instructions, project instructions, `00` v1.3, `01` v1.3 for its owned contracts, Generator prompt, DEP prompt, labeled assumptions |
| Owner | Security and privacy architecture; product owner accepts privacy choices and residual risks |
| Downstream | `03` runtime, `04` desktop, `05` mobile, `06` UX, `07` phase gates |

The document assigns controls and tests, not production implementation. A changed upstream invariant requires an explicit change record identifying old and new wording, dependent IDs, data migration or incident implications, and product-owner approval. Identifiers in this document start at `SEC-201`, `THR-201`, `CTRL-201`, `PRIV-201`, `IR-201`, `ADR-201`, `RISK-201`, `OQ-201`, and `AC-201`. They do not replace `00` or `01` identifiers.

## 2. Executive Summary and Security Objectives

**Security objective `SEC-201`:** A malicious listing, document, website, model result, or worker cannot promote a factual claim, accept an approval, or create an unauthorized external effect. **`SEC-202`:** Protect candidate and application data across local, optional hosted, and fully self-hosted operation. **`SEC-203`:** Attribute consequential decisions to one authority and preserve enough minimal evidence to explain uncertainty, recovery, and duplicate prevention. **`SEC-204`:** Make loss of a device, key, worker, network link, or permission visible and recoverable without claiming that an employer submission can be rolled back. **`SEC-205`:** Keep the local-only MVP functional with secure local setup and Manual package review, and provide no automated real-world submission path.

The largest residual risks are a compromised unlocked desktop session, a compromised employer or browser session, a malicious update, and an employer submission whose result cannot be observed reliably. Encryption, prompt wording, and internal idempotency do not remove these risks. The release gate for later submission requires demonstrable source permission, destination identity, isolated browser sessions, current policy and claims, an exact bundle, a durable effect record, and safe handling of uncertainty. The MVP needs none of that external submission capability.

## 3. Source Authority, Inherited Contracts, and Conflict Register

| Inherited decision | Security consequence |
| --- | --- |
| `ARCH-01`, `ARCH-07`, `CON-105`, `CON-143`, `ADR-105` | Local-only has one transactional local authority. After successful opt-in enrollment, a control-plane accepted revision owns elected shared state. Offline changes are proposals. A self-hosted control plane obeys the same authority model. |
| `POL-01`, `POL-02`, `CON-111` to `CON-115`, `CON-121`, `CON-122`, `CON-125`, `CON-128` | Imported or model content is unverified; permitted, current, user-verified claims and exact-context sensitive answers control output. Fit cannot authorize eligibility. |
| `CON-103`, `CON-127`, `SM-102` | Complete packages require a verified manifest commit, even without atomic directory rename. |
| `CON-104`, `ADR-103`, `CON-141`, `CON-142`, `SM-104` | Submission identity guard survives grouping edits. Internal idempotency does not imply exactly-once employer submission; uncertainty blocks retries. |
| `ARCH-13`, `POL-06`, `CON-135` to `CON-137`, `SM-103` | Notification is a hint. A current authenticated principal requests a one-use, exact-bundle decision at the authority. |
| `CON-140`, `CON-144` to `CON-147` | Commands validate actor, device, realm, revision, nonce, policy, and version; audit commits with state; deletion tombstones and replica acknowledgements are explicit. |
| `POL-03` to `POL-05`, `POL-09` to `POL-16`, `CON-130`, `CON-131` | Three modes and three strategies only; protective budgets apply even to continuous operation. Dedicated browser profiles, no challenge bypass, no automatic submission in MVP. |

| Register ID | Statements, affected documents | Consequence and recommended resolution | Approval state |
| --- | --- | --- | --- |
| `SEC-CF-201` | `00` section 17 leaves offline synchronized claim authority unstated; `01` `CON-101`, `ADR-105`, `CON-143` make control-plane accepted claims authoritative. Affects `00`, `01`, `02` to `05`. | Use `01`'s approved contract: private offline revisions cannot authorize shared effects. Amend explanatory text in `00` if it is reopened; never run two authorities for one published revision. | Approved `01` baseline; no silent contract change. |
| `SEC-CF-202` | `00` section 24 offers `LIKELY_ELIGIBLE`; `01` `CON-102`, `CON-121`, `CON-128` bar inferred affirmative authorization. Affects `00`, `01`, `02`, `03`, `06`. | Display assessment separately from exact answer authorization. Only verified exact-context answer may become authoritative. | Approved `01` baseline. |
| `SEC-CF-203` | `00` sections 26 and 31 request atomic packages; `01` `CON-103`, `CON-127` specify committed manifest when atomic rename is unavailable. Affects `00`, `01`, `02` to `04`. | Readers reject incomplete or mismatched manifests. | Approved `01` baseline. |
| `SEC-CF-204` | `00` duplicate prevention versus `01` `CON-104`, `CON-141` guard across merge and split. Affects `00`, `01`, `02`, `03`. | Keep application identity separate from canonical job grouping. | Approved `01` baseline. |
| `SEC-CF-205` | `01` `OQ-101` and `OQ-102` remain open after approval. Affects `02`, `03`, `05`, `06`. | Default to explicit selected claim fields, no evidence bytes; fresh exact-context verification of sensitive answers. Do not enlarge either permission by treating document approval as answer to its question. | Product-owner decision required before any broader sync or reuse. |

No new contradiction is required to keep the MVP viable. In version 0.1 the labels inside `00` and `01` still said “draft”; version 1.0 of both documents carries the approved status, and `00` now states the rules behind `SEC-CF-201` to `SEC-CF-204` directly (`00` `CHG-009`). `SEC-CF-201` through `SEC-CF-204` are recorded for traceability, not requests to reverse approved contracts.

## 4. Scope, Assumptions, Deployment Topologies, and Security Boundaries

In scope: desktop UI and local authority, separately packaged worker, model endpoints, local and user-selected stores, permitted source and employer sites, optional hosted or self-hosted authority, mobile companion and push transport, installers and updates, logs, backups, exports, and recovery. An employer site, external model provider, cloud operator, self-host operator, and OS are outside the candidate-controlled application trust domain. Employment law adjudication, a universal scraping entitlement, defense against a fully compromised host, and guaranteed remote deletion from third parties are outside demonstrable product guarantees.

| Topology | Active authority | Security condition | Safe failure |
| --- | --- | --- | --- |
| Local-only MVP | One local transactional authority and protected local store | Desktop and worker authenticate over a scoped local channel; output and model egress require separate grants. | Locked key or lost local authority pauses mutations; saved data remains accessible only after legitimate unlock or restore. |
| Optional hosted sync | One hosted realm for accepted shared revisions, approvals, guards, and leases; local drafts remain local | Explicit staged enrollment, field-level selection, scoped device and worker registration, server-side account isolation. | Outage means cached view and private proposals only; no fresh shared effect. |
| Fully self-hosted sync | One user-chosen control-plane realm with the same protocol | Operator owns endpoint, keys, backups, upgrades, TLS, and incident response; remote clients verify configured endpoint identity. | On misconfiguration or compromise, disable remote actions; local-only restoration requires explicit split or re-enrollment, never dual authority. |

Assumptions `SEC-A-201`: single-user local MVP (`ASM-02`); reference hardware resolved in v1.1 as the product owner's MacBook Pro running macOS (`00` `ARCH-15`, `OQ-01`; v1.0 had selected Pop!_OS). `SEC-A-202`: a separately packaged worker can have a distinct process identity, but a shared OS user cannot be treated as a strong security boundary. `SEC-A-203`: supported model and browser adapters can be denied network access outside their approved endpoints where the platform permits it; where OS enforcement cannot be demonstrated, user-facing capabilities narrow. `SEC-A-204`: a user's account at an employer site is independent of this product's account. `SEC-A-205` (v1.0): the MVP reference platform is Linux (Pop!_OS), so the Linux rows of `ADR-201` are on the MVP critical path, and Secret Service behavior under the owner's desktop session is unproven until `04` and `00` `EXP-01` test it [RES-209]. v1.1 update: the MVP reference is now macOS, so Keychain wrapping in `ADR-201` is the MVP path; the Linux rows and this assumption apply when Pop!_OS is proven as a compatibility target.

## 5. Assets, Data Inventory, and Classification

Classification inherits the six classes from `01` section 23. A record can carry multiple classes; its effective handling uses the stricter class. Metadata, digests, URLs, filenames, error messages, and logs can be personal even when their payload is absent. The actual data map and lifecycle is in sections 18 and 19.

| Asset | Class | Integrity or availability consequence |
| --- | --- | --- |
| Candidate name, address/contact channels, education, employment, portfolio and resume | `CANDIDATE_PERSONAL`, sometimes `CANDIDATE_SENSITIVE` | Identity theft, inaccurate applications, confidentiality breach. |
| Residence, authorization, immigration status, sensitive form answers, demographics and compensation commitments | `CANDIDATE_SENSITIVE`, `APPLICATION_CONFIDENTIAL` | Harmful disclosure or false legally consequential answer. |
| Evidence originals, verified claims, revisions, permitted uses, readiness, policies | Personal or sensitive by contents | Untruthful output or unauthorized change. |
| Job observations, source snapshots, URLs and adapter permission state | `PUBLIC_SOURCE` unless captured forms or personalized pages add confidential content | Source restriction breach, redirect or policy poisoning. |
| Documents, manifests, exact final answers, confirmation evidence, screenshots | `CANDIDATE_PERSONAL` or `APPLICATION_CONFIDENTIAL`; sensitive if contents require | Exposure, wrong bundle, unsupported submission, failed reconciliation. |
| API keys, refresh tokens, browser cookies, local encryption keys, worker credentials, signing keys, filesystem grants | `SECRET` | Account takeover, data compromise, unauthorized external effects. |
| Audit events, app guards, leases, tombstones, safe metrics | `OPERATIONAL`, with contextual personal or sensitive treatment | Duplicate actions, hidden abuse, inaccurate deletion claims. |

**`CTRL-201` classification enforcement:** Ingestion defaults uncertain or mixed content to the more restrictive class; only authority-accepted metadata can lower it after explicit policy review. All components enforce the effective class at read, sync, model-call, export, log, and retention boundaries. A downgrade failure blocks disclosure. Evidence: policy fixtures with mixed documents and sensitive filenames. Applies MVP and later.

## 6. Actors, Adversaries, Capabilities, and Abuse Cases

| Actor or failure source | Capability and incentive | Boundary it can cross without an application flaw |
| --- | --- | --- |
| Candidate | Approves own claims, preferences, local disclosure and later authorized review; may make an honest mistake | Can authorize actual disclosure or submission if gates pass, but cannot create externally verified facts by assertion from a posting. |
| Another local user, thief, malware | Read files on shared device; may control unlocked session, inject process, or steal browser profile | OS account or process isolation may fail, especially for same-user malware. |
| Malicious listing or employer page, poisoned uploaded resume or repository | Supply arbitrary text, forms, redirects, attachments, and scripts within site origin | No policy, claim-verification, local filesystem, or tool authority. |
| Malicious model response or compromised provider | Return crafted structured content, leak submitted data under provider terms, suggest tool actions | No command, secret store, or authority access. |
| Rogue worker or registered device | Present stale credential, counterfeit results, flood commands | Authentication alone does not give user approval or cross-account access. |
| Push and mail transport or spoofed notification | Delay, forge visual hint, expose lock-screen metadata | No accepted approval or current review bundle. |
| Hosted or self-host operator, update publisher, dependency maintainer | May access service-side data and deployment surface | Operational powers are bounded by encryption, separation, audits, and signed artifacts only to the degree proved by implementation. |
| Network adversary, compromised DNS, outage | Redirect, block, replay traffic or create partial failures | No authenticated session or successful consequence without verified destination, fresh authority, and applicable controls. |

Abuse scenarios include automated high-volume requests against a source, a forged approval after a phone theft, candidate data exfiltration through a job-description “instruction,” a local model endpoint bound publicly, and retrying an application after a crashed submit click. The risk register gives testable paths.

## 7. Trust Boundaries and Sensitive Data Flows

Each arrow denotes data moving between independently validated contexts. Diagrams are conceptual, not a guarantee that processes or operating systems enforce isolation.

### 7.1 Local-only

```mermaid
flowchart TB
  D["Desktop and local authority"] <-->|"authenticated local IPC"| W["Worker process"]
  U["Untrusted files and listings"] --> W
  W -->|"bounded request"| M["Chosen model endpoint"]
  W -->|"validated package"| S["Protected local store or granted destination"]
  W -->|"later, approved origin"| E["Employer site"]
```

Local IPC carries command IDs and capability-scoped actions (`CTRL-202`). File and posting ingestion is untrusted (`CTRL-214`). Worker to model egress is task-minimal (`CTRL-215`, `CTRL-226`). Outputs are granted, validated and manifest-bound (`CTRL-213`). The employer boundary is closed in MVP (`CTRL-218`). A worker has access to a particular browser profile only for its scoped site task (`CTRL-212`).

### 7.2 Optional hosted synchronization

```mermaid
flowchart TB
  D["Desktop local authority and cache"] <-->|"enrolled sync"| C["Hosted control plane"]
  W["Registered worker"] <-->|"scoped task channel"| C
  P["Mobile cached companion"] <-->|"authenticated fetch and decision"| C
  C -->|"minimal alert"| N["Push transport"]
  W -->|"validated origin, later only"| E["Employer site"]
```

Authority transfers per accepted field and revision, never merely because a connection exists (`CTRL-203`). Cross-account object authorization is server-side (`CTRL-204`). Worker task grants are short-lived (`CTRL-205`). Notification data is a hint (`CTRL-208`). Mobile offline decisions are blocked (`CTRL-207`). External submit effects require durable guarding and current authority (`CTRL-219`).

### 7.3 Fully self-hosted synchronization

```mermaid
flowchart TB
  O["Self-host operator"] -->|"keys, backup and updates"| C["Self-host control plane"]
  D["Desktop"] <-->|"verified configured endpoint"| C
  P["Mobile"] <-->|"verified configured endpoint"| C
  W["Remote worker"] <-->|"scoped outbound channel"| C
  C -->|"optional minimal alerts"| N["Push provider"]
```

Operator access is a separate trust boundary: access control, backups, signing and audit are operator responsibilities (`CTRL-209`, `CTRL-211`, `CTRL-223`). A self-hosted label does not imply end-to-end confidentiality from that operator or automatic public reachability. A private ingress or VPN is an option, with verified TLS and authenticated application protocol for remote connections. Operator compromise triggers the same shared-authority freeze as hosted compromise.

**Boundary coverage `SEC-206`:** desktop/worker `CTRL-202`, `AC-201`; worker/site `CTRL-217` to `CTRL-219`, `AC-205`; worker/model `CTRL-215`, `CTRL-226`, `AC-204`, `AC-217`; device/control `CTRL-203`, `CTRL-204`, `CTRL-225`, `CTRL-206`, `AC-202`; control/push `CTRL-208`, `AC-203`; local/synced authority `CTRL-203`, `AC-206`; app storage/destination `CTRL-213`, `AC-207`; operator/control `CTRL-209`, `CTRL-223`, `AC-211`.

## 8. Threat Modeling Method and Risk Prioritization

Risk categories use impact and plausibility, not numerical probabilities. Impact **critical** means unauthorized external submission, cross-account sensitive disclosure, key compromise with durable access, or corrupted authoritative eligibility. **High** means significant personal disclosure, materially false application output, or undetected action loss. **Moderate** means contained leak or recoverable interruption. Plausibility is **credible** when reachable from a routine untrusted input or common device loss, **conditional** when another failure or privileged compromise is necessary, **remote** only when multiple independently tested barriers must fail. Priority P0 is critical plus credible or conditional, P1 is high plus credible or critical plus remote, P2 covers the remainder. No frequencies or percentages are asserted. Product owner accepts residual P0 before the corresponding feature ships; a blocking acceptance criterion cannot be waived solely by accepting risk.

For compactness each threat row uses `asset / adversary / entry and boundary / path`; it then names impact, likelihood reasoning, prevention, detection, containment, recovery, residual risk, owner, and test. P0 on later features is a design priority and does not require implementing those features in MVP.

## 9. Threat Register

| Threat, priority | Asset; adversary or failure; entry and plausible path | Impact and plausibility rationale | Prevention; detection; containment; recovery | Residual risk; owner; test |
| --- | --- | --- | --- | --- |
| `THR-201` P1 | Local keys and documents; thief or shared user; device and OS account; reads unlocked cache or stolen backup. | High, credible because portable devices are lost and shared. | `CTRL-209` lock and encrypted store; `CTRL-211` protected backups; access audit; revoke device, sessions and keys, recover from clean backup. | Unlocked same-user compromise remains; desktop `04`; `AC-207`, `AC-211`. |
| `THR-202` P0 | Claims, secrets and tasks; malware or compromised worker; IPC and worker context; calls authority with forged results or reads task secrets. | Critical, conditional on worker compromise. | `CTRL-202`, `CTRL-205`, `CTRL-212`; anomalous effects and capability audit; quarantine worker and invalidate grants; rebuild and reconcile. | Same-user malware can inspect memory; `03`, `04`; `AC-201`, `AC-209`. |
| `THR-203` P0 | Candidate data and output; malicious listing, website, resume, repository or model output; untrusted text enters model and tools; instructs exfiltration or claim promotion. | Critical, credible from routine ingestion. | `CTRL-201`, `CTRL-214` to `CTRL-216`; rejected output and egress logs; quarantine item/provider; reverify claims and regenerate. | Semantic manipulation may evade classifiers; `03`; `AC-204`. |
| `THR-204` P0 | Employer identity, browser session; malicious URL or redirect; fetch or form navigation to attacker or private IP. | Critical, credible from source content. | `CTRL-217`; destination-change audit; block origin, retire adapter and invalidate bundle; user verifies canonical site. | Legitimate site may itself be compromised; `03`; `AC-205`. |
| `THR-205` P0 | Cookies, credentials, API key; profile theft or logging; worker filesystem and diagnostics; reuse in browser or model API. | Critical, conditional on local access or leak. | `CTRL-209`, `CTRL-210`, `CTRL-212`, `CTRL-222`; leak scanner; revoke sessions, rotate key, isolate profile; restore scoped access. | Third-party revocation may lag; `03`, `04`; `AC-208`. |
| `THR-206` P0 | Approval and exact bundle; rogue device or replay; command endpoint accepts stale nonce, version or notification tap. | Critical, credible on remote review surface. | `CTRL-206` to `CTRL-208`; race/replay audit; revoke device and pending approvals; reissue reviewed bundle. | An already completed external effect cannot be retracted; `03`, `05`; `AC-202`, `AC-203`. |
| `THR-207` P1 | Eligibility and stop status; offline mobile or sync conflict; stale cache appears authoritative. | High, credible during outage. | `CTRL-203`, `CTRL-207`; stale indicators and conflict audit; freeze consequential action; fetch authoritative snapshot and resolve competing revision. | User can still act manually outside product; `05`, `06`; `AC-206`. |
| `THR-208` P0 | Other candidate's profile; broken realm authorization or mis-scoped worker; object ID traverses account boundary. | Critical, conditional on implementation flaw. | `CTRL-204`, `CTRL-205`; access-denied anomaly; quarantine principal and suspend realm; investigate and notify as applicable. | Insider with privileged database access remains; `03`; `AC-210`. |
| `THR-209` P0 | Worker channel and task; stolen enrollment credential or worker impersonation; false execution and effect receipt. | Critical, conditional on credential theft. | `CTRL-205`, `CTRL-210`; registration and token audit; revoke worker and lease; compare effect evidence and re-enroll. | In-flight external effect uncertain; `03`; `AC-209`. |
| `THR-210` P1 | Candidate facts; unprotected local inference service; LAN or public API reaches model context and task data. | High, credible when endpoint is misconfigured. | `CTRL-215`; endpoint reachability check; disable provider and revoke exposed tokens; bind privately or reconfigure authenticated TLS. | Provider code may still be compromised; `03`; `AC-204`, `AC-217`. |
| `THR-211` P0 | All stores and worker; malicious dependency or update; installer supply chain executes code. | Critical, conditional on publisher compromise or validation failure. | `CTRL-223`; provenance and signature alert; halt rollout, revoke signer, restore signed known-good build, rotate exposed keys. | Trusted publisher compromise may pass signing; `04`, `07`; `AC-212`. |
| `THR-212` P1 | Source accounts and availability; excessive automated requests; broad or continuous run ignores caps. | High, credible if scheduling faulty. | `CTRL-224`; per-source and global counters; circuit breaker; pause source and restore bounded policy. | Sources may change rate limits; `03`; `AC-213`. |
| `THR-213` P0 | Submitted answers and application; model invents authorization or form changes after review. | Critical, credible in later form workflows. | `CTRL-216`, `CTRL-218`, `CTRL-219`; changed-field and answer mismatch audit; pause and invalidate bundle; user reviews exact question. | Human can affirm an inaccurate fact; `03`, `06`; `AC-205`. |
| `THR-214` P1 | Backups, logs, screenshots; unsafe export or support attachment; sensitive bytes leave protected store. | High, credible in diagnostics. | `CTRL-211`, `CTRL-221`, `CTRL-222`; DLP fixture and download inventory; stop sharing, rotate exposed secrets, purge where possible. | Recipients may retain copies; `03`, `04`; `AC-208`, `AC-211`. |
| `THR-215` P0 | Application identity and submission outcome; worker crash, partition, lost lease or deceptive confirmation; repeat submit under new key. | Critical, credible in later automation. | `CTRL-219`, `CTRL-220`; uncertain-effect event; freeze identity guard; reconcile employer evidence before any new attempt. | Employer may give no conclusive evidence; `03`; `AC-214`. |
| `THR-216` P1 | Synced data deletion; offline or retired device fails tombstone receipt; stale replica resurfaces data. | High, conditional on lost replica or conflict. | `CTRL-203`, `CTRL-221`; pending acknowledgement report; quarantine stale client and require full snapshot before action; purge on reconnection or mark unreachable. | Offline uncontrolled copy cannot be remotely erased; `03`, `05`; `AC-215`. |
| `THR-217` P0 | Local output or provider credentials; archive, DOCX, PDF or renderer exploits parser; content escapes processing area. | Critical, conditional on vulnerable parser. | `CTRL-212`, `CTRL-214`, `CTRL-223`; crash and egress anomaly; quarantine evidence and renderer, update or roll back; rerun safe import. | Process isolation is incomplete on desktop; `03`, `04`; `AC-204`, `AC-212`. |
| `THR-218` P0 (v1.1) | Candidate data, local files and credentials; consumer chat service or official subscription developer tool (`00` routes R1 and R2); a relay prompt carries excess personal data to a consumer service, a pasted reply smuggles an instruction or false claim, or an agentic vendor tool reads files, runs commands, or browses on its own initiative. | Critical, credible because R1 tools are built for agentic coding and R2 relies on user copy and paste. | `CTRL-215`, `CTRL-216`, `CTRL-227`; disclosure ledger `PRIV-203` and rejected-reply audit; disable the route and revoke the tool sign-in at the vendor; regenerate affected outputs. | Consumer services retain data under their own terms; `03`, `06`; `AC-219`. |

### 9.1 Coverage of the Generator threat list (v1.0)

The Generator names threats the model must cover. Each maps to at least one register entry above.

| Generator threat | Register entry |
| --- | --- |
| Stolen device | `THR-201` |
| Compromised worker | `THR-202`, `THR-209` |
| Malicious browser page | `THR-203`, `THR-204` |
| Prompt injection in job descriptions or company websites | `THR-203` |
| Poisoned resume or uploaded document | `THR-203`, `THR-217` |
| Malicious redirects | `THR-204` |
| Credential leakage | `THR-205` |
| Secret leakage in logs | `THR-205`, `THR-214` |
| Insecure local model endpoints | `THR-210` |
| Cross-user data leakage | `THR-208` |
| Approval replay | `THR-206` |
| Notification spoofing | `THR-206`, `CTRL-208`, `AC-203` |
| Dependency or update compromise | `THR-211` |
| Unsafe generated application answers | `THR-213` |
| Excessive source scraping | `THR-212` |
| Compromised browser profile | `THR-205` |

## 10. Identity, Authentication, Sessions, and Account Recovery

**`CTRL-202` local identity and IPC:** One profile does not mean anonymous mutation. Local authority binds the initiating desktop session and bounded worker connection to the OS user and installation. Use an unguessable per-installation local channel credential, peer identity where supported, strict socket or pipe permissions, and command capability checks; a localhost TCP port without authentication is insufficient. Worker may request tasks, report evidence and results, but cannot present itself as an approved human. Locking the product closes sensitive views and blocks new user decisions; background Manual preparation requires separately consented unlock behavior and cannot bypass the readiness gate. Validate with a second OS user and hostile local process. MVP.

**`CTRL-225` synchronized account authentication:** Propose passkeys as preferred where supported, plus recovery method chosen at enrollment. A password fallback, if provided, uses a current memory-hard salted password hash, online throttling, and step-up for device enrollment, recovery, export, deletion, sensitive sharing and consequential approvals; no security questions. Hosted sign-in is required only for optional sync, never for local-only use. A self-hosted realm applies the same API semantics and documents operator-managed identity dependencies. Session tokens are short-lived, rotate on refresh, are bound to realm and device registration, and are invalidated on sign-out, device revocation, account recovery or security incident. Proposed configuration, subject to UX and threat validation: 15-minute access token, maximum 30-day renewable device session, and a step-up proof no older than five minutes at a consequential decision. Timeouts are product proposals, not NIST certification. NIST SP 800-63-4 gives reauthentication and authenticator lifecycle guidance; OWASP recommends adaptive password hashing. [RES-201; RES-202; RES-203] Later release.

Recovery: pre-enrolled recovery method plus rate-limited verification; a lost last authenticator cannot be silently replaced by an email link and immediately authorize a submission. Recovery revokes all prior sessions and pending approvals, requires re-enrollment of devices, and places submission-capable actions in a 24-hour proposed hold with clear user notice and a manual appeal path. A self-hosted operator can restore access only through the documented recovery procedure, with an auditable break-glass event; operator authentication is not a candidate approval. The hold is a proposed policy to validate against usability and account-takeover risk before remote submission.

## 11. Authorization, Roles, Devices, Workers, and Authority Enforcement

| Principal | Authorized capability | Never inferred from its ID alone |
| --- | --- | --- |
| Candidate user | Verify own claims, choose data disclosure, issue allowed commands and exact review decisions in current realm. | A registered `dev_` does not replace authentication or recent step-up. |
| Desktop or mobile device | Cache and present state; send authenticated requests bound to account and realm. | A push token, device registration or cached bundle is not approval. |
| Worker | Execute scoped assigned computation, access task-specific local secrets and site profile, report evidence. | Worker does not confirm claims, accept approvals, decide eligibility answers or alter another account. |
| Operator | Maintain hosted or self-hosted service and respond to incidents with audited role. | Operator has no authority to consent for candidate or silently view raw data. |
| System authority | Validate and commit commands, guard transitions, issue leases and write audit. | An unsigned event or worker status is not an authoritative fact. |

**`CTRL-203` authority and sync:** Enrollment stages inventories and explicit selected sharing; remote authority begins only after accepted revision and acknowledged binding (`CON-143`). Server rejects stale, unpublished or wrong-realm revisions and unavailable authority returns `ERR-114`. Conflict is `ERR-113`, not last-write-wins. A reconnecting device must refresh a gapful stream before consequential action. MVP local path, later sync path.

**`CTRL-204` object authorization:** Check realm, account, profile, principal role, object ownership, allowed command, classification, and expected revision at every control-plane mutation and read. Do not use client-supplied object IDs as authorization. Use separate credentials and scoped operator roles; bulk export requires recent user step-up. Rejection gives a safe error and audit signal without revealing existence of another user's object. Later.

**`CTRL-205` worker registration and tasks:** A worker enrolls through an authenticated user action, binds a public credential to realm and installation, rotates short-lived task credentials, proves possession over its outbound channel, and receives only required task fields, narrow local secret handles, budget and allowed effects (`CON-132` to `CON-134`). No credential is shared among workers. Authorization checks occur at assignment and immediately before external effect. Revocation denies new tasks and grants, kills reachable active lease, wipes worker-held task secrets where possible, and flags any effect in progress uncertain. A disconnected worker must not start a new shared external effect. Local MVP uses equivalent scoped local permissions; remote enrollment comes later.

**`CTRL-206` consequential command gate:** The authority authenticates actor and device; checks recent step-up where needed, realm, scope, exact bundle revision and digest, nonce, expiry, expected authority revision, dependency revisions, policy and audit transaction (`CON-136`, `CON-140`, `CON-142`). Failure does not partially mutate or expose protected values. `CMD-101`, `CMD-102`, `CMD-105`, `CMD-106`, `CMD-107`, `CMD-108`, `CMD-110`, `CMD-111`, `CMD-112` use command-specific checks; purely computational proposals cannot call these as a user. Claim confirmation and package completion still work in local MVP, while submission authorization is absent. `EVT-101`, `EVT-102`, `EVT-106` to `EVT-112` carry audit-safe accepted results.

**`CTRL-207` offline and revocation:** Offline mobile shows last-sync time and read-only sensitive action states, cannot queue `CMD-107` or imply stop acknowledgement. Revocation of a registered device invalidates its sessions and pending decisions; another active device sees revocation before approving. An in-flight external effect is not rewritten after revocation. Later.

## 12. Secrets, Credentials, Browser Sessions, and Key Lifecycles

**Architecture choice `ADR-201`:** Use a random per-installation data encryption key (DEK) for the local encrypted database and application-managed sensitive blobs; wrap the DEK with an OS-protected key where a tested store exists. Apple Keychain is intended for small secrets; Windows user-scoped DPAPI protects keys but applications running under the same user can use the protection context; Linux Secret Service implementations have variable unlocking and client-access behavior. These are platform capabilities, not identical hardware-backed guarantees. [RES-204; RES-205; RES-206; RES-207; RES-208]

| Alternative | Selection and limit |
| --- | --- |
| OS-protected DEK wrapping | Preferred on tested macOS and Windows and on Linux with a verified usable secret service. Enables unattended worker after approved unlock policy, but same-user malware may still request secrets. |
| User passphrase-derived wrapping | Explicit Linux fallback when a usable protected service is absent, with memory-hard KDF, unique salt, configurable work factor and backup recovery material. Requires user unlock after restart; no unattended execution until unlocked. |
| Unprotected key in file, environment, or source control | Rejected for persistent keys. Environment variables may inject ephemeral process credentials in managed deployment, but can leak through diagnostics, process environments or operators. |
| Hardware-only or end-to-end encrypted hosted store | Consider only after target platform prototypes and key sharing/recovery design; cannot assume a secure enclave, TPM or operator-blind hosting universally. |

Pop!_OS reference consequence (v1.0; v1.1 applies it to the Linux compatibility target): an open upstream issue reports that on Pop!_OS with the COSMIC desktop, libsecret clients can hang indefinitely when the keyring daemon restarts mid-session and no unlock prompt appears [RES-209]. Every Secret Service call from the desktop or worker therefore has a bounded timeout. A timeout or locked collection pauses only the tasks that need the secret and shows an unlock action. The product never falls back to an unwrapped key. When no working Secret Service exists in the session, the passphrase-derived wrapping row applies. `AC-218` tests this.

**`CTRL-209` key lifecycle:** Generate random DEKs and independent key identifiers; encrypt blobs using an authenticated encryption primitive with unique nonces and associated account or profile context, implemented through a maintained library. Store ciphertext and key ID, never key bytes in the database. Unlock key only to the owning process; minimize memory lifetime and prevent debug or crash dumps containing secrets where possible. Rotate wrapping key after OS account compromise and DEK after suspected exposure, re-encrypt records with resumable journal and versioned backup, verify decryptability before retiring old key. A lost key without authorized recovery material makes ciphertext unrecoverable; display this explicitly before destructive rotation. Lock and wipe transient plaintext on logout, stop and crash recovery. MVP for local storage; later per-realm server keys and rotation.

**`CTRL-210` secret inventory and grants:** Model API keys, browser cookies, site tokens, local model endpoint credentials, worker keys, session/refresh tokens, signing keys, database keys and scoped destination grants have independent owners, scopes, storage, rotation and revocation. Worker receives a short-lived handle or narrowly scoped value just before use; never place secret values in command/events, package metadata, telemetry, model prompts, URL query strings, or default logs. Browser cookies remain in site-scoped dedicated automation profiles on the originating worker and never sync. User signs into employer site directly through supported interactive flow; do not capture raw passwords for replay or bypass a security challenge. Rotate or revoke the affected third-party credential at its issuer after exposure; local deletion alone does not revoke it. MVP applicable to provider keys; site credentials later.

| Secret | Create and protect | Use, rotate, recover and delete |
| --- | --- | --- |
| Local DEK and evidence/document keys | Random on profile creation; OS store or passphrase wrap; separate blob contexts. | Unlock for specific local operations; rewrap on platform migration; re-encrypt on DEK rotation; deletion destroys live key, backups expire by policy. |
| API/model token | Enter through protected UI or OS injection, store in protected store, provider and task scoped. | Worker temporary use; provider-side revocation and replacement; no automatic disclosure to unrelated provider. |
| Browser cookies/site session | Created by user's permitted interactive login in isolated profile. | Only approved site adapter; invalidate at site and destroy profile on compromise; user may need to log in again. |
| Worker enrollment key and short-lived credentials | Unique per worker, private key in protected store where possible. | Rotate and revoke centrally or locally; reassess in-flight effects; re-enroll after clean rebuild. |
| Control-plane session and signing keys | Separate service-managed secrets, access logged, backups protected. | Rotate with overlapping verification window for existing safe reads; force reauth on incident; expired or revoked signer cannot create approvals. |
| Destination grant | OS-scoped bookmark, URI permission or path ACL, bound to device. | Revalidate before manifest commit; revoke at OS and app; never sync the actual grant. |

**`ADR-202`:** A hash of document bytes verifies integrity under a specified canonical representation; it is neither encryption nor authorization. A digest in a shared record may expose correlation and must be treated as personal metadata where linkable. No security decision relies on hash alone as proof of who approved or who received an application.

## 13. Encryption, Storage Protection, Transport, and Backups

**`CTRL-211` storage and backup:** Encrypt local authoritative database and app-managed sensitive blob store with tested authenticated protection, limit filesystem ownership and inherited ACLs, avoid world-readable temporary files, exclude plaintext from swap or crash dumps where feasible, and restrict backup access. User-selected destinations are outside guaranteed app-managed encryption: show their protection status, omit sensitive answer files by default, and require explicit choice to export sensitive content. A platform encryption option or disk encryption is defense in depth, not a substitute for per-object authorization. Backups are versioned, encrypted with a recovery key independent of a lost live installation, integrity checked and periodically restored in an isolated test. Proposed later hosted restore target inherits `NFR-02`'s 24-hour chosen-point objective; prove it before a claim of readiness. Do not claim secure deletion from SSD or external user-selected destinations when the platform cannot establish it. MVP local restore, later hosted.

**`CTRL-226` transport and endpoint:** Remote device, worker, hosted model and self-host endpoints use verified TLS with hostname and certificate validation; reject downgrade, bad certificate and insecure redirects. Mutating requests use authenticated session and protocol-level anti-replay, independent of TLS. A local Unix socket or named pipe uses OS access checks plus installation credential. If a local model runs in another process, loopback-only binding and authentication are required; any reachable network endpoint requires authenticated encrypted transport and an endpoint identity check. Source fetches use the URL policy in section 16. Self-host operators must supply a trusted endpoint configuration; no silent “accept any certificate” mode. Engineering test checks expired certificates, wrong hosts and proxy interception. TLS configuration is checked against current OWASP transport guidance at build time. [RES-210]

**`ADR-203`:** Per-user application-layer encryption for hosted synced fields is a potential later option, but would complicate server-side validation, multi-device recovery and search. The baseline uses service-side at-rest encryption, per-account authorization, minimal selected sync and limited operator access; it does not promise the cloud operator cannot see synchronized plaintext. Self-host operators have similar practical access. Any stronger confidentiality claim requires its own key ownership and recovery design.

## 14. Worker, Browser, File, and Process Isolation

**`CTRL-212` execution isolation:** Launch a separate worker with least filesystem and network permission feasible on each target OS. Give each employer site or tenant a dedicated automation browser context or profile, isolated cookies and downloads, no access to everyday browser credentials, no cross-site copy of sessions, and no remote debugging interface reachable from another process or network. Limit process child creation, download paths, output size and browser context lifetime. Sandboxing on macOS, Windows and Linux varies; `04` must prove permissions and sidecar behavior rather than treat a separate PID as a security sandbox. A malicious page may still exploit the browser or same-user process, so the consequence is reduced reach, not elimination. MFA, CAPTCHA and authentication challenges pause for direct user action, never use evasion tooling (`POL-10`, `POL-11`).

**`CTRL-213` output isolation:** Reject absolute or parent-traversal paths from untrusted names, normalize Unicode for comparison while retaining original provenance, use stable opaque IDs and bounded sanitized labels in filenames, disallow symlink escapes, verify current grant and safe writable root, write into a private staging directory, check hashes and contents, then publish a validated manifest marker (`CON-127`; exact layout, naming and commit protocol in `01` `CON-148`). Distinguish app-managed from user-selected destination. Retain prior package versions; failed staging is quarantined and time-bounded. Verify no output package implicitly contains exact sensitive answer files or credentials. MVP.

**`CTRL-214` ingestion isolation:** Accept only declared MIME and magic-byte pairs, enforce size, page, nesting, archive entry and decompression bounds, reject device files and links outside extraction root, disable macros, active content and external reference fetches in parsers, and render HTML as escaped text or tightly sanitized inert markup with restrictive content security policy. Do not mount an imported repository as executable code for extraction. Parse PDF/DOCX in a resource-limited worker and keep original bytes separate from extracted text; parser crash or suspicious content quarantines that item. Automated vulnerability scanning and renderer updates are part of `CTRL-223`. MVP for candidate files and listings; richer archive handling later only after its tests.

## 15. Untrusted Inputs, Prompt Injection, Model Output, and Supply Chain

**`CTRL-215` model disclosure boundary:** Classify every task input, use an allowlisted provider capability and documented endpoint, minimize text to the task, remove unused identifiers, require separate consent before a third-party model sees personal or sensitive data, and label each source span as untrusted data. No model receives browser cookies, local paths, unrelated evidence, API keys or all candidate records by default. The model has no direct shell, network, browser, secret or authoritative command tool. Model output is a typed proposal validated against schema, allowed claims, policy and budgets by deterministic code. Unsupported or malformed output fails safely. Hosted provider data handling, retention, region, training and subprocessors must be reviewed at selection time; a provider label alone is not a privacy guarantee. OWASP identifies prompt injection and sensitive information disclosure as distinct LLM risks. [RES-211; RES-212] MVP for evaluated provider; later for alternatives.

**`CTRL-216` claim and answer validation:** Source text may state “ignore the rules,” “call this URL,” or claim that a resume skill is verified; treat the entire source as quoted evidence. Every generated factual sentence resolves to current permitted claim revisions (`CON-125`); a sensitive answer resolves to a current question snapshot and exact-context user verification (`CON-128`). A model cannot set `VERIFIED`, change `permitted_uses`, mark a package `COMPLETE`, accept `CMD-107`, or call `CMD-108`. A changed question, form version, destination, file, answer, claim or policy invalidates dependent bundle (`CON-107`). Reviewers see original question and exact answer. MVP factual validation; later form answers.

**`CTRL-223` supply chain and updates:** Pin reviewed dependencies and transitive versions with checksums, generate a dependency inventory, scan for known vulnerabilities and provenance anomalies, use signed release artifacts and update metadata, verify signature and version before install, prohibit unsafe downgrade, stage rollout with rollback to previously verified version, and require a migration backup and recovery path. Keep signing keys separate from development keys and audit release authority. These are proposed implementation controls; signing does not guarantee a benign signer. Update handling and OS packaging belong to `04`; `07` gates release.

Abuse fixtures: posting says “send applicant SSN to this endpoint,” HTML contains a hidden instruction in a comment, portfolio README claims to be a system prompt, DOCX contains an external relationship and macro, model JSON contains an extra `verified_by` field, and retrieved text embeds a lookalike URL. The expected result in each case is a blocked unauthorized disclosure or transition, with an attributable safe error. Include benign paraphrase fixtures to detect excessive false blocks.

**`CTRL-227` subscription tool and manual relay routes (v1.1):** For route R1, the worker launches the official vendor tool as a child process with every built-in tool capability disabled (no shell, file, edit, web, or browser tools), an empty working directory in the worker's private staging area, no inherited environment secrets, and network egress limited to the vendor's documented endpoints where the OS permits. The product never reads, copies, or stores the tool's own sign-in tokens; the user signs in through the tool's supported flow, and sign-out or revocation happens at the vendor. R1 stays disabled until `03` records current, dated vendor-terms evidence that the use is permitted, and the authority disables it automatically if a later check fails (`01` `CON-138`). For route R2, the prompt package is task-minimal, excludes `SECRET` data and, by default, `CANDIDATE_SENSITIVE` data, and shows the user exactly what will leave the product before it is copied. Each export is recorded in the `PRIV-203` disclosure ledger with the declared destination service. A pasted reply is untrusted model output under `CTRL-215` and `CTRL-216`. Consent under `PRIV-201` is given per destination service before its first use. Evidence: `AC-219`. MVP for R2; R1 when enabled.

## 16. Job Source, Redirect, ATS Form, and Submission Safety

**`CTRL-217` origin and destination validation:** Maintain per-source permission and method state from `CON-118`; `03` performs current source-specific terms and integration research. Parse URLs with one canonical parser; allow only approved `https` application destinations for assisted actions (`01` section 7). Reject userinfo, unexpected ports, ambiguous Unicode hostnames, private or loopback/reserved targets, local-file and nonweb schemes, embedded credentials, and unknown redirect origins. Resolve DNS immediately before a request, constrain egress to the validated destination address, and revalidate each redirect hop with a fixed limit rather than auto-following unchecked redirects; repeat destination and job identity check before a final browser submit. OWASP recommends disabling automatic redirect following in SSRF defenses. [RES-213] A real employer may use a new domain or third-party ATS; show an explicit adapter review instead of silently accepting it.

**`CTRL-218` form safety:** Later form adapters require recorded source permission, allowlisted adapter and minimum version, canonical employer/requisition identity, chosen observation, live destination, field map and question snapshot, current `VERIFIED_ELIGIBLE` assessment where needed plus current exact-context authorization answer, supported attachments and document digests, matching final bundle, appropriate mode, budgets, and no unresolved sensitive field or challenge. Unknown widget, changed form, CAPTCHA, MFA, permission restriction, failed login, suspicious redirect or contradictory confirmation pauses the item in `MANUAL_ACTION_REQUIRED` with a reason code (`01` `SM-104`, v1.0), provided no submit request can have left the product; otherwise `CTRL-219` uncertainty applies. Never solve or bypass a site challenge or falsely report submission. In Manual mode the user expressly submits; Hybrid requires `CMD-107` on the exact bundle; Auto only on explicitly allowed flows after all mandatory gates. MVP only permits package review and external handoff, with no in-app real-world submit.

**`CTRL-219` external-effect guard:** Before a later release crosses the final submit boundary, authority atomically reserves the `CON-141` application identity guard, verifies current lease (`CON-134`) and dependencies, records `EVT-108` with bundle and target digests, attempt ID, actor or policy authorization, timestamp and allowed effect, and persists the audit event. Only then may the scoped worker interact with the submit control once. Confirmation requires source-specific credible evidence or explicit manual attestation (`CON-129`); a click or page load is not confirmation. Lost response, partition, expired lease during effect, unexpected redirect, or browser crash transitions to `SUBMISSION_UNCERTAIN` and `EVT-110`, never an automatic retry. `03` specifies receipt evidence and scheduling. Later only.

**`CTRL-220` reconciliation:** Quarantine the identity guard during uncertainty. Inspect employer acknowledgement, candidate's account status, email received directly by the candidate, and captured permitted receipt metadata without creating another application. A named human records disposition through `CMD-110` with evidence and audit (`EVT-111`); if evidence is insufficient, uncertainty remains. An explicit, reviewed reapplication decision is necessary before another attempt. “Not found in inbox” alone does not prove no submission. Later only.

## 17. Approval Integrity, Replay Defense, Idempotency, and Offline Safety

The exact approval protocol under **`CTRL-206`** applies `CON-135` and `CON-136`: the signed-in user fetches the current bundle directly from the authority; server or local authority displays full destination, documents and answers; a step-up credential binds to actor and registered device; `CMD-107` includes bundle revision and digest, nonce, permitted decision, expected authority revision and idempotency key. The authority compare-and-sets one `PENDING` approval to exactly one terminal result and commits audit with it. An old nonce, expired session, wrong device, old bundle, conflicting decision or replay returns typed error (`ERR-106`, `ERR-107`) without granting effect. In local-only mode the same invariant is enforced by local authority. `CMD-108` is not shipped in MVP.

**`CTRL-208` push boundary:** Store only opaque notification locator and minimal generic text in push payload; lock-screen detail defaults hidden. Opening a push performs authenticated current-state fetch. Delivery, open and tap events record transport state (`CON-137`) but never call the approval transition. Push delays or duplicates do not alter the review queue. Later only.

Under **`CTRL-207`**, a saved mobile bundle is visibly stale with last authoritative sync and no enabled consequential command. A queued proposal may be shown as unpublished but cannot be replayed as approval. A stop button returns pending until authority acknowledges; unreachable worker may continue an in-flight action, which is shown as uncertain. Later only.

**`ADR-204`:** Use a durable internal idempotency result plus identity guard instead of relying on a short HTTP dedupe window. The result record lasts at least through the entity lifetime and submission-history lifetime as `ADR-103` specifies; new keys do not evade the unique guard. Exactly-once semantics stop at the authority boundary. There is no distributed transaction with an employer site.

## 18. Privacy, Consent, Data Minimization, and Third-Party Disclosures

**`PRIV-201` purpose separation:** Local preparation, optional selected sync, third-party model inference, external employer disclosure, optional diagnostics, and optional telemetry each have separately named purposes. Consent to one does not enable another. The user chooses fields before enrollment and sees provider identity, destination and data classes before first external model disclosure; consent can be changed for future processing without pretending already submitted data can be recalled. All telemetry is off by default (`NFR-07`). A privacy notice must explain operator and self-host responsibilities, backups and deletion limits. Canadian privacy guidance emphasizes meaningful consent and limiting collection, use, disclosure and retention; applicability to a deployment and other jurisdictions needs professional review, not a blanket compliance claim. [RES-214; RES-215; RES-216]

**`PRIV-202` default disclosure:** No raw evidence bytes, cookies, credentials, browser profiles, local filesystem grants, complete document bytes, screenshots or sensitive answers sync by default (`CON-143`, `OQ-101`). Selected assertion fields, revision and digest may sync after opt-in. A sufficient current assertion must be published for any shared consequential decision; if this cannot be done within the user's chosen disclosure, the action remains local-only or blocked. Explicit document sync needs separate consent and encrypted controlled storage. No model disclosure of eligibility or immigration facts by default unless a specific task truly requires it and the user enables that provider and class. `OQ-102` stays answered by exact-context re-verification until a new approved policy narrows it.

**`PRIV-203` third-party disclosure ledger:** Record provider or employer, purpose, class, fields or content digest, time, user choice or mode policy, retention terms version, and revocation/contact path without logging the raw payload. For a locally run model, log endpoint identity and local or network boundary. Audit exported packages and user-selected destinations as disclosures from app-managed protection. Later provider terms may change; re-evaluate before continued processing. Direct employer submission is a separate user effect, not consent for a model to receive all candidate data.

| Class and concrete data | Default store and sync | Model and telemetry rule | Export and backup treatment |
| --- | --- | --- | --- |
| `PUBLIC_SOURCE`: job title, permitted description, original and resolved URL, timestamp, source ID | Local observations; selected job metadata may sync; raw snapshot only if source policy permits. | Minimal description may go to chosen evaluated model; operational counts only in consented telemetry. | Export provenance if permitted; backups expire with record. |
| `CANDIDATE_PERSONAL`: contact, employment, education, resumes, verified claim text | Encrypted local store; selected assertion fields only by opt-in; documents local by default. | Task-minimal chosen provider by explicit disclosure; no default telemetry. | User-selected output may be plaintext with warning; protected backup. |
| `CANDIDATE_SENSITIVE`: residence, eligibility/immigration, demographic or legally consequential facts | Encrypted local store; selected sufficient assertions only after explicit sharing; no evidence bytes by default. | No default third-party model disclosure; explicit scoped consent and provider eligibility assessment. No telemetry. | Omit from ordinary export package; user-controlled comprehensive export and protected backup. |
| `SECRET`: API keys, cookies, tokens, worker credentials, DEK, destination grants | Protected secret store or isolated browser profile; never ordinary sync; server-side secrets in operator-managed key store. | Never to model or telemetry. | Exclude from data export and diagnostic bundle; separately encrypted key recovery where applicable; provider-side revocation on deletion. |
| `APPLICATION_CONFIDENTIAL`: exact answers, completed forms, screenshots, confirmation evidence | Encrypted local authoritative store; only selected exact bundle and minimal receipt metadata to shared authority when needed, never raw screenshots by default. | Answer interpretation only under explicit provider/class grant; no telemetry. | Default package omits exact answers and screenshots; optional user-controlled protected export. |
| `OPERATIONAL`: audit digests, stage, task health, safe error code, pseudonymous metric | Local audit; shared audit for synchronized transitions. | No model need; opt-in redacted telemetry only. | Explainable user export with sensitive identifiers protected; encrypted backups and minimal long-term history. |

## 19. Retention, Export, Deletion, and Replica Propagation

**`PRIV-204` proposed periods:** These are product defaults to validate with applicable law, source permissions, service terms, user choice and actual operational needs before hosted commercialization. “After trigger” starts when the record becomes inactive or the named event occurs. An unresolved uncertain submission, security incident, active user hold or legal obligation can extend only the necessary minimal records with documented reason, review date and restricted access. Do not silently promise to erase employer-held copies or already-sent model inputs.

| Data | Proposed active period and trigger | Deletion or exception |
| --- | --- | --- |
| Profile, claims, resumes, documents, output packages | While account or local profile active; on deletion request begin purge within 30 days of authority processing. | Retain minimal hashes and transition evidence only if needed for unresolved application or lawful obligation; user-selected copies require user action. |
| Permitted public posting snapshot | While relevant; 30 days after posting removal or 90 days after last use, whichever comes first, unless source demands earlier purge. | Keep minimal ID, URL, content digest and observation time for duplicate and provenance history where lawful. |
| Raw HTML, temporary downloads and extraction files | Delete within 24 hours after successful processing; failed/quarantined item within 7 days unless incident hold. | Never include raw content in telemetry. |
| Browser site cookies and profile | While user has an active supported site session; delete on site disconnect or account deletion, and offer immediate local wipe. | Site may still have server session; request provider-side logout or revoke where available. |
| Debug screenshots or captured form HTML | Off by default; if essential, encrypted with explicit reason and erase within 7 days after closure. | Incident hold requires specific approval, access log and review date; redact before support sharing. |
| Proposed answers and completed form copy | Keep only while review or active application needs it; delete raw copy 90 days after final outcome or account deletion, subject to user hold. | Retain audit-minimal answer digest, exact question identity and consent evidence if needed for a disputed submission; reconsider jurisdictions. |
| Safe operational logs | Rolling 30 days locally or hosted; security access events proposed 90 days. | Redacted security incident excerpts under time-bounded hold; no raw credentials. |
| Submission and approval audit-minimal history | While application active; proposed 24 months after final outcome for duplicate and dispute evidence, then minimize further or delete. | Legal review may require a different period; profile deletion requests produce a specific exception report. |
| Encrypted backups | Proposed rolling 30 days local, 35 days hosted; verify restoration before use. | Expiry is asynchronous; deletion report states last backup expiry. Key destruction may render retained ciphertext inaccessible but is not a universal erasure guarantee. |

**`CTRL-221` deletion and export:** Provide machine-readable profile, claim, job, package, application, approval and audit-minimal export with provenance and schema version; provide available document bytes as separate files. An export requiring sensitive fields uses recent authentication and protected destination, excludes secrets and site sessions, and records its completion. On delete, authority creates versioned request and tombstones (`CON-145`); online replicas acknowledge, offline devices remain **pending**, revoked or retired devices are listed as **unreachable or removed without acknowledgement**. A stale replica must not resurrect deleted records on reconnect: it refreshes current tombstones and authoritative snapshot before mutation. Stop future sync/provider calls, delete local app-managed bytes and service copies where controlled, queue bounded backup expiry, and report third parties and user-selected destinations separately. Where audit-minimal history must remain, show its fields, purpose and end date. A compromised device cannot be remotely guaranteed wiped; revoke access and advise local wipe. MVP covers local export/deletion and backup limits, later sync adds tombstones and propagation.

## 20. Logging, Audit, Diagnostics, and Security Monitoring

**`CTRL-222` audit and diagnostic policy:** A consequential transition and its `CON-147` audit event share a transaction; include actor/system principal, device/worker, authority, old and new state, input revision digests, policy result, approval or application guard reference, causation, time and privacy class. Rejected cross-account, replay, stale, revoked, and unsupported-version attempts have safe security events even though state remains unchanged. Append-only or tamper-evident storage is a proposed mechanism; integrity detection and restore must be tested, and an operator with full storage control can still delete data. Default logs contain typed stage, duration, safe error and correlation ID, not full URLs with tokens, prompts, resumes, answers, screenshots, cookies or keys. Structured redaction happens before disk or telemetry; stack traces are scrubbed. A secret scanner covers diagnostics and crash artifacts. Alert on impossible device/worker identity changes, rapid approval failures, cross-account read denials, abnormal egress, source bursts, audit gaps, repeated uncertainty and deletion failures. Users see incident and source health without raw protected payloads.

**`PRIV-205` diagnostics consent:** Optional crash and usage telemetry begins off, is independently opt-in with preview and revocation, and uses a privacy-filtered channel. A support bundle requires a separate user export action, redaction preview and a precise time-limited share; no automatic screenshot upload. Where hosted operation requires abuse and account security logs, document the minimal necessary events separately from optional product telemetry. `03` defines aggregation and alerts; `06` explains settings.

## 21. Incident Response, Recovery, and Compromised Device or Worker Handling

**Common protocol `IR-201`:** Record detection time, affected realm/profile, severity, involved versions and authority revision. Freeze only affected capability or source when safe; freeze all submission-capable work if authority or signing integrity is uncertain. Preserve minimal attributable audit digests and permitted receipts in a restricted incident store with access log, expiration and no unnecessary screenshots. Rotate or revoke exposed credentials at their issuer, not only in the app. Review any `SUBMISSION_UNCERTAIN` identity guards before resumption. Decide user, employer/provider, operator or regulator notification based on actual disclosure and jurisdiction with professional review; do not assert a universal statutory deadline. Return to service only when root cause is contained, tests pass, replay and audit state are reconciled, and an authorized owner signs off.

| Playbook | Detection, immediate containment, revocation | Evidence and recovery | Notification decision; return criterion |
| --- | --- | --- | --- |
| `IR-202` lost device | User report or suspicious session; revoke `dev_`, sessions, pending decisions and worker enrollment if co-located; lock shared effects. | Preserve safe access history; restore from protected backup to new device, rotate local recovery material and site sessions if accessible. | Notify candidate and assess disclosure; return after new device registration and account audit. |
| `IR-203` compromised worker | Unexpected task, egress, process or receipt; quarantine `wrk_`, revoke task credentials and leases, freeze effects. | Retain hashes, task IDs and permitted site evidence; rebuild signed worker, rotate scoped keys, reconcile each possible effect. | Notify candidate and affected third party where required; return after clean enrollment, regression test and guard review. |
| `IR-204` exposed API key | Key in log, repo, screenshot or provider alert; disable provider path and revoke key at provider immediately. | Preserve redacted exposure path and usage times; replace through protected entry and review provider usage and bills. | Notify candidate if costs or data exposure; return after leak scanner clean and revoked key rejected. |
| `IR-205` stolen browser session | Unexpected employer activity or cookie exposure; stop site adapter, revoke site sessions where possible, wipe isolated profile. | Preserve minimal account and application receipt metadata; direct user sign-in, verify account and identity guards. | Notify candidate, perhaps employer on unauthorized submission; return after reauthentication and reconciled history. |
| `IR-206` unauthorized approval | Unrecognized `EVT-107` or forged session; revoke device/session and pending grants, freeze target effect. | Preserve bundle digest, nonce use and actor timeline; if effect happened, record correction and uncertainty as warranted. | Notify candidate promptly and external recipient if actual effect warrants; return after account recovery and guard reconciliation. |
| `IR-207` cross-user disclosure | Object access anomaly or report; disable affected endpoint or realm access, isolate keys and exports. | Preserve access metadata, determine fields, recipients, duration and downstream copies; fix object authorization and recheck accounts. | Jurisdiction-aware user and regulator assessment; return after account isolation test, remediation and review. |
| `IR-208` poisoned dependency or update | Signature, checksum, SBOM or behavior alert; halt rollout and revoke affected release channel. | Preserve binaries and metadata, roll back to verified signed build, rotate potentially accessed keys, check migrations and data integrity. | Notify users proportionate to exposure; return after provenance review and clean signed rollout. |
| `IR-209` duplicate or uncertain submission | Crash, partition, conflicting receipt or employer message; stop new attempts and hold identity guard. | Preserve `EVT-108`, `EVT-110`, target, permitted confirmation evidence; reconcile by `CMD-110` without another submit. | Inform candidate of uncertainty; return only after documented resolution or keep affected application blocked. |

## 22. Security Requirements by MVP and Later Release

| Gate | Mandatory controls and blocked capability |
| --- | --- |
| MVP, local Manual | `CTRL-201`, `CTRL-202`, `CTRL-209` to `CTRL-216`, `CTRL-221` to `CTRL-224` as applicable, local `CTRL-203`, source fetch `CTRL-217`, model transport `CTRL-226` (added v1.0 to match the section 22.1 index), model routes `CTRL-227` (added v1.1); secure setup, isolated preparation, verified claim and package, export/deletion, protected API key, safe logs, backup recovery. `CMD-108` and real-world form submit are unavailable. |
| Hosted or self-hosted synchronization and mobile | Complete `CTRL-203` to `CTRL-208`, `CTRL-211`, `CTRL-212`, `CTRL-221`, `CTRL-222`, remote sign-in and recovery `CTRL-225`, remote transport `CTRL-226` (last two added v1.0 to match the section 22.1 index); stage enrollment, single authority, authenticated roles, device and worker revocation, tombstones, push hint, stale mobile display. No automatic submission merely because sync exists. |
| Later assisted form and Hybrid | `CTRL-217` to `CTRL-220`, confirmed adapter permission and version, exact bundle step-up, challenge stop, durable receipt and uncertain-effect reconciliation; security review of each source and form context. |
| Later Auto and Continuous | All above, explicit allowlist and policy, complete answer and eligibility gate, worker lease and budgets (`CTRL-224`), abuse monitoring, operator incident drill, validated rate limits and recovery. |

**`CTRL-224` protective budgets:** Enforce per-source request, per-run and daily job, model token and cost, disk, hardware and later form/submission caps at authority and worker checkpoints (`CON-131`). Circuit-break on source restrictions, unexpected spikes, rate-limit signals and depleted funds. No “continuous” exception. MVP for source/model budgets, later for unattended runs.

### 22.1 Control enforcement and evidence index

This index makes the required safe behavior explicit for each control. “MVP” includes only the capabilities actually shipped in the Manual local vertical slice. Later controls block the feature they protect until proved.

| Control | Scope; enforcer; protected asset | Safe failure or degradation | Evidence; release |
| --- | --- | --- | --- |
| `CTRL-201` | Every ingestion, store and disclosure; authority and worker; classified data. | Uncertain class takes stricter rule; no disclosure on classification error. | Mixed-class fixtures and `AC-204`; MVP. |
| `CTRL-202` | Local IPC; desktop authority and worker; commands and task secrets. | Reject unauthenticated peer, close session. | `AC-201`; MVP. |
| `CTRL-203` | Enrollment and sync; local and remote authority; canonical revisions. | Leave offline edit unpublished, reject dual or stale authority. | `AC-206`, `AC-215`; local authority MVP, sync later. |
| `CTRL-204` | Reads and commands; control plane; account and profile isolation. | Deny and safe-audit foreign object. | `AC-210`; sync. |
| `CTRL-205` | Enrollment, task and effect; authority and worker; scoped task and credential. | Revoke lease and deny new effects; mark possibly started effect uncertain. | `AC-209`; local scope MVP, distributed later. |
| `CTRL-206` | Consequential commands; local or remote authority; claims, approvals, package and effect. | Transaction rejects stale, wrong-actor or unaudited mutation. | `AC-202`, `AC-216`; local subset MVP, remote later. |
| `CTRL-207` | Cached mobile and revocation; control plane and mobile; approval and stop status. | Disable offline decisions and label stop unacknowledged. | `AC-206`; mobile later. |
| `CTRL-208` | Push dispatch; control plane and mobile; private review information. | Delivery failure leaves authoritative review pending. | `AC-203`; mobile later. |
| `CTRL-209` | Local and server storage; key owner; encrypted personal data. | Missing key locks data and work, never stores unwrapped key as fallback. | `AC-207`, `AC-211`; local MVP, server later. |
| `CTRL-210` | Secret issue and use; protected store and worker; tokens, cookies, keys. | Missing or revoked secret pauses only dependent task. | `AC-208`, `AC-209`; provider key MVP, site sessions later. |
| `CTRL-211` | App-managed store and backups; desktop or operator; data and recovery. | Restore fails verification without promoting corrupt backup. | `AC-207`, `AC-211`; local MVP, hosted later. |
| `CTRL-212` | Worker and browser process; desktop and worker; site session and filesystem. | Sandbox or permission unavailable disables affected capability. | `AC-201`, `AC-204`; preparation MVP, browser later. |
| `CTRL-213` | Package export; worker and authority; document bytes and grant. | Partial or tampered manifest never becomes `COMPLETE`. | `AC-207`; MVP. |
| `CTRL-214` | File, HTML and repository ingest; worker parser; local files and code execution. | Malformed or dangerous input quarantined without further fetch. | `AC-204`; MVP. |
| `CTRL-215` | Worker-to-model call; policy and worker; candidate disclosures and cost. | Unapproved class or endpoint blocks model task. | `AC-204`, `AC-208`; MVP. |
| `CTRL-216` | Factual and answer output; authority validator; claim truth and form answers. | Unsupported fact or context invalidates output or bundle. | `AC-204`, `AC-216`; factual MVP, forms later. |
| `CTRL-217` | Source fetch and redirect; adapter and network boundary; origin and secrets. | Unknown origin or network target blocks request and records source health. | `AC-205`; permitted source fetch MVP, forms later. |
| `CTRL-218` | Employer form; authority and adapter; answer and application integrity. | Changed or unsupported form pauses item. | `AC-205`; later only. |
| `CTRL-219` | External submit; authority and worker; guarded employer effect. | No durable guard, lease or receipt means no new effect or explicit uncertainty. | `AC-214`; later only. |
| `CTRL-220` | Uncertain submit; authority and human reviewer; duplicate guard. | Unresolved outcome retains hold. | `AC-214`; later only. |
| `CTRL-221` | Export and deletion; local or shared authority and replica; data lifecycle. | Incomplete deletion reports pending, stale replica loses mutation rights. | `AC-215`; local export/deletion MVP, sync later. |
| `CTRL-222` | Audit and telemetry; authority and diagnostic pipeline; evidence and secrets. | Redaction failure blocks diagnostic upload, never blocks authoritative audit commit silently. | `AC-208`; MVP. |
| `CTRL-223` | Install and updates; desktop and release pipeline; executable integrity. | Invalid or downgraded release rejected, prior verified build retained. | `AC-212`; MVP release. |
| `CTRL-224` | Source, model and runtime budget; authority and worker; resources and site access. | Exhausted reservation pauses dependent action. | `AC-213`; MVP applicable limits, later Continuous. |
| `CTRL-225` | Remote sign-in, recovery and session; identity service; candidate account. | Failed step-up or recovery blocks sensitive and submission actions. | `AC-202`, `AC-210`; sync. |
| `CTRL-226` | Remote and local model transport; network client and local service; endpoint and payload. | Certificate or identity error blocks connection; never silently downgrades. | `AC-217`; model MVP, remote later. |
| `CTRL-227` | Model routes R1 and R2; worker, desktop, and policy; candidate data, local files, credentials. | Missing terms evidence keeps R1 off; an invalid reply is rejected without state change; a tool that requests a capability is terminated. | `AC-219`; R2 MVP, R1 when enabled. |

## 23. Verification Plan, Abuse Tests, and Acceptance Criteria

Use mock employer sites, fake accounts, synthetic candidate records, controlled model responses, virtual clock, proxy and filesystem fault injection. **Never submit a fake application to a real employer.** Every test records accepted/rejected command, state, audit event, disclosure and network destination. Differential tests must exercise both local and synchronized authority when the latter ships. Test fixtures contain no real user secrets.

| ID | Test and release acceptance | Owner |
| --- | --- | --- |
| `AC-201` | Second OS user and rogue local process cannot invoke local authority or steal a task through IPC; compromised worker result cannot verify a claim or accept approval. | `03`, `04`; MVP |
| `AC-202` | Two authenticated devices race exact approval: one accepted and audited; wrong digest, nonce replay, expired step-up and revoked device yield typed rejection; no external effect. | `03`, `05`; sync |
| `AC-203` | Spoofed, duplicated, delayed and tapped push produces no accepted approval; opening requires current authenticated bundle. | `05`; sync |
| `AC-204` | Hostile listing, README, resume, DOCX external relationship and model JSON extra command cannot exfiltrate a secret, access private network, promote an unsupported claim, or make an unapproved provider call. | `03`, `04`; MVP |
| `AC-205` | Malicious DNS/redirect, changed form or sensitive question pauses flow; only a verified allowed destination and exact current answer may proceed in mock ATS. | `03`; later |
| `AC-206` | Offline synced claim edit and mobile decision remain proposal/read-only; reconnection resolves conflict without dual authority; stale approval is rejected. | `03`, `05`; sync |
| `AC-207` | Stolen locked device cannot read app-managed encrypted data; revoked destination prevents package completion; user-selected plaintext export is marked and tested; lost key without recovery is unrecoverable as documented. | `04`; MVP |
| `AC-208` | Inject API keys, cookies and sensitive answer strings into error paths, logs, screenshots and support preview; none appear in default diagnostics or telemetry. Screenshot capture defaults off and expires on schedule. | `03`, `04`; MVP |
| `AC-209` | Worker with wrong realm, revoked key, expired lease or unsupported capability gets no task or new effect. During external boundary loss, mark uncertain. | `03`; sync/later |
| `AC-210` | In two synthetic accounts, enumerate and mutate foreign IDs across all query/command surfaces and worker claims; no cross-account disclosure, and denial is audit-safe. | `03`; sync |
| `AC-211` | Encrypt, restore and verify a local backup; rotate wrapping and data keys with crash injection; old credentials fail after retirement; hosted backup recovery and owner access tested when relevant. | `03`, `04`; MVP/later |
| `AC-212` | Modified, unsigned or downgraded update rejected; known-good signed rollback preserves interpretable audit and data after migration failure. | `04`, `07`; MVP release |
| `AC-213` | Continuous fixture exhausts each source/model/storage cap, pauses dependent task and issues no further request or cost-bearing call. | `03`; applicable release |
| `AC-214` | Mock submit loses receipt after effect or lease expires; `SUBMISSION_UNCERTAIN`, durable guard and `EVT-110` survive restart; neither same nor new idempotency key retries without explicit evidenced `CMD-110`. | `03`; later |
| `AC-215` | Synced deletion creates tombstone; online replica acknowledges, offline/compromised/retired device remains reported pending or unreachable, and reconnect cannot resurrect bytes or authority. Backup-expiry report is accurate. | `03`, `05`; sync |
| `AC-216` | Claim withdrawal or expiry invalidates dependent document/package and unused approval, and blocks next effect; historical confirmed submission remains an auditable fact. | `03`; MVP/later |
| `AC-217` | An expired certificate, wrong hostname, untrusted self-host certificate, TLS downgrade and unauthenticated network model endpoint each block connection; an authenticated local socket works only for its scoped peer. | `03`, `04`; model MVP, remote later |
| `AC-218` | On Pop!_OS, restart the keyring daemon mid-run and lock the collection: every Secret Service call returns within its timeout, only dependent tasks pause with an unlock action, no key is stored unwrapped, and work resumes after unlock. Repeat with no Secret Service provider: the passphrase fallback is offered (v1.0). | `04`, `03`; Linux compatibility gate (v1.1; was MVP in v1.0) |
| `AC-219` | Export a relay package and confirm it contains no secret and, by default, no sensitive-class field, and that the ledger records it. Paste replies containing an injected instruction, an extra `verified_by` field, and an unsupported claim: each is rejected. Configure R1 with a fake vendor tool that attempts a shell command, a file read, and a web fetch: each is blocked or the process is terminated, and no output is accepted from that run (v1.1). | `03`, `04`; R2 MVP, R1 when enabled |

Acceptance is based on observed state, audit and blocked outbound effects, not merely UI messages. Required negative tests run at every affected release gate; `07` places them in phase order. Fuzz URL and document parsers, validate renderer isolation on each supported OS, assess authenticated API with an independent review before hosted release, and perform tabletop `IR-202` to `IR-209` before later submission release. A failing P0 control blocks the feature.

## 24. Decisions, Assumptions, Residual Risks, and Open Questions

| ID | Decision or risk | Consequence |
| --- | --- | --- |
| `ADR-201` | Local random DEK wrapped by tested protected store or explicit passphrase fallback. | Linux unattended operation depends on tested secure store and user's unlock choice. |
| `ADR-202` | Digests prove only byte identity under specified canonicalization. | They never authorize disclosure or submission. |
| `ADR-203` | Minimized selected sync with service-readable fields, without unsupported operator-blind claim. | Operator trust and compromise remain disclosed risks. |
| `ADR-204` | Authority idempotency result plus durable application identity guard; uncertainty at employer boundary. | Some applications remain unresolved indefinitely. |
| `RISK-201` | Same-user malware on unlocked desktop can read application memory or call a permitted secret store. | OS hardening, key lock and scoped worker reduce exposure but cannot promise containment. |
| `RISK-202` | Employer site or model provider can retain disclosed data and change terms. | Review providers and permission per release; user sees actual recipients. |
| `RISK-203` | Suppressing screenshots reduces forensic visibility in uncertain submissions. | Keep default off, permit short-lived encrypted capture only for justified supported flows. |
| `RISK-204` | Self-host operator can misconfigure transport, backup and access policy. | Installation checks and clear status help but cannot guarantee operator practices. |
| `RISK-205` | After an external effect, revocation or rollback cannot erase the employer's record. | Correction and candidate notification replace false rollback claims. |

| ID | Question, default and decision owner |
| --- | --- |
| `OQ-201` | `OQ-101`: exact claim fields allowed to sync by default? Until approved, no evidence bytes and only user-selected necessary assertions. Product owner and privacy review before sync release. |
| `OQ-202` | `OQ-102`: may a verified sensitive answer be reused across contexts? Until approved, fresh verification of exact wording and context. Product owner and security review before form automation. |
| `OQ-203` | Which local key-store and unattended unlock guarantees actually hold on macOS, Windows and target Linux desktop? `04` prototypes, starting with the macOS reference (v1.1), then Pop!_OS with `AC-218`; product owner accepts usability tradeoff before platform claim. |
| `OQ-204` | Which privacy laws and employer, model and source retention obligations apply to each deployment and user location? Legal/privacy review before hosted commercialization; current periods are proposed defaults. |
| `OQ-205` | What receipt qualifies as confirmed employer submission for each adapter (`OQ-103`)? `03` source study; uncertainty until validated. |
| `OQ-206` | Which destination filesystems support durable commit and which user-selected targets are encrypted (`OQ-104`)? `04` validates; manifest invariant remains. |
| `OQ-207` | Resolved in v1.1: the reference machine is the product owner's MacBook Pro running macOS (`00` `OQ-01`, `CHG-011`), replacing the v1.0 Pop!_OS choice. Security signoff for the MVP uses macOS first. |

## 25. Requirements Traceability and Downstream Allocation

| Upstream requirement or contract | Threat | Control | Enforcing component | Release; verification | Downstream |
| --- | --- | --- | --- | --- | --- |
| `PRD-01`, `POL-07`, `NFR-07`, `ARCH-14`, `CON-111`, `CON-147`, `AC-01` | `THR-201`, `THR-214` | `CTRL-201`, `CTRL-209` to `CTRL-211`, `CTRL-221`, `CTRL-222` | Local authority, desktop, secret store | MVP; `AC-207`, `AC-208`, `AC-211` | `03`, `04`, `06`, `07` |
| `PRD-02`, `PRD-03`, `POL-01`, `POL-02`, `CON-106`, `CON-112` to `CON-115`, `SM-101`, `CMD-101`, `CMD-102`, `EVT-101`, `EVT-102`, `ERR-103`, `AC-03`, `AC-101` | `THR-203`, `THR-213`, `THR-217` | `CTRL-214` to `CTRL-216` | Worker proposes, local or shared authority accepts | MVP; `AC-204`, `AC-216` | `03`, `04`, `06`, `07` |
| `PRD-05`, `PRD-06`, `POL-15`, `CON-118` to `CON-120`, `ERR-112`, `AC-02`, `AC-102` | `THR-204`, `THR-212` | `CTRL-217`, `CTRL-224` | Worker and source policy authority | MVP limited sources; `AC-205`, `AC-213` | `03`, `07` |
| `PRD-08`, `CON-125` to `CON-127`, `SM-102`, `CMD-105`, `EVT-106`, `ERR-105`, `AC-04`, `AC-05`, `AC-105` | `THR-213`, `THR-214` | `CTRL-213`, `CTRL-216` | Worker and package authority | MVP; `AC-207`, `AC-216` | `03`, `04`, `06` |
| `PRD-09`, `POL-09` to `POL-11`, `POL-16`, `CON-129`, `CON-141`, `SM-104`, `CMD-108` to `CMD-110`, `EVT-108` to `EVT-111`, `ERR-108`, `ERR-109`, `AC-08`, `AC-109` | `THR-204`, `THR-215` | `CTRL-217` to `CTRL-220` | Shared or local authority and worker | Later; `AC-205`, `AC-214` | `03`, `06`, `07` |
| `PRD-10`, `PRD-11`, `POL-03` to `POL-05`, `POL-12`, `CON-130` to `CON-134`, `SM-105`, `CMD-106`, `AC-06`, `AC-07`, `AC-116` | `THR-202`, `THR-212` | `CTRL-205`, `CTRL-224` | Authority and worker | MVP limits, later advanced runs; `AC-209`, `AC-213` | `03`, `04`, `07` |
| `PRD-12`, `POL-06`, `ARCH-13`, `CON-135` to `CON-137`, `SM-103`, `CMD-107`, `CMD-112`, `EVT-107`, `EVT-112`, `ERR-106`, `ERR-107`, `AC-09`, `AC-10`, `AC-106`, `AC-107`, `AC-110` | `THR-206`, `THR-207` | `CTRL-203` to `CTRL-208` | Control plane or local authority, mobile view | Sync/later; `AC-202`, `AC-203`, `AC-206` | `03`, `05`, `06`, `07` |
| `PRD-13`, `POL-14`, `CON-138`, `CON-139`, `ARCH-11` | `THR-203`, `THR-210` | `CTRL-210`, `CTRL-215`, `CTRL-216` | Worker and provider policy | MVP; `AC-204`, `AC-208` | `03`, `04` |
| `ARCH-01`, `ARCH-07`, `ADR-105`, `CON-101`, `CON-143` to `CON-146`, `CMD-111`, `ERR-113`, `ERR-114`, `AC-112`, `AC-114` | `THR-207`, `THR-216` | `CTRL-203`, `CTRL-204`, `CTRL-221` | Local and synchronized authority | Later; `AC-206`, `AC-215` | `03`, `04`, `05`, `07` |
| `PRD-16`, `NFR-01`, `NFR-02`, `CON-140` to `CON-142`, `CON-147`, `AC-108`, `AC-109` | `THR-208`, `THR-215` | `CTRL-204`, `CTRL-206`, `CTRL-219`, `CTRL-222` | Control plane or local authority | Applicable release; `AC-202`, `AC-210`, `AC-214` | `03`, `07` |
| `NFR-08`, `EXP-01`, `POL-07` | `THR-202`, `THR-211`, `THR-217` | `CTRL-202`, `CTRL-212`, `CTRL-214`, `CTRL-223` | Desktop installer and worker | MVP platform gate; `AC-201`, `AC-212` | `03`, `04`, `07` |
| `POL-17`, `PRD-13`, `01` `CON-138`, `CON-153` | `THR-218` | `CTRL-215`, `CTRL-216`, `CTRL-227`, `PRIV-203` | Worker, desktop and provider policy | R2 MVP, R1 when enabled; `AC-219` | `03`, `06`, `07` |

Runtime scheduling, queues, receipts and source permissions go to `03`; OS credential stores, IPC, packaging and update proofs to `04`; mobile authentication and offline/push behavior to `05`; disclosure, stale state and exact review UI to `06`; test gates and release ordering to `07`. This table points to representative tests, while sections 9 and 23 retain the complete threat coverage.

## 26. Completeness and Contradiction Audit

The six inherited data classes each have storage, synchronization, model, telemetry, export and backup rules in sections 18 and 19; period and deletion triggers are explicit proposals. Every drawn boundary maps to a control and an acceptance test in section 7. Claim verification, package commit, approval, application attempt, stop, device revocation and sync enrollment have named authorizer and transactional audit, with `CMD-108` absent from the MVP. Local-only use works without an account or control-plane network. A synchronized published revision has exactly one accepting authority. The worker neither verifies candidate facts nor accepts an approval. Offline mobile cannot authorize a consequence. Submission uncertainty keeps the application identity guard and blocks retry. Inherited states and wire fields are referenced without amendment; the v1.0 `01` additions (`MANUAL_ACTION_REQUIRED`, `CON-148`, `CON-151`) are applied in `CTRL-213` and `CTRL-218` and create no new trust boundary. The `00`/`01` draft labels are replaced by approved version 1.0 of both documents; `OQ-101` and `OQ-102` are not assumed resolved. No security claim here grants permission to scrape, bypass a challenge, infer work authorization, expose a local model to the internet, or promise cryptographic protection against a fully compromised unlocked host.

### Research register

Consulted 2026-09-24. Primary references support bounded platform and standards facts, while retention periods, token lifetimes and architecture choices are proposed requirements. NIST SP 800-63-4 on authenticator lifecycle and session management [RES-201; RES-202]; OWASP password storage, SSRF and TLS guidance [RES-203; RES-213; RES-210]; Apple Keychain, Microsoft DPAPI and freedesktop Secret Service documentation [RES-204; RES-205; RES-208]; OWASP LLM prompt-injection guidance [RES-211]; Office of the Privacy Commissioner of Canada privacy principles and consent guidance [RES-214; RES-215]. Jurisdictional coverage, individual provider terms and each job source's automation permissions remain release-specific investigations.

v1.0 citation repair: version 0.1 cited sources through chat-session markers that did not resolve to any URL. Each marker has been replaced with a reference ID. Each URL below is the official page supporting the stated claim, verified on 2026-09-27. The 0.1 research session may have used different pages on the same sites; the claims were rechecked against these pages.

| ID | Source | URL |
| --- | --- | --- |
| RES-201 | NIST SP 800-63-4, Digital Identity Guidelines | https://pages.nist.gov/800-63-4/ |
| RES-202 | NIST SP 800-63B-4, Authentication and Authenticator Management (final) | https://csrc.nist.gov/pubs/sp/800/63/b/4/final |
| RES-203 | OWASP Password Storage Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html |
| RES-204 | Apple Developer, Keychain services | https://developer.apple.com/documentation/security/keychain-services |
| RES-205 | Microsoft Learn, `CryptProtectData` (DPAPI): by default only the same logon credential on the same computer can decrypt | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata |
| RES-206 | Microsoft Learn, "How to use data protection" (.NET `ProtectedData`, current-user scope) | https://learn.microsoft.com/en-us/dotnet/standard/security/how-to-use-data-protection |
| RES-207 | GNOME, libsecret project page | https://wiki.gnome.org/Projects/Libsecret |
| RES-208 | freedesktop.org, Secret Service API specification | https://specifications.freedesktop.org/secret-service/latest-single/ |
| RES-209 | pop-os/cosmic-epoch issue 3453, libsecret clients hang after keyring daemon restart on COSMIC (open as of 2026-09-27) | https://github.com/pop-os/cosmic-epoch/issues/3453 |
| RES-210 | OWASP Transport Layer Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html |
| RES-211 | OWASP GenAI Security Project, LLM01:2025 Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| RES-212 | OWASP GenAI Security Project, LLM02:2025 Sensitive Information Disclosure | https://genai.owasp.org/llmrisk/llm02-insecure-output-handling/ |
| RES-213 | OWASP Server Side Request Forgery Prevention Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html |
| RES-214 | Office of the Privacy Commissioner of Canada, PIPEDA fair information principles | https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/ |
| RES-215 | Office of the Privacy Commissioner of Canada, Guidelines for obtaining meaningful consent | https://www.priv.gc.ca/en/privacy-topics/privacy-for-businesses/appropriate-handling-of-personal-information/collecting-personal-information-and-consent/consent/gl_omc_201805/ |
| RES-216 | Office of the Privacy Commissioner of Canada, Principle 5: Limiting Use, Disclosure, and Retention | https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/p_principle/principles/p_use/ |

## 27. Version 1.0 Change Record and Approval

Version 1.0 results from the 2026-09-27 gap audit of `00`, `01`, and `02`, run before `03` was drafted. The product owner instructed that the documents be treated as unapproved until the gaps were fixed, and approved them once fixed. No identifier was removed or renumbered, and no line of version 0.1 was deleted. The table lists modified content; all other changes are additions.

| Change | Old state | New state | Sections | Downstream effect |
| --- | --- | --- | --- | --- |
| `CHG-201` | Version 0.1, "Proposed security baseline"; `00` and `01` called approved "despite stale internal draft labels" | Version 1.0, approved; `00` and `01` at approved v1.0 | 1, 3, 26 | Binding for `03` to `07` |
| `CHG-202` | 11 citations were chat-session markers with no URL | Reference IDs `RES-201` to `RES-216` with verified URLs | 10, 12, 13, 15, 16, 18, research register | None; claims unchanged |
| `CHG-203` | Reference hardware open (`SEC-A-201`, `OQ-207`) | Pop!_OS reference; `SEC-A-205`; Secret Service timeout and fallback rule; `AC-218`; `OQ-203` starts on Pop!_OS | 4, 12, 23, 24 | `04` proves Linux key storage first |
| `CHG-204` | Release gate table omitted `CTRL-226` from MVP and `CTRL-225`, `CTRL-226` from sync, contradicting the section 22.1 index | Gate rows corrected | 22 | `07` gates |
| `CHG-205` | `THR-210` and the worker/model boundary did not cite `AC-217` | Cited | 7, 9 | None |
| `CHG-206` | No explicit mapping of the Generator threat list | Section 9.1 | 9.1 | None |
| `CHG-207` | `CTRL-213`, `CTRL-218` referenced `01` v0.1 contracts only | Reference `CON-148` and the `MANUAL_ACTION_REQUIRED` state | 14, 16, 26 | `03` adapter behavior |

Approval: with these changes the audit found no remaining gap in `02` that blocks `03`. Items that stay open by design (`OQ-201` to `OQ-206`, `SEC-CF-205`) each name an owner and the phase before which they must be decided. The product owner's approval of the fixed package, given in advance on 2026-09-27, makes this version binding.

### 27.1 Version 1.1 changes (2026-09-28)

| Change | Old state (v1.0) | New state (v1.1) | Sections | Downstream effect |
| --- | --- | --- | --- | --- |
| `CHG-208` | Pop!_OS reference; `AC-218` an MVP check | macOS reference (`00` `CHG-011`); Keychain is the MVP key path; Linux rows, `SEC-A-205`, and `AC-218` move to the Linux compatibility gate; `OQ-203`, `OQ-207` updated | 1, 4, 12, 23, 24 | `04` proves Keychain first |
| `CHG-209` | No controls for subscription developer tools or manual relay | `THR-218`, `CTRL-227`, `AC-219`; MVP gate and control index updated | 9, 15, 22, 22.1, 23 | `03` implements tool sandboxing and relay export; `06` designs the disclosure preview |

No identifier was removed, and no line of version 1.0 was deleted. The product owner approved version 1.1 on 2026-09-28.

## 28. Version 1.2: Hardened Isolation and Confidentiality Baseline (2026-09-29)

### 28.1 Direction and scope

On 2026-09-29 the product owner set security as the product's first priority, for personal use as much as for any later public release: the owner's own documents and data must not leak even if the app is never published. The owner instructed that the documentation be revised to the strongest practical baseline. This section records that revision. It adds threats, controls, decisions, tests, and gates; it removes no identifier and deletes no line of version 1.1. Where this section and an earlier section of this document disagree, this section governs, and the earlier text is read as superseded to the extent stated in section 28.9.

The revision rests on one reassessment. Version 1.1 treated a compromised worker as "conditional" (`THR-202`, `THR-217`). That is no longer defensible for a product that ingests public job postings automatically: anyone can place a crafted posting on an aggregator or an employer's board, the product fetches and parses it without a human choosing it, and the reward (resumes, eligibility and immigration facts, application answers, later the user's job-site sessions) is valuable. A parser or renderer compromise is therefore **credible**, and with a single worker process that holds network access and runs as the user, its impact is every file the user can read and any host on the internet. The response is structural: split the worker so that no process that touches untrusted bytes can both reach the user's data and reach the network, and enforce the split with the operating system's own sandbox, not with the worker's code.

### 28.2 New and re-rated threats

| Threat, priority | Asset; adversary; entry and path | Impact and plausibility | Controls | Test |
| --- | --- | --- | --- | --- |
| `THR-219` P0 | User files, keys, and product data; attacker who seeds a crafted posting, HTML page, PDF, or DOCX into a source the product reads, or a crafted relay reply; exploit in a parser, sanitizer, or renderer gives code execution in a worker process | Critical; credible because ingestion is automatic and the content is attacker-controlled | `CTRL-228`, `CTRL-229`, `CTRL-231`, `CTRL-214` | `AC-220`, `AC-221`, `AC-224` |
| `THR-220` P0 | Any data a compromised role can read; exfiltration over the network | Critical; credible once `THR-219` succeeds in a process with network access | `CTRL-229`, `CTRL-230`, `CTRL-233` | `AC-221`, `AC-222` |
| `THR-221` P0 | Every installation; theft of the update-signing or code-signing key from the release machine; a malicious signed update | Critical; conditional on release machine compromise, but one success reaches all users | `CTRL-223`, `CTRL-234` | `AC-227` |
| `THR-222` P0 (later) | Synchronized candidate data; hosted or self-hosted operator compromise, database leak, or insider | Critical; conditional, but a single breach discloses every account | `CTRL-237`, `ADR-205` | `AC-228` |
| `THR-223` P1 | Plaintext intermediate files (fetched pages, extracted text, rendered drafts) left in staging, temporary directories, backups, or indexes | High; credible because intermediate files outlive their purpose and are copied by OS backup and indexing | `CTRL-231` | `AC-223` |
| `THR-224` P1 | The desktop's trusted core; a flaw in the webview-to-core IPC path or in the core's OS integration | High; conditional on a webview script-execution flaw plus a core flaw | `04` `ADR-403`, `CTRL-202`, `CTRL-235`; residual `RISK-206` | `04` `AC-405`, `AC-406` |
| `THR-225` P0 (later) | User's job-site sessions and the host; malicious employer page attacks the automation browser | Critical; credible when browser automation ships | `CTRL-238`, `CTRL-212` | `AC-229` |

Re-rated: `THR-202` and `THR-217` move from "conditional" to "credible" for plausibility. Their priority stays P0; the new controls below are the mitigation.

### 28.3 New controls

**`CTRL-228` Role isolation (mandatory, MVP included).** The worker component of `00` `ARCH-02` is implemented as separate processes, one per role, each confined by an operating-system sandbox that grants only that role's resources. A role that cannot be confined does not start; its capability is unavailable and the reason is shown. There is no unconfined fallback. This supersedes `SEC-A-203`'s "capabilities narrow" wording with a stricter rule: the capability is off.

| Role | Handles untrusted bytes | Network | Filesystem | Secrets | Lifetime |
| --- | --- | --- | --- | --- | --- |
| `authority` | No (validates structured data only) | None | Its own data container | Database key and backup key, in memory | Session |
| `fetch` (source adapters and model clients) | Yes, raw responses | None directly; only through `egress` | None beyond a private temporary directory | None; provider keys are injected by `egress` (`CTRL-230`) | Session |
| `parse` (evidence files, posting HTML, relay replies before validation) | Yes, the most exposed role | None | None beyond a private temporary directory | None | Recycled after every task |
| `render` (PDF and DOCX rendering and validation of generated documents) | Only product-generated structured content | None | None beyond a private temporary directory | None | Recycled after every package |
| `write` (package commit) | No | None | Only the one destination folder, received as an open directory handle | None | Per commit |
| `egress` (the only network client) | Transports bytes; parses only HTTP framing and TLS | Only hosts named in the current task ticket (`CTRL-229`) | None | Provider keys, in memory, per request | Session |
| `browser` (later) | Yes, live employer pages | Only the verified employer domain, through `egress` policy | Its own profile store inside a VM | Site sessions inside the VM | Per site task (`CTRL-238`) |
| `model-local` (later, R4) | Model output | Loopback to its managed runtime only | Model files, read-only | Local endpoint token | Session |

The supervisor (the desktop core in local mode, `04`) holds no role's privileges beyond what it needs to start them and pass them handles. Mechanisms: App Sandbox for each role as an XPC service on macOS; AppContainer or LPAC on Windows; bubblewrap, Landlock, seccomp, and a network namespace on Linux, or Flatpak sub-sandboxes. `03` and `04` specify them.

**`CTRL-229` Egress brokering.** Only the `egress` role has a network socket. Every outbound request from `fetch` or `model-local` goes to `egress` with a task ticket issued by the authority: task ID, fencing token, allowed hosts and methods, byte and request budgets, and expiry, authenticated with a key shared only between the authority and `egress` at start. `egress` performs DNS resolution, the private-address and redirect rules of `CTRL-217`, TLS verification (`CTRL-226`), size and time limits, and rate limits, and it refuses any host not in the ticket. A compromised `fetch` process can therefore talk only to the hosts its current task is allowed to reach, and a compromised `parse` or `render` process cannot talk to anything.

**`CTRL-230` Secret injection at the broker.** Provider API keys (R3) and later local endpoint tokens are supplied by the supervisor to `egress`, bound to a ticket, and added by `egress` to requests for that provider's host only. They never enter the `fetch` role's memory, a task input, or a log.

**`CTRL-231` No plaintext at rest outside the chosen destination.** Fetched responses, extracted text, rendered drafts, and relay replies travel between roles in memory or as encrypted blobs held by the authority (`03` section 8.5). No role keeps a plaintext staging area. The only plaintext the product writes to disk is the committed package in the user's chosen destination and exports the user requests (both already disclosed under `CTRL-211`). Private temporary directories are wiped when a role is recycled and are excluded from backups and indexing.

**`CTRL-232` Hardware-backed key protection.** The database key is wrapped by a non-exportable hardware key when the platform provides one to the product: the Secure Enclave on macOS, a TPM through the platform crypto provider on Windows, TPM 2.0 on Linux where present. Unwrapping can be gated on user presence (Touch ID or Windows Hello), on by default at launch. The recovery material of `CTRL-209` remains mandatory because a hardware key dies with its device. Where hardware protection is unavailable (for example, a signing tier that the platform does not allow to use it), `ADR-201`'s OS key store applies and the product shows "hardware key protection unavailable" in its security status.

**`CTRL-233` Pre-connected IPC only.** No product process exposes a filesystem socket, named pipe name, or listening port that another process can connect to. The supervisor creates connected socket pairs (or the platform equivalent) and hands each role its ends at start; the authority serves those connections directly. Bearer credentials and principal binding still apply to each connection (`CTRL-202`). This removes the local attack surface of a discoverable endpoint.

**`CTRL-234` Release key protection.** The update-signing key and code-signing identities are never stored as plaintext files. On the owner's release machine they are encrypted to a hardware-bound key (a Secure Enclave-backed key, for example through `age-plugin-se` [RES-217], or a hardware security token when one is bought), unlocked only for a release, with an encrypted offline backup and a documented rotation procedure. Release builds are reproducible and published with their SBOM and checksums.

**`CTRL-235` Continuous adversarial testing.** Every release runs: a simulated-compromise suite in which each role executes hostile test code and must fail to read planted canary files, reach forbidden hosts, or open forbidden sockets (`AC-220`, `AC-221`); continuous fuzzing of the PDF, DOCX, and HTML ingestion paths; dependency vulnerability scans for Rust, Python, and npm; secret scanning; and static analysis. A failing case blocks the release.

**`CTRL-236` Independent review gate.** Before any build is used by anyone other than the owner, before any Hybrid or Auto phase, and before browser automation ships: an independent security review of the isolation design and a penetration test of the release candidate, and a published vulnerability disclosure policy.

**`CTRL-237` End-to-end encryption of synchronized sensitive content (later).** See `ADR-205`.

**`CTRL-238` Browser automation isolation (later).** The automation browser runs inside a lightweight virtual machine per worker host, with its own encrypted profile store and no access to the host filesystem beyond a single exchange directory for the files a task needs; its network follows `egress` policy for the task's verified employer domain. This strengthens `CTRL-212` for the component that renders hostile live pages.

### 28.4 Decisions

**`ADR-205` End-to-end encryption for synchronized sensitive content.** Context: `ADR-203` chose service-readable synchronized fields and disclosed operator trust as a risk. The owner's security priority makes that risk unacceptable for candidate data. Decision: for the classes `CANDIDATE_PERSONAL`, `CANDIDATE_SENSITIVE`, and `APPLICATION_CONFIDENTIAL`, synchronized payloads are encrypted on the user's devices with keys the control plane never holds. Each device has a device key pair protected by `CTRL-232`; an account content key is wrapped for each registered device and for a user-held recovery key. The control plane stores ciphertext plus the `OPERATIONAL` metadata it needs to order transitions (entity IDs, revisions, states, digests, timestamps). Consequences: (1) the control plane can no longer validate content (claim grounding, eligibility, bundle contents); those checks run on the user's device authority before a command is submitted, and consequential commands carry a signature by the registered device key that the control plane verifies (`03` section 33.10); (2) adding a device requires an existing device or the recovery key; (3) losing every device and the recovery key loses the synchronized content; (4) the mobile companion (`05`) needs its own device key to display review bundles; (5) server-side search over content is not available. `ADR-203` is superseded for these classes; it still describes `OPERATIONAL` data. The detailed protocol is designed and independently reviewed before the synchronization phase (`OQ-208`).

**`ADR-206` Isolation is a release gate, not an optimization.** No release, including the owner's personal MVP build, ships a role that handles untrusted bytes outside its OS sandbox (`CTRL-228`). If a platform cannot provide the sandbox, that platform does not get the capability.

### 28.5 Assumptions

`SEC-A-206`: the operating-system sandboxes named in `CTRL-228` enforce their documented restrictions; kernel or sandbox escapes are residual risk (`RISK-208`). `SEC-A-202` still holds: a same-user attacker already running arbitrary code outside the product is not contained by these controls.

### 28.6 Release gates, revised

| Gate | Added mandatory controls |
| --- | --- |
| MVP, local Manual (owner's personal use) | `CTRL-228` to `CTRL-235`; `CTRL-232` where the signing tier allows it, else the visible fallback |
| Any use by another person | Everything above plus `CTRL-236` and a distributable, notarized or equivalently signed build (`04` tier T2) |
| Synchronization and mobile | `CTRL-237` (`ADR-205`) in addition to the version 1.1 sync gate |
| Browser automation, Hybrid, Auto | `CTRL-238` and a fresh `CTRL-236` review |

### 28.7 Acceptance criteria

| ID | Test and release acceptance | Owner |
| --- | --- | --- |
| `AC-220` | In each role, a test-build hook runs hostile code that tries to read canary files planted in the user's home folder, in the authority's data, and in another role's temporary directory; every attempt fails and is recorded. | `03`, `04`; MVP |
| `AC-221` | The same hook in `parse`, `render`, `write`, and `authority` cannot open any network connection; in `fetch` it can reach only `egress`; `egress` refuses a host outside the ticket, an expired ticket, a ticket with a wrong fencing token, and a forged ticket. | `03`, `04`; MVP |
| `AC-222` | With R3 enabled, the provider key never appears in the `fetch` role's inputs, memory snapshot (test build), or logs; requests from `fetch` to a non-provider host never carry it. | `03`, `04`; MVP when R3 is used |
| `AC-223` | After a full pipeline run with canary strings in the evidence and the posting, a scan of every product data, temporary, cache, and log location finds the canaries only inside the encrypted database and blob store (as ciphertext, so not found) and in the committed package in the destination. | `03`, `04`; MVP |
| `AC-224` | Removing a role's sandbox configuration in a test build makes that role refuse to start and the capability show as unavailable; nothing runs it unconfined. | `04`; MVP |
| `AC-225` | While the product runs, no product process has a listening TCP socket, a bound filesystem socket, or a named endpoint that another process can open. | `03`, `04`; MVP |
| `AC-226` | Where `CTRL-232` is active, copying the product's data and key store items to another machine does not allow the database to be opened; with user presence on, launch requires Touch ID or the password. | `04`; MVP where available |
| `AC-227` | No update-signing or code-signing private key exists as a plaintext file on the release machine or in any repository; a release requires the hardware-bound unlock. | `04`, `07`; MVP release |
| `AC-228` | A full dump of the control-plane database contains no plaintext value of the three protected classes. | `03`; sync (later) |
| `AC-229` | Hostile page fixtures in the automation browser cannot read the host's home folder or reach hosts outside the task's policy. | `03`; browser phase (later) |

### 28.8 Residual risks

| ID | Risk | Mitigation |
| --- | --- | --- |
| `RISK-206` | The desktop core is the trusted base: it holds the key-store access and supervises the roles, and it is not itself sandboxed (it must replace its own bundle for updates and supervise the roles) | Minimal Rust core, no parsing of untrusted bytes, webview content rendered by the OS's own sandboxed web process, command allowlist (`04` `ADR-403`), hardened runtime, `CTRL-235` testing |
| `RISK-207` | Same-user malware already on the machine | Out of the product's power to contain (`SEC-A-202`); hardware-backed keys and user-presence gating reduce what it can take silently |
| `RISK-208` | Sandbox or kernel escape in the OS | Timely OS updates; `CTRL-236` review; defense in depth: an escape from `parse` still has no key and no network |
| `RISK-209` | The owner's free signing tier limits hardware key use and forbids distribution (`04` section 30) | Visible fallback; `CTRL-236` gate before any other user |
| `RISK-210` | Plaintext leaves protection by the user's own choice: committed packages in the destination and relay packages pasted into a chat service | Disclosure preview and ledger (`PRIV-203`), destination protection status (`04` section 10.6), minimization of relay content (`CTRL-227`) |

### 28.9 Superseded or refined text

| Earlier text | Now |
| --- | --- |
| `SEC-A-203`: capabilities "narrow" where OS enforcement cannot be shown | The capability is unavailable (`CTRL-228`, `ADR-206`) |
| `CTRL-212`: "a separately packaged worker" with least permission "feasible" | Per-role OS sandboxes are mandatory (`CTRL-228`) |
| `CTRL-217`: validation performed by the worker's client | Performed by `egress` (`CTRL-229`); the rules are unchanged |
| `CTRL-210`: the worker receives a short-lived handle just before use | For provider keys, `egress` receives the key and the worker never does (`CTRL-230`) |
| `CTRL-202`: an unguessable local channel credential with socket or pipe permissions | Pre-connected channels with no discoverable endpoint, plus the credential (`CTRL-233`) |
| `ADR-203` | Superseded for the three protected classes by `ADR-205` |
| `THR-202`, `THR-217` plausibility "conditional" | "Credible" (section 28.2) |
| Section 1 Authority row names `00` and `01` v1.0 | Corrected to the current versions (`03` `RT-CF-303`) |

### 28.10 Open question

| ID | Question | Owner and decision point |
| --- | --- | --- |
| `OQ-208` | Detailed end-to-end encryption protocol for sync: key hierarchy, device enrollment, recovery key format, rotation after device loss, and which metadata the control plane may see | `03` and `05` with an independent review, before the synchronization phase |

### 28.11 Research added

| ID | Source | URL | Supports |
| --- | --- | --- | --- |
| `RES-217` | age-plugin-se, Secure Enclave-bound keys usable only on the Mac that created them | https://github.com/remko/age-plugin-se | `CTRL-234` |
| `RES-218` | Apple, Creating XPC Services (each service has its own sandbox; launchd manages the lifecycle) | https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingXPCServices.html | `CTRL-228` |

### 28.12 Version 1.2 change record

| Change | Old state (v1.1) | New state (v1.2) | Sections | Downstream effect |
| --- | --- | --- | --- | --- |
| `CHG-210` | Single worker process; OS enforcement "where feasible"; compromised worker rated conditional | Mandatory per-role OS sandboxes, egress broker, broker-side secret injection, no plaintext intermediates, pre-connected IPC, hardware-backed keys, release key protection, adversarial testing, independent review gate; `THR-219` to `THR-225`; `CTRL-228` to `CTRL-238`; `AC-220` to `AC-229` | 28 | `03` section 33, `04` section 31, `07` gates |
| `CHG-211` | `ADR-203`: service-readable synced fields | `ADR-205`: end-to-end encryption for the three protected classes; `OQ-208` | 28.4 | `01` section 29.2, `03` section 33.10, `05` |
| `CHG-212` | Section 1 Authority row cited `00` and `01` v1.0 | Cites `00` v1.2 and `01` v1.2 | 1 | None |

No identifier was removed and no line of version 1.1 was deleted; two rows of section 1 (Version and Status, Authority) were updated in place. The product owner directed these changes on 2026-09-29 and reviews the text for approval.

## 29. Version 1.3: Independent Audit Fixes and Approval (2026-09-29)

### 29.1 Audit record and scope

On 2026-09-29 an independent reviewer (a separate model instance that had not written the documents) audited `00` v1.2, `01` v1.2, `02` v1.2, `03` v1.1, and `04` v0.3 against the owner's goal: no known security gap in the MVP, and a product the owner can use efficiently every day. The audit found 0 Critical, 7 High, 12 Medium, and 5 Low findings (`F-01` to `F-24`). The owner instructed that every gap be fixed and the package approved. This section records the security side of the fixes; `03` section 34, `04` section 32, `01` section 29.3, and `00` section 42.3 record the rest. No identifier was removed and no line of version 1.2 was deleted. Where this section and an earlier section disagree, this section governs to the extent stated in section 29.12.

Five platform facts the audit could not confirm from a primary source remain unverified after this revision's research: whether an inherited directory descriptor lets an App-Sandboxed process create entries inside it (`F-01`), the lifetime and launch behavior of free-tier provisioning profiles (`F-07`), whether one XPC bundle can run as several simultaneous instances (`F-14`), which hardened-runtime entitlements the pinned native Python wheels need (`F-17`), and whether each rendering and parsing library can work entirely on in-memory bytes (`F-11`). Every fix below is written to be safe whichever way those facts fall: the design either stops depending on the fact or names the experiment that decides and the outcome for each result.

| Finding | Severity | Fix (this document) | Fix elsewhere |
| --- | --- | --- | --- |
| `F-01` destination writes from a sandboxed `write` role unproven | High | `CTRL-239` (no `write` role; the core commits opaque bytes) | `03` `ADR-324`, `04` `ADR-421` |
| `F-02` backup key and plaintext recovery file bypass hardware protection | High | `CTRL-241` | `04` section 32.4 |
| `F-03` `fetch` parses hostile data and holds candidate data | High | `CTRL-239`, `ADR-208` | `03` `ADR-322`, `01` `CON-154` refinement |
| `F-04` fallback keeps network; `ADR-414` "still runs"; no runtime proof of confinement | High | `CTRL-240` | `04` `ADR-420` |
| `F-05` raw HTML and undefined members in the package | High | `CTRL-243` | `01` `CON-155` |
| `F-06` MVP not buildable as specified | High | `CTRL-235` MVP scope | `04` section 32.10 |
| `F-07` Secure Enclave may be unusable on the free tier | High | `ADR-207` | `04` `ADR-422`, `EXP-417` extended |
| `F-08` updater in the unsandboxed core | Medium | `CTRL-245` | `04` `ADR-423` |
| `F-09` lock pauses runs and adds prompts | Medium | `ADR-209` | `04` section 32.6 |
| `F-10` per-task recycling cost | Medium | `CTRL-239` lifetimes | `03` section 34.4 |
| `F-11` plaintext role temporary directories | Medium | `CTRL-231` exceptions (section 29.4) | `03` section 34.5 |
| `F-12` relay injection and chat-product context | Medium | `CTRL-244` | `03` section 34.3, `04` section 32.7 |
| `F-13` superseded text not listed | Medium | Section 29.12, section 29.9 | All documents |
| `F-14` XPC lifecycle, core dumps, resource limits | Medium | `CTRL-246` | `04` section 32.2 |
| `F-15` HTTP server on pre-connected sockets | Medium | `CTRL-233` refinement | `03` `ADR-323`, `01` `CON-157` |
| `F-16` FileVault and unsafe destinations only warned | Medium | `CTRL-242` | `04` section 32.5 |
| `F-17` entitlements of native wheels | Medium | `CTRL-246` | `04` `EXP-416` extended |
| `F-18` snapshot retention conflict | Medium | `CTRL-247` | `01` `CON-155`, `03` section 34.6 |
| `F-19` authority handling hostile-derived text; adapter split undefined | Medium | `ADR-208` | `03` `ADR-322`, section 34.3 |
| `F-20` invisible Unicode in directory names | Low | None | `01` section 29.3 |
| `F-21` Typst template injection | Low | `CTRL-248` | `03` section 34.5 |
| `F-22` clipboard residual | Low | `CTRL-249`, `RISK-214` | `04` section 32.7 |
| `F-23` read-back verified only by the writer | Low | None | `03` `ADR-324` |
| `F-24` relay as the only guaranteed route | Low | None | `00` `CHG-023` |

### 29.2 Revised role set

**`CTRL-239` Role set, version 1.3 (supersedes the `CTRL-228` table; `CTRL-228`'s rule is unchanged).** Roles are separated by the data class they may hold and by whether they touch network-facing or file-borne hostile bytes. No process that decodes hostile bytes can reach both candidate data and the network.

| Role | macOS bundle | Decodes hostile bytes | Data it may hold | Network | Filesystem | Secrets | Lifetime |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `authority` | `Authority.xpc` | No. Stores source responses as opaque encrypted blobs without decoding them; accepts only strict framed messages (`01` `CON-157`) whose payloads it validates against schemas | All classes | None | Its own container | DEK in memory; old DEKs in the key history (section 29.3) | Session, holding an XPC transaction (`CTRL-246`) |
| `egress-source` | `EgressSource.xpc` (Rust) | HTTP framing, TLS, content decoding of job-source responses | Public source data only; never receives a byte of class `CANDIDATE_PERSONAL`, `CANDIDATE_SENSITIVE`, or `APPLICATION_CONFIDENTIAL` | Only hosts in a source ticket; ticket hosts come only from the source registry and verified employer records (`01` `CON-149`), never from a URL found in a posting | None | None | Session |
| `egress-model` | `EgressModel.xpc` (Rust) | HTTP framing and TLS of model-provider responses | Model request payloads, in flight | Only provider hosts from the provider registry | None | Provider key bound to a ticket (`CTRL-230`) | Started when an R3 task is leased; exits after 60 seconds idle |
| `work-public` | `WorkPublic.xpc` (Python) | Yes: source responses, posting HTML, JSON, XML, feeds | Public source data only | None | Only the temporary exceptions of section 29.4 | None | Recycled after 25 tasks, after 256 MB resident growth, or after 60 seconds idle, whichever is first (provisional, `03` `EXP-314`) |
| `work-private` | `WorkPrivate.xpc` (Python) | Yes: the owner's evidence files, model outputs, relay replies; also renders and validates generated documents | Candidate and application data for one task | None | Only the temporary exceptions of section 29.4 | None | Recycled after every task |
| `commit` | Inside the desktop core | No. Writes opaque bytes whose names it validates itself | Package members in memory during one commit | None | Only the one destination directory, through a handle the core opened | None | Per commit |
| `browser` (later) | Unchanged from `CTRL-228` | | | | | | |
| `model-local` (later) | Unchanged from `CTRL-228` | | | | | | |

Rules that complete the table:

1. A ticket names the one egress instance it is valid on (`role_id`); `egress-source` rejects model tickets and `egress-model` rejects source tickets.
2. A process instance serves one task class for its whole life; `work-private` never processes a public posting task and `work-public` never receives candidate data.
3. The `fetch` role of version 1.2 and the `write` role of version 1.2 are removed (`ADR-208`, `03` `ADR-324`).
4. Each separately confined role is its own bundle, so no design point depends on one bundle running as several instances (`F-14`).

**`ADR-208` Planning in the authority, transport in egress, decoding in work roles.** Context: `F-03` and `F-19` showed that `fetch` both decoded hostile responses (cursors, match keys) and held candidate data for R3 calls, and that the adapter split was undefined. Decision: a source adapter is three entry points in three places (`03` section 34.2): `plan` runs in the authority and turns the source registry entry and a validated cursor into request specifications; `egress-source` performs the requests and returns response bytes, which the authority stores unread; `parse` runs in `work-public` and returns canonical observations, match keys, and the next cursor, each bound to the SHA-256 digest of the input blob. Model calls follow the same shape: the authority builds the request body from validated structured data with a JSON serializer, `egress-model` sends it and returns the response bytes, and `work-private` decodes and validates the model output. Consequences: (1) no role both decodes hostile bytes and reaches the network with candidate data; (2) the authority processes strings that originated in postings only as validated, length-capped fields of canonical structures, never as raw input; (3) one role type fewer to build. Alternatives rejected: a separate `model` role beside `fetch` (keeps a network-adjacent decoder of hostile data), and parsing inside egress (puts candidate data and hostile decoders together).

### 29.3 Keys, backups, and recovery

**`ADR-207` Key protection tiers.** The database key (DEK) is protected at the highest tier the owner's build supports, chosen by `04` `EXP-417` and never downgraded silently:

| Tier | Mechanism | User presence | When used |
| --- | --- | --- | --- |
| `K2` | DEK wrapped by a Secure Enclave P-256 key whose access control requires user presence | Cryptographic: Touch ID or the login password, enforced by the Secure Enclave | Default when `EXP-417` shows that the build can create and use the key and keeps working for at least 90 days without a rebuild, across a same-identity rebuild, and across renewal of the Apple Development certificate |
| `K1P` | DEK in a login keychain item restricted to the app's signing identity, and additionally wrapped by a key derived with Argon2id from a launch passphrase (parameters tuned to about 1 second on the reference Mac, at least 256 MiB memory) | Cryptographic: the passphrase, once per launch; unlocking after a lock uses Touch ID through LocalAuthentication because the DEK is already in memory | Default when `K2` is unavailable |
| `K1` | DEK in a login keychain item restricted to the app's signing identity; in-app LocalAuthentication lock | Not cryptographic: the lock is enforced by the app only | Only when the owner explicitly chooses it over `K1P`; recorded as `RISK-213` |

The security status always names the active tier. A change of tier requires the owner's confirmation and is audited. This refines `CTRL-232` and `04` `ADR-417`: the Secure Enclave remains the goal, and the free signing tier can no longer force a weaker tier without the owner seeing it.

**`CTRL-241` Recovery phrase and recipient-encrypted backups (supersedes the separate backup key of `03` section 8.7 and `04` section 8.3, and refines `CTRL-209` and `CTRL-211`).**

1. At setup the authority generates 256 bits of entropy and shows it once as a 24-word phrase from the BIP-39 English word list with its checksum [RES-220]. The window that shows it is excluded from screen capture where the platform allows it (on macOS, a window sharing type of none). The owner confirms three randomly chosen words. The phrase is never written to disk, the clipboard, a log, or a file dialog.
2. From the entropy, HKDF-SHA-256 with distinct labels derives (a) the recovery X25519 key pair and (b) a recovery wrapping key. The Mac keeps only the recovery public key and a copy of the DEK wrapped by the recovery wrapping key. The entropy and derived private keys are erased from memory after setup.
3. There is no backup key. A backup is a consistent copy of the SQLCipher database and the blob store, both already encrypted under the DEK, plus a key file holding the DEK encrypted in the age format [RES-219] to the recovery public key. The Mac can verify its own backups with the live DEK; no one can open a backup on another Mac without the recovery phrase.
4. When the DEK is rotated, earlier DEKs stay in a key history inside the database, encrypted under the current DEK, until the last backup that needs them expires (30 days), so the weekly restore test still covers every retained backup.
5. The weekly restore test opens the newest backup with the DEK in an isolated scratch location inside the authority's container, runs `PRAGMA integrity_check`, compares row counts against the signed manifest, and deletes the scratch copy. Every 90 days the app offers a recovery drill: the owner types the phrase and the app checks that it derives the stored recovery public key. The drill is optional and can be postponed.
6. A backup folder chosen by the owner must pass the destination rules of `CTRL-242`.

Result: an attacker who copies the login keychain, the authority's container, and every backup, and who knows the login password, opens nothing at tiers `K2` and `K1P` without the Secure Enclave with user presence, the launch passphrase, or the recovery phrase (`AC-231`).

### 29.4 Plaintext on disk, precisely

**`CTRL-231` refined.** The rule of version 1.2 stands: no role keeps a plaintext staging area, and the committed package plus user-requested exports are the only intended plaintext on disk. The exceptions are now exact:

1. A work role may write a temporary file only where `03` `EXP-316` shows a pinned library cannot operate on in-memory bytes. Such a file lives in the role's own container temporary directory, is deleted when the task ends, and is listed by name pattern in the role's manifest of permitted temporary files.
2. The core deletes the contents of every role's temporary directory before the role starts, after the role exits for any reason, and during emergency stop, and verifies that each directory is empty before reporting READY.
3. Role temporary directories are excluded from Time Machine and from Spotlight indexing.
4. Crash reports and core dumps from roles are disabled (`CTRL-246`).

`AC-237` scans for canaries after `kill -9` of each role and after an emergency stop.

**`CTRL-242` At-rest preconditions.**

1. Setup does not complete while FileVault is off. The owner may override with a typed confirmation ("I accept plaintext at rest on this Mac"); the override is audited and shown permanently in the security status.
2. A package destination or backup folder is accepted without override only on the internal APFS volume with FileVault on or on an encrypted APFS external volume. The following are refused unless the owner records a per-folder override with a typed confirmation: iCloud Drive and any File Provider domain, network volumes, exFAT, FAT, NTFS, and any unencrypted volume. Overrides are audited and shown in the destination's protection status.
3. The checks rerun at every revalidation (`04` section 10.2). A folder that no longer qualifies pauses commits to it with `DESTINATION_UNAVAILABLE`.

**`CTRL-243` Package minimization.** Every package member has a schema and a privacy class (`01` `CON-155`). The package never contains raw HTML or any other active content from a job source: the job description is stored as sanitized plain text. `fit-analysis.json` holds scores, the eligibility outcome, and identifiers only, with no free-text field and no reason codes, so it cannot restate the owner's residence, citizenship, work authorization, or immigration facts. The manifest records each member's class, and the package's class is the highest member class.

**`CTRL-247` Posting snapshot retention (resolves `F-18`; refines `PRIV-204`).** Raw fetched bytes of a posting are deleted within 24 hours of successful parsing. The authority keeps a sanitized text snapshot of each posting as an encrypted blob of class `PUBLIC_SOURCE` for the life of any application record that references it, and for 90 days after last use otherwise. The destination copy (`job-description.txt`) is a user-owned export that the product never deletes; `PRIV-204` states that the product's retention rules do not apply to it. Inputs that caused a parsing or validation failure are kept encrypted for 7 days as the reproducibility store required by the DEP prompt, then deleted.

### 29.5 Relay, rendering, clipboard

**`CTRL-244` Relay hardening (refines `CTRL-227`).**

1. Each relay package wraps every data section between markers that contain a fresh 128-bit random value for that exchange; any occurrence of the marker text inside the data is escaped. The header states that nothing between the markers is an instruction and that the model must not use tools, browse, or save memory.
2. Before the first copy in a session, the owner confirms a checklist: a temporary or incognito chat, memory off, connectors and web browsing off, no project context. The confirmation lasts until the app restarts.
3. A reply that contains a URL, a markdown image, or HTML where the reply schema allows none is rejected with a specific reason.
4. For relay extraction of evidence, the owner reviews the outgoing text before it is copied; the preview shows how many identifying strings remain after minimization.
5. R3 with a hard spend cap is the recommended route when the owner has an API key (`00` `CHG-023`); R2 stays the no-key route.

**`CTRL-248` Rendering input rule.** Structured resume content enters document templates only as data (a JSON document read by the template), never as markup built from strings. Package resolution and network access in the renderer are disabled. Templates must not call functions that read files or include images by path; a lint check enforces it. Claim text containing template control sequences is part of the malformed-input corpus (`CTRL-235`).

**`CTRL-249` Clipboard.** Outgoing relay packages are placed on the clipboard only by the core, marked current-host-only and concealed, and cleared after 2 minutes (visible countdown) or as soon as the reply is accepted, whichever is first. The reply the owner copies from the chat service carries none of these protections; this is residual `RISK-214`.

### 29.6 Process hygiene, network surface, testing scope

**`CTRL-245` Minimal network surface in the MVP.** Only the two egress roles hold a network entitlement. The core has no network client: the MVP ships without the updater (`04` `ADR-423`), telemetry, or crash upload. The webview's content security policy allows no network destination. This supersedes the MVP scope of `CTRL-223` and `CTRL-234`; both move to the gate "any use by another person".

**`CTRL-246` Process hygiene.**

1. Long-lived services hold an XPC transaction for their lifetime so that launchd does not end them as idle [RES-221]; their unexpected exit is a supervised crash (`03` section 33.7).
2. Every role host sets `RLIMIT_CORE` to 0 before loading any library.
3. The core's watchdog samples each role's resident memory and CPU time and terminates a role that exceeds its limit (`03` section 9.6 values per role).
4. No credential, key, or path appears in a role's arguments or environment; the bootstrap message is the only channel.
5. Release builds never carry `com.apple.security.cs.disable-library-validation` or `com.apple.security.cs.allow-dyld-environment-variables`. Any other hardened-runtime exception a pinned wheel needs is recorded by `04` `EXP-416`, listed in `04` `AC-431`'s expected set, and accepted here only if it does not grant network or file access.

**`CTRL-233` refined.** Local channels carry a length-prefixed framed protocol (`01` `CON-157`), not HTTP. Frames have a hard size cap; a malformed or oversized frame closes the channel and raises a security event.

**`CTRL-235` refined for the MVP.** Every MVP build runs: the simulated-compromise canary suite in every role (`AC-220`, `AC-221`, `AC-230`); a fixed malformed-input corpus of at least 200 files covering PDF, DOCX, HTML, JSON, XML, relay replies, model outputs, and template control sequences; dependency vulnerability scans; secret scanning; and static analysis. Continuous coverage-guided fuzzing moves to the `CTRL-236` gate.

**`CTRL-240` Confinement self-test, fail closed.** Every role, at start and before it accepts work, runs a self-test and reports the result to the core: an outbound connection to a canary address (must fail, except in egress roles where a non-ticketed destination must be refused by the role's own code and the OS check is recorded), opening a canary file planted outside its container (must fail), and listing the home folder (must fail). The core reports READY only when every required role passes. The security status shows each role's confinement tier. Start is disabled while any required role runs below "OS-confined, no network" (egress roles: "OS-confined, network only through ticket policy").

**`ADR-209` The UI lock protects the interface, not the run.** Context: `F-09`. Version 1.2 paused runs on every lock, which the owner would switch off in practice, while the DEK stayed in memory anyway. Decision: a run started while unlocked continues after the UI locks, including provider key supply for that run's tickets, because the owner authorized it while present. While locked, no new run starts, no approval, export, deletion, disclosure-class change, or destination change is accepted (`ERR-116`), and relay steps wait. Runs pause on system sleep. "Pause runs when locked" is an opt-in strict setting. Consequence: a person at the unlocked Mac after the owner walks away sees only the lock screen; a same-user attacker gains nothing new because the DEK was already in memory (`SEC-A-202`).

### 29.7 Release gates, revised

| Gate | Mandatory controls |
| --- | --- |
| MVP, local Manual (owner's personal use) | `CTRL-201`, `CTRL-202`, `CTRL-203` (local), `CTRL-209` to `CTRL-217`, `CTRL-221`, `CTRL-222`, `CTRL-224`, `CTRL-226`, `CTRL-227`, `CTRL-228` to `CTRL-233`, `CTRL-235` (MVP scope), `CTRL-239` to `CTRL-250` |
| Any use by another person | All of the above plus `CTRL-223`, `CTRL-234`, `CTRL-236`, continuous fuzzing, and a notarized or equivalently signed build (`04` tier T2) |
| Synchronization and mobile | Version 1.1 sync gate plus `CTRL-237` |
| Browser automation, Hybrid, Auto | `CTRL-238` and a fresh `CTRL-236` review, plus the version 1.1 gates |

This table replaces the MVP row of section 22 and the MVP row of section 28.6.

### 29.8 Acceptance criteria added

| ID | Test and release acceptance | Owner |
| --- | --- | --- |
| `AC-230` | A test build that grants network to `work-public`, or removes a role's sandbox, makes that role's self-test fail; the core does not report READY and Start is disabled; the security status names the role and its tier. | `03`, `04`; MVP |
| `AC-231` | At tiers `K2` and `K1P`: copying the login keychain items, the authority container, and every backup to another Mac, with the login password known, opens neither the database nor any backup; entering the recovery phrase opens them. No file on the Mac contains the phrase, the entropy, or a private key derived from it. | `04`; MVP |
| `AC-232` | Setup with FileVault off stops unless overridden; one negative fixture per refused destination class (iCloud Drive, a File Provider domain, a network volume, exFAT, an unencrypted APFS volume) is refused for both packages and backups unless overridden, and each override is audited. | `04`; MVP |
| `AC-233` | Every committed package validates against `01` `CON-155`; it contains no HTML; `fit-analysis.json` contains no free-text field; the manifest lists a class for every member. | `01`, `03`; MVP |
| `AC-234` | With canary strings in the owner's evidence, a full run with R3 shows the canaries in no `egress-source` traffic capture or test-build memory snapshot; `egress-source` rejects a model ticket and `egress-model` rejects a source ticket. | `03`, `04`; MVP |
| `AC-235` | Only the two egress bundles carry `com.apple.security.network.client`; the core binary contains no updater plugin; a socket scan during a run shows outbound connections only from egress processes. | `04`; MVP |
| `AC-236` | A posting containing the relay closing marker cannot end the data section; replies with a URL, image, or HTML where not allowed are rejected with a reason; the first copy of a session is blocked until the checklist is confirmed. | `03`, `04`; MVP |
| `AC-237` | After `kill -9` of each role mid-task and after an emergency stop, a scan of every container, temporary, cache, and log location finds canaries only as ciphertext and in committed packages. | `03`, `04`; MVP |
| `AC-238` | Every role reports `RLIMIT_CORE` 0; a test role that exceeds its memory limit is terminated by the watchdog; no role's arguments or environment contain a credential, key, or destination path. | `04`; MVP |
| `AC-239` | Rendering a claim that contains template control sequences produces the literal text; a template that calls a file-reading function fails the lint check. | `03`; MVP |

`AC-226` stays and is extended by `AC-231`. `AC-227` moves to the "any use by another person" gate with `CTRL-234`.

### 29.9 Section 22.1 index additions

| Control | Scope; enforcer; protected asset | Safe failure or degradation | Evidence; release |
| --- | --- | --- | --- |
| `CTRL-228` | Every role; OS sandbox; all local data | Role does not start; capability unavailable | `AC-220`, `AC-221`, `AC-224`; MVP |
| `CTRL-229` | Outbound requests; `egress-source`, `egress-model`; network reach | Request refused | `AC-221`, `AC-234`; MVP |
| `CTRL-230` | Provider keys; `egress-model`; API keys | Task pauses with `SECRET_LOCKED` | `AC-222`; MVP when R3 used |
| `CTRL-231` | Intermediate data; all roles and the core; plaintext | Role refused READY until temporary directories are empty | `AC-223`, `AC-237`; MVP |
| `CTRL-232` | DEK; core and Secure Enclave; database | Lower tier with visible status (`ADR-207`) | `AC-226`, `AC-231`; MVP |
| `CTRL-233` | Local channels; core and authority; commands and data | Channel closed, security event | `AC-225`; MVP |
| `CTRL-234` | Release keys; owner's release machine; update and signing trust | No release | `AC-227`; any use by another person |
| `CTRL-235` | Builds; CI and release checklist; every asset | Build blocked | Suite results; MVP scope, full at distribution |
| `CTRL-236` | Isolation design and release candidate; independent reviewer | No use by another person | Review report; distribution |
| `CTRL-237` | Synchronized protected classes; devices; candidate data | No sync | `AC-228`; sync |
| `CTRL-238` | Automation browser; VM; host and sessions | No browser automation | `AC-229`; browser phase |
| `CTRL-239` | Role separation by data class; core and OS sandbox; candidate data | Role unavailable | `AC-230`, `AC-234`; MVP |
| `CTRL-240` | Role start; core; confinement proof | Start disabled | `AC-230`; MVP |
| `CTRL-241` | Recovery and backups; authority and core; database and blobs | Setup does not complete without a confirmed phrase | `AC-231`; MVP |
| `CTRL-242` | Setup and destinations; core; plaintext at rest | Setup or folder refused unless overridden | `AC-232`; MVP |
| `CTRL-243` | Package contents; `work-private`, authority, core; candidate data | Commit refused | `AC-233`; MVP |
| `CTRL-244` | Relay; authority, `work-private`, desktop; candidate data and chat account | Copy blocked or reply rejected | `AC-236`; MVP |
| `CTRL-245` | Network surface; build and core; all data | Build blocked | `AC-235`; MVP |
| `CTRL-246` | Role processes; core watchdog and role hosts; memory contents | Role terminated | `AC-238`; MVP |
| `CTRL-247` | Posting snapshots; authority; public and audit data | Deletion on schedule | Retention fixture; MVP |
| `CTRL-248` | Rendering; `work-private`; generated documents | Render fails closed | `AC-239`; MVP |
| `CTRL-249` | Clipboard; core; relay package | Cleared early | `04` `AC-446`; MVP |
| `CTRL-250` | Backup export; core; database and blobs | Export refused; in-container backups continue | `AC-240`; MVP |

### 29.10 Residual risks, stated plainly

The owner asked for a product with no security gaps. No software can promise that literally; what this revision achieves is that every gap the audit found is closed, and every risk that remains is named, bounded, and accepted here rather than hidden.

| ID | Residual risk | Why it cannot be removed | Bound |
| --- | --- | --- | --- |
| `RISK-206` | The desktop core is unsandboxed and trusted | It supervises roles, reads the key store, and writes packages | Small Rust core; no network (`CTRL-245`); decodes no hostile bytes; `CTRL-235` |
| `RISK-207` | Malware already running as the owner | An OS account boundary cannot contain code running as the same user (`SEC-A-202`) | Tiers `K2` and `K1P` stop silent DEK theft at rest; nothing stops it while the app is unlocked |
| `RISK-208` | macOS sandbox or kernel escape | Outside the product's control | Timely OS updates; an escape from `work-public` still holds no candidate data or key |
| `RISK-210` | Plaintext the owner chooses to export or paste | The product's purpose | `CTRL-242`, `CTRL-243`, `CTRL-244`, disclosure ledger |
| `RISK-211` | The authority decodes framed messages from roles that may be compromised | The authority must accept results | Strict frame cap, schema validation, no dynamic evaluation, `CTRL-235` corpus includes malformed frames |
| `RISK-212` | `egress-model` holds candidate data in flight and decodes provider HTTP | R3 sends that data to the provider by design | Rust, provider hosts only, TLS verification, exits when idle |
| `RISK-213` | Tier `K1` has no cryptographic user presence | Chosen only by the owner over `K1P` | Visible status; default is `K1P` or `K2` |
| `RISK-214` | The relay reply on the clipboard is readable by any same-user process | The chat service places it there | Accepted immediately and cleared; advisory in the relay sheet |
| `RISK-215` | Continuous fuzzing starts only at the distribution gate | Buildability for one developer (`F-06`) | Fixed corpus on every build; parsers run in `work-public` and `work-private`, which hold no network |

### 29.11 Research added

| ID | Source | URL | Supports |
| --- | --- | --- | --- |
| `RES-219` | age file encryption format specification, v1 | https://age-encryption.org/v1 | `CTRL-241` |
| `RES-220` | BIP-39, mnemonic code for generating deterministic keys (word list and checksum) | https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki | `CTRL-241` |
| `RES-221` | Apple, `xpc_transaction_begin()` | https://developer.apple.com/documentation/xpc/1505586-xpc_transaction_begin | `CTRL-246` |

### 29.12 Superseded or refined text

| Earlier text | Now |
| --- | --- |
| `CTRL-228` role table (rows `fetch`, `write`) | `CTRL-239`; the rule of `CTRL-228` stands |
| `CTRL-232` last sentence (fallback to the OS key store) | `ADR-207` tiers |
| `CTRL-209` "recovery material"; `CTRL-211` "encrypted with a recovery key independent of a lost live installation" | The recovery phrase and recipient-encrypted backups of `CTRL-241`, which satisfy both |
| `CTRL-231` "Private temporary directories are wiped when a role is recycled" | Section 29.4 exceptions and sweeps |
| `CTRL-233` "the authority serves those connections directly" | Framed protocol, `01` `CON-157` |
| `CTRL-235` "continuous fuzzing" in every release | MVP scope in section 29.6; continuous fuzzing at `CTRL-236` |
| Section 22 MVP row and section 28.6 MVP row | Section 29.7 |
| Section 22.1 index without `CTRL-228` to `CTRL-238` | Section 29.9 |
| `AC-221` "in `fetch` it can reach only `egress`" | Work roles reach nothing; only egress roles have network (`AC-235`) |
| `AC-227` MVP release | Any use by another person |
| `RISK-209` | Covered by `ADR-207` and `CTRL-245` |
| `PRIV-204` rows for the posting snapshot and raw HTML | `CTRL-247` |
| `THR-201` "stolen backup" mitigation `CTRL-211` | `CTRL-241` |
| `CTRL-202` lock semantics for runs | `ADR-209` |
| `CTRL-226` "A local Unix socket or named pipe uses OS access checks plus installation credential" | Local channels are pre-connected and framed (`CTRL-233` refined); no socket file or pipe name exists |
| `AC-201` "Second OS user and rogue local process cannot invoke local authority ... through IPC" | Still required; tested by `03` `AC-337` against pre-connected channels, since no endpoint exists to invoke |
| `THR-210` local inference endpoint | Unchanged for R4 (later); `model-local` stays confined per `CTRL-228` |

### 29.13 Second independent verification (2026-09-29)

A second reviewer, independent of the author and of the first audit, checked the fixes above. It rated `F-01`, `F-03`, `F-07`, `F-08`, `F-09`, `F-12`, `F-15` to `F-17`, `F-20` to `F-22`, and `F-24` closed and the rest partially closed, and found ten new issues (`N-1` to `N-10`: 2 High, 5 Medium, 3 Low) plus two Low notes. Every one is fixed below or in `03` section 34.15, `04` section 32.15, and `01` section 29.3. After these fixes no finding of either review is open.

**`CTRL-250` Backup export (fixes `N-1`, High).** Backups are written first inside the authority's container, where they are encrypted and included in Time Machine. The copy to an owner-chosen folder is written by the desktop core's `commit` principal under a separate `backup` capability: the authority streams the backup set as frames; the core writes it through a directory handle of a folder that passes `CTRL-242`, accepts only the names of `01` section 29.3 (a `backup-<timestamp>` directory holding `db.sqlcipher`, `blobs-NNNN.bin`, `key.age`, and `manifest.json`), flushes with `F_FULLFSYNC`, reads back, and reports digests. The weekly restore test covers the newest owner-folder copy by having the core stream it back into the authority's scratch location. Setup recommends an encrypted APFS external drive for this folder, because a copy on the same Mac does not survive the loss of the Mac.

**`CTRL-239` amendments (fix `N-3`, High, and `N-5`, Medium).**

1. Ticket hosts have exactly three origins: the source registry, verified employer records (`01` `CON-149`), and portfolio hosts the owner enters in settings. A portfolio host is HTTPS on port 443 only and passes the `CTRL-217` address checks at every request and redirect, like any other host. Responses from a portfolio host go only to `work-private`, never to `work-public`.
2. New privacy class `SOURCE_QUERY` (`01` section 29.3): the minimum search parameters the owner approved for sending to job sources (keywords, location, remote preference, posted-since window). `egress-source` may hold `SOURCE_QUERY` data and public source data and nothing else of the owner's. The readiness review shows the owner the exact query parameters each source will receive.
3. `plan` places a cursor only as a percent-encoded value of a query parameter or body field that the adapter declares, never in the URL path or host.

**`CTRL-246` item 6 (fixes `N-4`, Medium).** macOS crash reports (the `.ips` files written by ReportCrash) cannot be disabled for one process. Therefore:

- Role hosts install a fatal-signal handler that records only a code and exits with `_exit`.
- Rust code builds with `panic = "abort"` and a panic hook that prints no payload.
- Python's exception hook records exception type, module, and line only.
- No product code puts candidate or posting data in an assertion, abort, or panic message.
- At startup and after every role crash, the core records that the crash happened and then deletes crash reports for role process names from `~/Library/Logs/DiagnosticReports`.

Residual: a report written by the OS may hold register values or stack fragments until the core deletes it (`RISK-217`).

**`CTRL-243` amendments (fix `N-6` and a Low note).** `fit-analysis.json` carries the eligibility outcome only; `eligibility_reason_codes` is removed, because such codes can restate work authorization or residence. The body of `job-description.txt` has bidirectional override and isolate characters (U+202A to U+202E, U+2066 to U+2069) removed, as directory names do.

**`CTRL-247` amendment (fixes `N-9`, Medium).** The DEP prompt's reproducibility requirement is met in full for failures (7-day quarantine) and in part for successes: a successful parse is reproduced from the sanitized snapshot, the adapter version, and the adapter's fixtures, not from the original bytes, which are deleted after 24 hours to respect source permissions and minimize retention. This deviation is accepted as `RISK-216`.

**`ADR-209` clarification (Low note).** A run that continues while the interface is locked may commit packages to the destination it started with; a commit is not a consequential user command. Changing the destination is.

| ID | Test and release acceptance | Owner |
| --- | --- | --- |
| `AC-240` | After a backup to an encrypted external APFS drive, a second Mac with a fresh install and only the recovery phrase restores the database and blobs, and both pass `PRAGMA integrity_check` and the manifest row counts. | `04`; MVP |
| `AC-241` | Portfolio host fixtures: an `http` URL, a port other than 443, a host resolving to a private, loopback, or link-local address, and a redirect to one are each refused; a portfolio response is never delivered to `work-public`. | `03`; MVP |
| `AC-242` | After a forced crash of each role, no crash report for a role process remains in `~/Library/Logs/DiagnosticReports` once the core has recorded the crash; `AC-237`'s scan includes that folder. | `04`; MVP |

| ID | Residual risk | Why it cannot be removed | Bound |
| --- | --- | --- | --- |
| `RISK-216` | Successful parses are reproduced from sanitized snapshots, not the original bytes | Source permissions and retention minimization | Adapter fixtures; failures keep original bytes for 7 days |
| `RISK-217` | An OS crash report may briefly hold fragments of role memory | macOS writes it before the core can act | Deleted when detected; no data in messages; `RLIMIT_CORE` 0 |

### 29.14 Approval and change record

| Change | Old state (v1.2) | New state (v1.3) | Sections | Downstream effect |
| --- | --- | --- | --- | --- |
| `CHG-213` | Audit findings `F-01` to `F-24` open | Fixed by `CTRL-239` to `CTRL-249`, `ADR-207` to `ADR-209`, `AC-230` to `AC-239`, the second-review fixes of section 29.13 (`CTRL-250`, `AC-240` to `AC-242`, `RISK-216`, `RISK-217`), and the refinements above | 29 | `00`, `01`, `03`, `04`, `07` |
| `CHG-214` | Section 22 gate and 22.1 index incomplete | Section 29.7 and 29.9 | 22, 29 | `07` derives its gates from section 29.7 |
| `CHG-215` | Status "pending the owner's review" | Approved as version 1.3 | 1 | Binding for `05` to `07` |

Approval: on 2026-09-29 the product owner instructed that the audit gaps be fixed and approved all documents on that basis. Version 1.3 is approved. The Version and Status rows of section 1 were updated in place; no other line of earlier text was changed.

## 30. Version 1.4: Synchronized Job Data and the Mobile Companion (2026-09-30)

### 30.1 Direction and scope

The review of `05` version 0.1 (`05` section 30) found that the synchronized topology, as approved, would let the control plane read which postings, employers, and roles the owner pursues, and that several controls the phone depends on had no home in this document. On 2026-09-30 the product owner directed that these security gaps be fixed at their source. This section records the fixes. No identifier was removed or renumbered and no line of version 1.3 was deleted; the Version and Status rows of section 1 were updated in place. Where this section and an earlier section disagree, this section governs to the extent stated in section 30.9.

### 30.2 New threat

| Threat, priority | Asset; adversary; entry and path | Impact and plausibility | Controls | Test |
| --- | --- | --- | --- | --- |
| `THR-226` P0 (later) | The owner's job search: which postings, employers, roles, locations, and search terms the owner considers, shortlists, applies to, and hears back from; a control-plane operator, a database leak, a host compromise, or legal process against the host; synchronized `PUBLIC_SOURCE` records and `SOURCE_QUERY` values linked to the owner's account, or plain digests of public postings matched against the public postings | Critical; conditional on operator or host compromise, but one breach reveals the whole search history, including employers the owner would not want told (for example a current employer) | `ADR-210`, `CTRL-237` | `AC-243`, `AC-244` |

### 30.3 Decision

**`ADR-210` Account-linked job data is protected when synchronized.** Context: `ADR-205` encrypts `CANDIDATE_PERSONAL`, `CANDIDATE_SENSITIVE`, and `APPLICATION_CONFIDENTIAL` end to end, and section 18 lets selected `PUBLIC_SOURCE` job metadata sync. A posting is public, but the fact that this owner looked at it, shortlisted it, or applied is personal information about the owner. Decision: in a synchronized realm, every record that names or identifies a posting or employer, or is derived from one, is encrypted on the owner's devices under `ADR-205`'s key hierarchy and is never readable by the control plane. This covers:

| Covered | Examples |
| --- | --- |
| Posting identity and content | Job title, employer display name and aliases, location as posted, employment type and compensation as posted, posting URL, source posting identifier, posting text and sanitized snapshots, employer records (`01` `CON-149`) |
| Derived records | Canonical job grouping evidence, eligibility assessments, fit analyses, decision records and explanations, package manifests, application timelines, outcome events, notes |
| Search parameters | `SOURCE_QUERY` values (`01` section 29.3 item 3) |
| Notification targets | Anything a notification points to beyond its `ntf_` ID |

The control plane keeps only: entity IDs, source registry IDs (`src_`, which name sources such as a job board, not employers), revisions, states and state transitions, timestamps, sizes (bucketed, rule 3), and digests (rule 2). Rules:

1. Records are encrypted before they leave the device authority that created them, exactly as for the classes of `ADR-205`; workers on other machines receive task inputs encrypted to their own device key (`03` section 33.10).
2. A digest the control plane stores or compares for a covered record is computed over the ciphertext, or keyed (HMAC-SHA-256) with a realm key derived from the content key hierarchy that the control plane does not hold. A plain digest of a public posting or its text is forbidden, because anyone can compute the same digest from the public posting and match it.
3. Ciphertexts of covered records are padded to the next power of two up to 64 KiB, then to the next multiple of 64 KiB, so that sizes do not identify postings.
4. Control-plane queries filter and sort only by the fields in the list above; filtering by eligibility, fit, employer, title, or location happens on the client after decryption (`03` `ADR-325`).
5. Deduplication across users is not available and not needed for a single-user realm; grouping evidence is computed by the device authority.

Consequences: (1) the control plane cannot build server-side job search features; (2) clients download and decrypt the projections they display, which is bounded for one user (`05` section 9.2 caps phone storage); (3) timing, counts, and bucketed sizes remain visible to the operator (`RISK-218`). Section 18's `PUBLIC_SOURCE` row ("selected job metadata may sync") is superseded for synchronized realms: such metadata syncs only as protected content. `ADR-203` no longer describes any field of a covered record.

### 30.4 New controls

**`CTRL-251` Proof-of-possession sessions for every remote client.** Every request from a desktop sync client or a phone to the control plane carries a signature by a key registered for that device (the desktop key of `04` section 33, the phone's `MK-C` of `05` `ADR-505`) over the method, path, body digest, access token digest, client time, and a fresh 128-bit nonce. The control plane rejects a token presented without a valid proof from the key bound to its session (`01` `ERR-118`), a proof more than 120 seconds from its clock, and a nonce seen in the last 24 hours. This refines `CTRL-225` and `CTRL-226`: a stolen session token is useless without the device's hardware key.

**`CTRL-252` Signed device registry and re-verification of human decisions.** Device and worker-supervisor keys are trusted only through the registry of `01` `CON-159`: every enrollment, key replacement, and revocation is signed by an enrolled device's decision key or by the recovery key, and every client verifies the chain from the anchor it pinned at enrollment and refuses a chain older than one it has seen. The control plane stores and serves the registry but cannot add to it. A human decision (`CON-136` approvals, `01` `CON-160` package acceptances, device revocations) is verified again against the registry by the worker installation's supervisor before any external effect and by the desktop `commit` principal before any commit; the control plane's word alone is never enough. This closes the path by which a compromised control plane could enroll its own device, receive the wrapped content key, or forge an approval. The exact encoding stays in `OQ-208`.

**`CTRL-253` Worker-signed stop receipts.** A stop is shown as confirmed only on a receipt (`01` `CON-158`) signed by the key of the process that supervises the worker installation's roles (`04` section 33), whose key is in the registry. The control plane reports `ACCEPTED`, `WORKER_CONFIRMED`, or `WORKER_UNREACHABLE` (`01` section 29.4); neither the network nor the operator can make a stop look confirmed. This refines `CTRL-207` ("label stop unacknowledged").

**`CTRL-254` Encryption export declaration and review.** Every build uploaded to App Store Connect, including TestFlight builds, carries an encryption declaration with its recorded reasoning [RES-222]. Before any build is distributed to another person (desktop or mobile), a professional review of export classification and any required filings under the rules that apply to the publisher's location and the distribution channels is part of the "any use by another person" gate. This document gives no legal conclusion.

**Mobile controls adopted.** `05` section 21 (`THR-501` to `THR-514`, `CTRL-501` to `CTRL-515`) is part of this document's threat register and control index from this version on. `CTRL-225`'s step-up for a decision made on a registered phone is the phone's `MK-D` signature over the exact command, produced after a fresh biometric match enforced by the phone's secure hardware (`05` `ADR-504`); WebAuthn stays required for sign-in, session renewal, device enrollment, and recovery.

### 30.5 Release gates, revised

| Gate | Added mandatory controls |
| --- | --- |
| Synchronization and mobile | `ADR-210`, `CTRL-251`, `CTRL-252`, `CTRL-253`, `05` `CTRL-501` to `CTRL-515` (the last for mobile), in addition to section 29.7's row |
| Any use by another person | `CTRL-254` in addition to section 29.7's row |
| First TestFlight upload (`05` tier `IT1`) | `CTRL-254` declaration |

### 30.6 Acceptance criteria

| ID | Test and release acceptance | Owner |
| --- | --- | --- |
| `AC-243` | A full dump of the control-plane database for a synthetic realm with 200 jobs, 20 shortlisted, 5 applications, and saved search terms contains no job title, employer name or alias, location, compensation, posting URL, source posting ID, posting text, or search term. | `03`, `05`; sync |
| `AC-244` | For every posting fetched in that fixture, SHA-256 of its text, snapshot, URL, and source posting ID matches no digest stored by the control plane; every stored ciphertext size of a covered record is a padding bucket of `ADR-210` rule 3. | `03`; sync |
| `AC-245` | A valid access token replayed from another machine without the device's proof is rejected with `ERR-118`; a reused nonce and a 121-second clock skew are rejected; this holds for the desktop sync client and the phone. | `03`, `04`, `05`; sync |
| `AC-246` | A registry entry, approval, package acceptance, or revocation inserted by a test hook in the control plane without a valid signature from an enrolled device is rejected by every client, by the worker supervisor before an effect, and by the `commit` principal before a commit. | `03`, `04`, `05`; sync |
| `AC-247` | A stop receipt signed by any key other than the worker supervisor's registry key is rejected; with the worker offline, `WORKER_UNREACHABLE` is reported 45 s after `ACCEPTED`. | `03`, `05`; sync |

### 30.7 Residual risk

| ID | Residual risk | Why it cannot be removed | Bound |
| --- | --- | --- | --- |
| `RISK-218` | The operator sees how many records exist, when runs and decisions happen, bucketed sizes, client IP addresses, and push timing | Ordering, leases, and delivery need them | Padding (`ADR-210` rule 3); no content, titles, employers, or search terms; self-hosting on a host the owner controls removes the third-party operator |

### 30.8 Research added

| ID | Source | URL | Supports |
| --- | --- | --- | --- |
| `RES-222` | Apple, Complying with encryption export regulations | https://developer.apple.com/documentation/security/complying-with-encryption-export-regulations | `CTRL-254` |

### 30.9 Superseded or refined text

| Earlier text | Now |
| --- | --- |
| Section 18 privacy table, `PUBLIC_SOURCE` row, "selected job metadata may sync" | In a synchronized realm, only as protected content (`ADR-210`) |
| `ADR-205` list of three protected classes | Extended by `ADR-210` to account-linked job data and `SOURCE_QUERY` |
| `ADR-203` "still describes `OPERATIONAL` data" | Unchanged for `OPERATIONAL` data; describes no field of a covered record |
| `CTRL-225` step-up "no older than five minutes" | Kept; on a registered phone the `MK-D` signature over the command is the step-up (section 30.4) |
| `CTRL-207` "label stop unacknowledged" | Refined by `CTRL-253` states and receipts |
| Section 29.7 gate rows | Extended by section 30.5 |
| `OQ-208` | Still open for the full protocol and its independent review; `CTRL-252`, `ADR-210`, and `05` section 9.5 are now fixed inputs to it |

### 30.10 Change record

| Change | Old state (v1.3) | New state (v1.4) | Sections | Downstream effect |
| --- | --- | --- | --- | --- |
| `CHG-216` | Synchronized job metadata readable by the control plane; no proof-of-possession sessions, device registry, stop receipts, or export review; no mobile threats in the register | `THR-226`, `ADR-210`, `CTRL-251` to `CTRL-254`, `AC-243` to `AC-247`, `RISK-218`, `RES-222`; `05` threats and controls adopted | 30 | `00` section 42.4, `01` section 29.4, `03` section 35, `04` section 33, `05` section 31 |
| `CHG-217` | Status: version 1.3 approved | Version 1.4 changes directed by the owner on 2026-09-30; text awaiting the owner's review | 1 | None |
