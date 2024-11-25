def markdown_to_blocks(markdown):
    blocks = [line for line in markdown.split("\n\n") if line.strip()]
    block = [s.strip() for s in blocks]
    return block
