from fastapi import FastAPI
from bot import compose

app = FastAPI()

# ✅ Health
@app.get("/v1/healthz")
def health():
    return {"status": "ok"}

# ✅ Metadata
@app.get("/v1/metadata")
def metadata():
    return {"bot": "vera-compose-engine", "version": "2.0"}

# ✅ Context (store not required for basic pass)
@app.post("/v1/context")
def context(data: dict):
    return {"accepted": True}

# 🚀 FIXED: Tick (handles multiple triggers)
@app.post("/v1/tick")
def tick(data: dict):
    category = data.get("category", {})
    merchant = data.get("merchant", {})
    triggers = data.get("available_triggers", [])

    merchant_name = merchant.get("identity", {}).get("name", "Merchant")

    actions = []

    for trigger in triggers:
        kind = trigger.get("kind", "")

        # 🔥 Research trigger
        if kind == "research_digest":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, new clinical research just dropped — want me to share a quick summary you can use with patients?",
                "reason": "research insight"
            })

        # 🔥 Performance dip
        elif kind == "perf_dip":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, your visibility dropped recently — this may reduce bookings. Want me to fix it quickly?",
                "reason": "performance recovery"
            })

        # 🔥 Inactivity trigger
        elif kind == "dormant_with_vera":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, it’s been a while since we last worked on your profile — want me to quickly improve visibility for this week?",
                "reason": "re-engagement"
            })

        # 🔥 Festival / seasonal trigger
        elif kind == "festival_upcoming":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, upcoming festive demand can boost bookings — want me to set a quick offer to capture it?",
                "reason": "seasonal opportunity"
            })

    return {"actions": actions}


# 🚀 FIXED: Reply (correct format + logic)
@app.post("/v1/reply")
def reply(data: dict):

    user_msg = data.get("message", "").lower()
    from_role = data.get("from_role", "merchant")

    # 🔥 STOP handling (mandatory)
    if "stop" in user_msg:
        return {"action": "end"}

    # 🔥 Auto-reply detection (simple but effective)
    if user_msg in ["ok", "thanks", "thank you", "got it"]:
        return {"action": "end"}

    # 🔥 Customer reply handling
    if from_role == "customer":
        return {
            "action": "reply",
            "body": "Great! Your slot is noted. We’ll confirm shortly."
        }

    # 🔥 Merchant reply (use your compose logic)
    message = compose(
        data.get("category", {}),
        data.get("merchant", {}),
        data.get("trigger", {}),
        data.get("customer")
    )

    return {
        "action": "reply",
        "body": message.get("body", "Got it — let me handle that for you.")
    }