from fastapi import FastAPI

app = FastAPI()


# ---------------- HEALTH ----------------
@app.get("/v1/healthz")
def health():
    return {"status": "ok"}


# ---------------- METADATA ----------------
@app.get("/v1/metadata")
def metadata():
    return {"bot": "vera-compose-engine", "version": "1.0"}


# ---------------- CONTEXT ----------------
@app.post("/v1/context")
def context(data: dict):
    return {"accepted": True}


# ---------------- TICK (IMPORTANT) ----------------
@app.post("/v1/tick")
def tick(data: dict):
    merchant = data.get("merchant", {})
    triggers = data.get("available_triggers", [])

    merchant_name = merchant.get("identity", {}).get("name", "Merchant")

    actions = []

    for trigger in triggers:
        kind = trigger.get("kind", "")

        # 🔥 Research
        if kind == "research_digest":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, a new clinical study shows 3-month fluoride recall reduces caries risk significantly. Want a quick 2-min summary?",
                "reason": "research insight"
            })

        # 🔥 Performance dip
        elif kind == "perf_dip":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, your profile visibility dropped recently — this could reduce bookings. Want me to fix it quickly?",
                "reason": "performance recovery"
            })

        # 🔥 No recent activity
        elif kind == "no_recent_activity":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, it's been a while since your last update — a quick refresh can boost visibility. Want help?",
                "reason": "engagement"
            })

        # 🔥 Negative trend
        elif kind == "negative_trend":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, recent trends show a dip in engagement — small tweaks can recover this fast. Want suggestions?",
                "reason": "recovery"
            })

        # 🔥 Competition alert
        elif kind == "competition_alert":
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, competitors nearby are gaining traction — want to boost your visibility this week?",
                "reason": "competition"
            })

        # 🔥 General fallback
        else:
            actions.append({
                "action": "send_message",
                "body": f"{merchant_name}, quick update available for your business. Want to check?",
                "reason": "fallback"
            })

    return {"actions": actions}


# ---------------- REPLY ----------------
@app.post("/v1/reply")
def reply(data: dict):
    user_msg = data.get("message", "").lower()
    from_role = data.get("from_role", "")

    # 🔥 STOP handling
    if "stop" in user_msg:
        return {"action": "end"}

    # 🔥 Auto-reply detection
    if user_msg in ["ok", "thanks", "thank you", "got it"]:
        return {"action": "end"}

    # 🔥 Customer reply
    if from_role == "customer":
        return {
            "action": "reply",
            "body": "Great! Your slot is noted. We’ll confirm shortly."
        }

    # 🔥 Merchant reply
    return {
        "action": "reply",
        "body": "Got it. I’ll take care of that for you."
    }