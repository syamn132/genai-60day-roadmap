Part_1

Q: What is the difference between print() and logging?

Logging supports configurable severity levels, formatting, handlers and output destinations. It is better suited for diagnosing application behavior consistently.

Q: Why use middleware for request logging?

Middleware allows cross-cutting concerns, such as request timing and HTTP status logging, to be implemented centrally rather than repeated in every endpoint.

Q: Why do we use logger.exception()?

It captures an error message with the current exception traceback, helping identify the source of a failure.

Q: Why use log rotation?

Without rotation or external retention controls, local log files can grow indefinitely and consume disk space.

Q: What should never be written into application logs?

Passwords, access tokens, secret keys, sensitive personal data and other credentials. Operational logs should contain only the information necessary to diagnose the system.



Part_2

What is application monitoring?
Monitoring is the process of collecting and analyzing operational measurements such as traffic, latency, failure rates and resource utilization to understand application health.

What is the difference between Counter and Gauge?
A Counter increases as events happen, while a Gauge represents a value that can move up and down, such as active tasks.

What is a Histogram?
A Histogram groups observations into configured buckets, allowing analysis of latency distributions rather than relying only on an average.

What is the difference between logs and metrics?
Logs describe individual events. Metrics represent numerical measurements suitable for aggregation and time-series analysis.

Why does monitoring matter for GenAI applications?
GenAI requests can be expensive and unpredictable. Monitoring helps engineers understand LLM latency, retrieval performance, request failures, traffic changes, and service capacity.



Q1. What is the difference between handled and unhandled exceptions?

Handled exceptions represent conditions the application anticipates, such as missing resources or invalid inputs. Unhandled exceptions represent unexpected failures, such as bugs or unforeseen dependency errors.

Q2. Why should we create custom exception handlers in FastAPI?

They help standardize error responses, preserve meaningful status codes, keep sensitive implementation details private, and integrate error reporting with logging.

Q3. Why do we need request IDs?

Request IDs allow engineers to correlate API responses with application logs and debugging information.

Q4. Should we return Python tracebacks in production responses?

No. Detailed tracebacks belong in protected application logs. Public responses should provide safe error messages and correlation identifiers.

Q5. How are logging, monitoring and error handling connected?

Logging records detailed events, monitoring measures operational behavior, and error handling controls how applications respond to failures.


Important HTTP status codes
Code	Meaning	Example
200	Success	- Product retrieved
400	Bad Request	- Division by zero in our demo
401	Unauthorized -	Missing or invalid authentication
403	Forbidden -	Insufficient permission
404	Not Found -	Product does not exist
409	Conflict -	Resource already exists
422	Validation Error -	Invalid parameter type
429	Too Many Requests -	API rate limit exceeded
500	Internal Server Error -	 Unexpected application failure
503	Service Unavailable -	Critical dependency unavailable