"""Built-in steps. Importing this module registers them."""
from pipeline_models import Enriched
from pipeline_registry import step


@step("drop_tiny", order=10)
def drop_tiny(item: Enriched) -> Enriched | None:
    return None if item.usd_total < 20 else item


@step("tag_bulk", order=20)
def tag_bulk(item: Enriched) -> Enriched:
    if item.order.qty >= 3:
        item.tags.append("bulk")
    return item


@step("tag_big", order=30)
def tag_big(item: Enriched) -> Enriched:
    if item.usd_total >= 100:
        item.tags.append("big")
    return item
