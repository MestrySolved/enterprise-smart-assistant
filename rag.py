def retrieve_context(query):

    with open("office_policy.txt", "r") as f:
        text = f.read()

    chunks = text.split("\n")

    relevant_chunks = []

    for chunk in chunks:

        if any(word.lower() in chunk.lower()
               for word in query.split()):

            relevant_chunks.append(chunk)

    return "\n".join(relevant_chunks)