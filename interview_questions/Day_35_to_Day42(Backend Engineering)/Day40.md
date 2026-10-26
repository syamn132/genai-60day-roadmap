Q: Why use Redis if PostgreSQL already exists?

Redis is often used as a fast-access cache to reduce repeated database reads and improve response latency. PostgreSQL remains the primary persistent database in our architecture.

Q: What is a cache hit versus a cache miss?

A cache hit means the requested value was found in Redis. A cache miss means the application must obtain it from another source, often PostgreSQL.

Q: What is TTL?

TTL is the remaining time before a cached entry expires. It helps limit how long temporary or potentially stale data remains available.

Q: What is cache invalidation?

Cache invalidation removes or refreshes outdated cached data after the underlying data changes.