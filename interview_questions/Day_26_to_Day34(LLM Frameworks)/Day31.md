1. What is MCP?
A. Model Context Protocol is an open standard for connecting AI applications to external tools, data, and reusable prompts through a standardized client-server interface. MCP servers expose capabilities such as tools, resources, and prompts, while MCP clients discover and use those capabilities independently of a specific model provider.

2. Why MCP?
A. Without MCP, AI applications often need custom integrations for every external service. MCP standardizes discovery and invocation of external capabilities, making integrations more reusable and model-neutral.

3. MCP Tool vs Resource
A. A tool represents an operation the model or application can invoke, such as querying a database or performing an action. A resource represents data that the application can read and place into model context.