# 🔐 Secrets & Security Management Blueprint: UAO Repository

**Repository:** [https://github.com/Cobo-san/UAO](https://github.com/Cobo-san/UAO)  
**Security Policy:** Zero Hardcoded Credentials & 100% Environment Variable Isolation

---

## 🛡️ 5-Step Secret Protection Protocol

### 1. Environment Variable Isolation (`.env`)
Never hardcode API keys, passwords, or tokens in source code. Store local secrets in a `.env` file:

```env
# Local Environment Secrets (Ignored by Git)
ACCOUNT_EMAIL=sounddharma@gmail.com
GCP_PROJECT_ID=anaconda-google-project-sounddharma
AZURE_CLIENT_ID=your_azure_client_id_here
AZURE_TENANT_ID=your_azure_tenant_id_here
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id_here
CODECOV_TOKEN=your_codecov_token_here
```

In Python code, access variables safely:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY_SECRET", "fallback_default")
```

---

### 2. Git Ignore Security Enforcement (`.gitignore`)
Ensure all credential files, token keys, and environment files are blocked from Git commits:

```text
# Sensitive Credential Files
.env
.env.local
*.pem
*.key
*.p12
*_credentials.json
service_account.json
```

---

### 3. GitHub Repository Secrets for Actions CI/CD
Store workflow secrets safely in GitHub Repository Settings:
* **Navigate to**: `https://github.com/Cobo-san/UAO -> Settings -> Secrets and variables -> Actions`
* **Add Secrets**:
  - `AZURE_CLIENT_ID`
  - `AZURE_TENANT_ID`
  - `AZURE_SUBSCRIPTION_ID`
  - `CODECOV_TOKEN`

In `.github/workflows/validate-posix-sandbox-paths.yml`:
```yaml
env:
  AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
  AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
```

---

### 4. Automated Pre-Commit Secret Scanner
Before pushing commits, run the automated secret scanner script:
```bash
python bin/scan_for_secrets.py
```
**Status Target**: `100% CLEAN - NO HARDCODED SECRETS OR PRIVATE KEYS DETECTED`.

---

### 5. Git History Scrubbing (Emergency Recovery)
If a secret is ever accidentally committed to Git history, revoke the key immediately and purge it using `git-filter-repo`:
```bash
pip install git-filter-repo
git filter-repo --invert-paths --path .env
git push origin --force --all
```
