def transform_id(original_id: str) -> str:
    if original_id.startswith("EAID_"):
        transformed_id = original_id[len("EAID_"):]
    else:
        transformed_id = original_id
    transformed_id = transformed_id.replace("_", "-")

    return transformed_id
