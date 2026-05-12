from codewiki.frontmatter import parse


def test_parses_simple_key_value():
    src = "---\nkind: module\ntitle: Auth\n---\n\n# Body"
    fm, body = parse(src)
    assert fm == {"kind": "module", "title": "Auth"}
    assert body.strip() == "# Body"


def test_parses_list_values():
    src = "---\nsource_paths:\n  - src/auth/\n  - src/middleware/auth.py\ntags: [auth, security]\n---\n"
    fm, _ = parse(src)
    assert fm["source_paths"] == ["src/auth/", "src/middleware/auth.py"]
    assert fm["tags"] == ["auth", "security"]


def test_no_frontmatter_returns_empty_dict():
    fm, body = parse("# Just a heading\n")
    assert fm == {}
    assert body == "# Just a heading\n"


def test_handles_null_and_scalars():
    src = "---\nlast_ingest: null\nsource_commit: abc1234\n---\n"
    fm, _ = parse(src)
    assert fm["last_ingest"] is None
    assert fm["source_commit"] == "abc1234"
