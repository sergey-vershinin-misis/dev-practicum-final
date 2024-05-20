import requests

from ..schemas import (
    PopulationStats,
    PopulationStatsExecutionResults,
)


def get_population_stats_by_oktmo_list(
        oktmo_list: list[str],
        api_key: str) -> PopulationStatsExecutionResults:
    out = {}
    exceptions = []
    for oktmo in oktmo_list:
        payload = {
            "key": api_key,
            "oktmo_list": oktmo
        }
        try:
            response = requests.get("https://api.geotree.ru/search.php", params=payload)
            response.raise_for_status()
        except requests.HTTPError as exc:
            exceptions.append({
                "oktmo": oktmo,
                "err_msg": exc,
            })
            continue

        try:
            response_body = response.json()
        except requests.JSONDecodeError as exc:
            exceptions.append({
                "oktmo": oktmo,
                "err_msg": exc,
            })
            continue

        if isinstance(response_body, dict) and response_body.get("error"):
            exceptions.append({
                "oktmo": oktmo,
                "err_msg": response_body.get("message")
            })
            continue

        if isinstance(response_body, list) and not response_body:
            exceptions.append({
                "oktmo": oktmo,
                "err_msg": "Population stats not found"
            })
            continue

        out[oktmo] = (PopulationStats.model_validate({
            "oktmo": oktmo,
            "locality_area": response_body[0]["area"],
            "locality_population": response_body[0]["population"],
        }))
    return PopulationStatsExecutionResults.model_validate({
        "population_stats": out,
        "exceptions": exceptions,
    })
