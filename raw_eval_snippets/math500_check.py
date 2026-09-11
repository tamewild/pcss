from math_verify import parse, verify, LatexExtractionConfig, ExprExtractionConfig


def extract_last_box(s: str) -> str:
    """Extracts the innermost content of the last \\boxed{...} tag with balanced braces."""
    tag = "\\boxed{"
    tag_start = s.rfind(tag)
    if tag_start == -1:
        return ""

    content = s[tag_start + len(tag):]
    depth = 1
    for i, char in enumerate(content):
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return content[:i].strip()

    return ""


def check_math500(ground_truth, response) -> bool:
    boxed_content = extract_last_box(response)
    if not boxed_content:
        return False

    boxed_response = f"\\boxed{{{boxed_content}}}"

    # Ensure ground truth is parsable by math_verify
    if "\\boxed" not in ground_truth:
        ground_truth = f"\\boxed{{{ground_truth}}}"

    gold = parse(
        ground_truth,
        # https://github.com/huggingface/Math-Verify/blob/ba3d3aaff23b3f4cac7a14672b4f6e293d97c98b/src/math_verify/tasks.py#L219
        [LatexExtractionConfig(boxed_match_priority=0)]
    )
    resp = parse(
        boxed_response,
        # https://github.com/huggingface/Math-Verify/blob/ba3d3aaff23b3f4cac7a14672b4f6e293d97c98b/src/math_verify/tasks.py#L221
        [
            LatexExtractionConfig(boxed_match_priority=0),
            ExprExtractionConfig()
        ]
    )
    return verify(gold, resp)

