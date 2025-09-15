def markdown_to_blocks(markdown):
    blocks = []

    sections = markdown.split("\n\n")
    for block in sections:
        stripped_block = block.strip() 
        if not stripped_block:
            continue
        blocks.append(stripped_block)

    return blocks