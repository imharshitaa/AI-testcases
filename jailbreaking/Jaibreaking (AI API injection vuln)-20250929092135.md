# Jaibreaking (AI API injection vuln)

# **BASELINE**

How malicious input moves from:
Attacker → API → agent → sensitive output.

**Attack structure:**
1. Discover input taking endpoint (chat, file upload, JSON prompt field).
2. Create injection payload (plain / encoded / file) aiming to override system instructions.
3. Submit payload to API endpoint (direct request, file upload, or memory write).
4. Agent composes prompt (system + user + history + file content).
5. Malicious component is interpreted as instruction.
6. Agent gives outputs that is sensitive info and performs unauthorized action.

![](https://t10505733.p.clickup-attachments.com/t10505733/d2693334-8245-437a-8a07-20232d800ffa/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-29-021446.png)
# **LOGIC OF VULNERABILITY**

**Cause:**
Untrusted input is added to the model’s prompt without proper sanitization or separation.

**Effect:**
The model interprets attacker input as an instruction and executes it (e.g., sensitive info, alter behavior).

**Requirements:**
*   User input placed in instruction-like areas of the prompt
*   Missing input validation
*   Use of history/memory without strict controls

**Areas to Inspect:**
*   **Prompt composition** – How system, user, and history text are combined
*   **File parsing** – Does it remove instruction markers?
*   **Memory handling** – Who can write and how data reloads
*   **Logging/metadata** – Risk of leaking hidden data

# **LOGIC OF ATTACK METHOD**

1. **Instruction Override**
*   Attacker embeds an explicit override instruction inside user-supplied text.
*   The prompt composer merges that text into the model input without blocking or distinguishing instructions from data.
*   The model sees the override as authority and executes the attacker’s instruction (e.g., reveal secrets or change behavior).

![](https://t10505733.p.clickup-attachments.com/t10505733/a0d73df1-8740-47f9-8a05-02f3942843f3/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-29-025428.png)

1. **Context Poisoning**
*   Attacker stores malicious instructions into writable persistent memory.
*   System saves poisoned content without validation or role separation.
*   Future prompts merge memory, causing model to follow instructions.

![](https://t10505733.p.clickup-attachments.com/t10505733/094cf600-dc40-45e2-a73e-6620e51f0952/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-29-031008.png)

1. **File Injection**
*   Attacker uploads file containing instruction-like or malicious prompt.
*   Parser reads file and appends content into prompt.
*   Model receives merged prompt and may execute embedded instructions.

![](https://t10505733.p.clickup-attachments.com/t10505733/3a6cf018-e915-48e6-b1d3-500ee4590839/Untitled%20diagram%20_%20Mermaid%20Chart-2025-09-29-032200.png)

# **PAYLOADS**

| Type | Work structure | Workflow |
| ---| ---| --- |
| Instruction override | Plain text that tells the model to ignore prior instructions. Model may execute attacker’s command. | User → Composer → Model |
| Encoded payload | Base64 or URL-encoded text that evades simple filters. Parser may decode or model interprets directly. | User → Parser (decodes) → Composer → Model |
| Escaped JSON | JSON object embedded in a string. Parser may merge inner fields into prompt, overriding rules. | User → Parser (string→JSON?) → Composer |
| File-embedded | Uploaded file contains malicious instructions. Parser concatenates content into prompt. | File → Parser → Composer → Model |
| Memory poison | Malicious note written to memory store. Future sessions merge it into prompt, affecting all interactions. | User → Memory API → DB → Session → Composer |

![](https://t10505733.p.clickup-attachments.com/t10505733/626512b7-a469-48a4-b0f8-b21429cae8cc/image.png)

Payload sample python program:
link -
[https://github.com/imharshitaa/AI-testcases/blob/main/jailbreaking/payload.py](https://github.com/imharshitaa/AI-testcases/blob/main/jailbreaking/payload.py)

# **PYTHON SCRIPT 1 - ATTACK METHOD**

Working:
*   Load payloads from generator module into memory.
*   Send payloads as user messages to endpoint.
*   Optionally write payloads into memory API.
*   Optionally upload file payloads to file endpoint.
*   Log responses and flag potential secret leaks.

Link: [https://github.com/imharshitaa/AI-testcases/blob/main/jailbreaking/exploit\_attack.py](https://github.com/imharshitaa/AI-testcases/blob/main/jailbreaking/exploit_attack.py)

# **PYTHON SCRIPT 2 - TOOL BASED ATTACK TESTING**

Working:
*   Generate curl scripts and JSON bodies.
*   Export payload lists usable by Burp Intruder.
*   Make curl scripts executable and runnable.
*   Optionally execute a selected curl script locally.
*   Save artifacts (scripts, bodies, burp files).

Link: [https://github.com/imharshitaa/AI-testcases/blob/main/jailbreaking/exploit\_tools.py](https://github.com/imharshitaa/AI-testcases/blob/main/jailbreaking/exploit_tools.py)