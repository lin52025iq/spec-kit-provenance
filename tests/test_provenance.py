import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "python" / "provenance.py"
spec = importlib.util.spec_from_file_location("provenance", MODULE_PATH)
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)


def test_sanitize_url_strips_secret_query_keys():
    value = provenance.sanitize_url("https://Example.com/docs/?token=secret&lang=zh#frag")
    assert value == "https://example.com/docs?lang=zh"


def test_readable_label_for_bare_url():
    value = provenance.readable_label("https://docs.example.com/platform/auth/api-v2")
    assert value == "docs.example.com — auth / api-v2"


def test_figma_is_design_source():
    uri = "https://www.figma.com/design/abc/login"
    provider = provenance.infer_provider(uri)
    assert provider == "figma"
    assert provenance.infer_type(uri, provider) == "design"


def test_add_bare_url_creates_readable_needs_review_entry(tmp_path):
    registry = tmp_path / ".specify" / "provenance" / "sources.md"
    assert provenance.add(
        registry,
        "https://docs.example.com/auth/api-v2",
        None,
        None,
        None,
        "user",
        "plan",
        "登录接口参考",
    ) == 0
    text = registry.read_text(encoding="utf-8")
    assert "SRC-001" in text
    assert "docs.example.com — auth / api-v2" in text
    assert "**Status**: needs-review" in text
    assert "**Origin**: user" in text
    assert "**Introduced during**: plan" in text
    assert "**Context**: 登录接口参考" in text


def test_add_deduplicates_exact_normalized_uri(tmp_path):
    registry = tmp_path / "sources.md"
    provenance.add(registry, "https://example.com/docs/", "Docs", "document", None)
    provenance.add(registry, "https://example.com/docs", None, None, None)
    text = registry.read_text(encoding="utf-8")
    assert text.count("## SRC-") == 1
