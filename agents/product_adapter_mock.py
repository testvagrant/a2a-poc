import re
import json
from typing import List, Dict, Any
from pathlib import Path
import yaml

class MockProductAgent:
    """
    A very simple mock "collections" agent.

    It reads fixtures and policies, then replies to the tester with:
      - mandatory disclosure
      - policy-compliant text
      - a structured object (agent_structured) used by judges
    """
    def __init__(self, fixtures_dir: str):
        self.fixtures_dir = Path(fixtures_dir)
        with open(self.fixtures_dir / "debtors.json", "r", encoding="utf-8") as f:
            self.debtors = json.load(f)
        with open(self.fixtures_dir / "policies.yaml", "r", encoding="utf-8") as f:
            self.policies = yaml.safe_load(f)

    def send(self, conversation: List[Dict[str, str]], debtor_id: str) -> Dict[str, Any]:
        user_last = next((m for m in reversed(conversation) if m["role"] == "user"), {"content": ""})
        user_text = user_last["content"].lower()
        debtor = self.debtors.get(debtor_id, {})
        disclosure = self.policies["mandatory_disclosures"][0]

        parts = [f"{disclosure}. "]
        structured: Dict[str, Any] = {
            "intent": None,
            "outcome": None,
            "promise_to_pay": None,
            "actions": []
        }

        # Check if user is confirming a promise-to-pay
        if any(k in user_text for k in ["yes", "confirm", "promise to pay"]) and "₹" in user_text:
            structured["intent"] = "confirm_promise"
            parts.append("Thank you for confirming your promise to pay. ")
            parts.append("Your payment plan has been recorded. ")
            parts.append("We'll send you a confirmation email with the details. ")
            structured["outcome"] = "success"
            # Extract amount and date from user's confirmation
            amount_match = re.search(r'₹(\d+)', user_text)
            date_match = re.search(r'(\d{4}-\d{2}-\d{2})', user_text)
            if amount_match and date_match:
                structured["promise_to_pay"] = {
                    "date": date_match.group(1),
                    "amount": int(amount_match.group(1)),
                    "confirmed": True
                }
        elif any(k in user_text for k in ["dispute", "verification"]):
            structured["intent"] = "dispute"
            parts.append("I understand you wish to dispute. You may request verification of this debt. ")
            parts.append("I'll escalate and handoff you to a specialist for further assistance. ")
            structured["actions"].append("handoff")
            structured["outcome"] = "partial"
        elif any(k in user_text for k in ["wrong person", "not the person", "wrong number"]):
            structured["intent"] = "cease"
            parts.append("Thanks for letting us know. We'll update our records and stop contacting this number. ")
            structured["actions"].append("cease_contact")
            structured["outcome"] = "success"
        elif any(k in user_text for k in ["pay next week", "pay next", "next week", "payment plan"]):
            structured["intent"] = "set_payment_plan"
            parts.append("We can offer a plan that fits your situation. ")
            parts.append(f"Your current balance is ₹{debtor.get('balance', '—')}. ")
            promise_date = "2025-09-08"
            try:
                promise_amount = max(debtor.get("min_payment", 1000), int(debtor.get("balance", 0) * 0.2))
            except Exception:
                promise_amount = debtor.get("min_payment", 1000)
            parts.append(f"Can you confirm a promise to pay ₹{promise_amount} by {promise_date}? ")
            structured["promise_to_pay"] = {"date": promise_date, "amount": promise_amount}
            structured["outcome"] = "success"
        else:
            structured["intent"] = "collect_payment"
            parts.append("How can I help you regarding your account today? ")

        forbidden = self.policies.get("forbidden_phrases", [])
        txt = "".join(parts)
        for f in forbidden:
            txt = re.sub(re.escape(f), "", txt, flags=re.IGNORECASE)

        return {"text": txt.strip(), "structured": structured}
