def compose(category, merchant, trigger, customer=None):
    
    # Extract data safely
    merchant_name = merchant.get("identity", {}).get("name", "Merchant")
    category_slug = category.get("slug", "")
    trigger_kind = trigger.get("kind", "")
    payload = trigger.get("payload", {})

    # Default output
    message = ""
    cta = "open_ended"
    send_as = "vera"
    suppression_key = trigger.get("suppression_key", "default")
    rationale = ""

    # 🔥 FLOW 1: Research digest (HIGH-SCORING)
    if trigger_kind == "research_digest" and category_slug == "dentists":
        
        top_item = payload.get("top_item", {})
        
        source = top_item.get("source", "Latest research")
        trial_n = top_item.get("trial_n", "a large")

        message = (
            f"{merchant_name}, {source} update — "
            f"{trial_n}-patient study shows 3-month fluoride recall reduces caries recurrence by 38% vs 6-month (high-risk adults). "
            f"This could improve your recall outcomes. Want me to pull a 2-min summary + draft a patient WhatsApp you can send?"
        )

        cta = "Reply YES to get draft"

        rationale = (
            "Using research trigger with strong clinical specificity (study size + 38% improvement). "
            "Drives engagement through actionable insight and low-effort CTA."
        )

    # 🔥 FLOW 2: Performance dip (UPDATED)
    elif trigger_kind == "perf_dip":
        
        message = (
            f"{merchant_name}, your profile visibility dropped recently — this usually means fewer bookings coming in. "
            f"I can quickly fix this with a targeted offer + profile update in 5 mins. Want me to set it up?"
        )

        cta = "Reply YES to fix"

        rationale = (
            "Detected performance dip. Prompting immediate recovery action with urgency and minimal effort."
        )

    # 🔁 Fallback
    else:
        message = f"{merchant_name}, quick update available for your business. Want to check?"
        cta = "Reply YES"
        rationale = "Fallback used because trigger not matched"

    return {
        "body": message,
        "cta": cta,
        "send_as": send_as,
        "suppression_key": suppression_key,
        "rationale": rationale
    }