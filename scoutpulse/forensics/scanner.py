"""
Automated reverse-engineering and signature analysis for repository packages and binary assets.
Detects obfuscated downloaders, malicious setup hooks, and unverified executables.
"""
import re
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ForensicFinding:
    severity: str  # HIGH, MEDIUM, LOW
    category: str
    description: str
    matched_pattern: str

class ForensicScanner:
    """
    Lightweight static reverse-engineering scanner for open-source releases.
    Inspects build scripts (setup.py, Makefile, package.json) for suspicious exfiltration hooks.
    """

    SUSPICIOUS_SIGNATURES = [
        (re.compile(r"(base64\.b64decode|eval\(|exec\()"), "OBFUSCATED_EXEC", "HIGH", "Dynamic execution of encoded payloads"),
        (re.compile(r"(curl|wget|powershell|certutil)\s+-[a-zA-Z]*\s+http"), "UNVERIFIED_DOWNLOADER", "HIGH", "Unauthenticated remote payload fetch"),
        (re.compile(r"(\.onion|pastebin\.com|raw\.githubusercontent\.com/[^\s]+/malware)"), "SUSPICIOUS_REMOTE_HOST", "HIGH", "Exfiltration / C2 endpoint match"),
        (re.compile(r"process\.env\[['\"][a-zA-Z_0-9]*KEY"), "CREDENTIAL_HARVESTING", "MEDIUM", "Broad credential environment extraction"),
    ]

    def scan_content(self, filename: str, content: str) -> List[ForensicFinding]:
        findings = []
        for regex, category, severity, desc in self.SUSPICIOUS_SIGNATURES:
            match = regex.search(content)
            if match:
                findings.append(ForensicFinding(
                    severity=severity,
                    category=category,
                    description=desc,
                    matched_pattern=match.group(0)
                ))
        return findings
