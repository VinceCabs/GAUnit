""""
Getting Started

Code sample: This is the code from the "Getting Started" GAUnit Documentation : 
https://gaunit.readthedocs.io/en/latest/tutorial.html
"""
import gaunit

tracking_plan = gaunit.TrackingPlan.from_json("tracking_plan.json")
r = gaunit.check_har(
    "demo_store_add_to_cart", tracking_plan, har_path="demo_store_add_to_cart.har"
)
print(r.was_successful())
# True

