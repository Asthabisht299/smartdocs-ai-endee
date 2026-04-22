def build_answer(query, results):
    if not results:
        return "I could not find relevant information in the uploaded documents."

    top_chunks = results[:3]

    answer_lines = [
        f"Question: {query}",
        "",
        "Answer based on retrieved document context:",
        ""
    ]

    for i, item in enumerate(top_chunks, start=1):
        answer_lines.append(
            f"{i}. From {item['metadata']['file_name']} "
            f"(topic: {item['metadata']['topic']}, chunk: {item['metadata']['chunk_id']}):"
        )
        answer_lines.append(item["text"])
        answer_lines.append("")

    answer_lines.append("This answer is grounded only in the uploaded document chunks shown above.")
    return "\n".join(answer_lines)