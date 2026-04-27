---
name: Generate Infographic
description: Crafts a beautiful visual infographic (image) based on a podcast summary, reflecting key topics and stories.
---

# Generate Infographic Skill

This skill parses a provided podcast summary (usually from a Markdown or Text file) and instructs the agent to generate an actual graphical infographic, rather than a text-based flowchart like Mermaid.js. Infographics are visual image files that combine stories, key figures, and information elegantly.

## Instructions

Whenever you need to invoke this skill, follow these steps:

1. **Read the Summary**: Use your file viewing capability to read the target podcast summary file.
2. **Draft a Visual Prompt**: Extrapolate the 3-4 key themes, important quotes, or core concepts from the summary into a highly detailed image generation prompt. Specify that the style should be an "infographic" with bold typography, complementary color palettes, and clear iconography.
3. **Generate the Image**: Use your `generate_image` tool (or the relevant API/tool available in your environment) passing the prompt you created. 
4. **Save Target**: Name the output file `infographic` so it is saved as an image in the current workspace.
5. **Embed**: When assembling the final newsletter or markdown file, embed the actual image file (e.g., `![Podcast Infographic](infographic.webp)`) instead of outputting mermaid code blocks.

## Guardrails
- **Image Generation Only**: Do not output ````mermaid```` code. You must generate an actual image.
- **Prompt Effectiveness**: Keep text rendering elements in the prompt concise, as image models handle short text elements better than long paragraphs. Focus on the visual layout, style (e.g., flat design, 3D render, minimalist), and concepts.
