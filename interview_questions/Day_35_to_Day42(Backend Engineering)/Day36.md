1. What is REST?
A. REST is an architectural style for designing network APIs around resources, typically using standard HTTP methods, resource-oriented URLs, stateless requests, representations such as JSON, and meaningful HTTP status codes.

2. PUT vs PATCH?
A. PUT is generally used to replace a resource representation, whereas PATCH applies a partial modification to a resource.

3. POST vs PUT?
A. POST is commonly used to create a new resource and is generally non-idempotent, while PUT targets a known resource and is intended to be idempotent.




4. What Is Dependency Injection?
A. Dependency Injection is a design pattern in which a component declares the objects or resources it needs instead of creating them itself. In FastAPI, dependencies are declared with Depends(), and FastAPI resolves, executes, and injects their results into path operations.

5. Why Use DI?
A. Dependency Injection reduces code duplication and coupling, centralizes shared logic, improves testability, and is useful for resources such as database sessions, authentication, configuration, services, and external clients.

6. return vs yield Dependency
A. A dependency using return simply provides a value, while a dependency using yield supports resource lifecycle management: setup happens before the yielded resource is used, and cleanup code can execute afterward. This is commonly used for database sessions and similar resources.




                    HTTP REQUEST
                          ↓
                       FastAPI
                          ↓
                 Resolve Dependencies
                 /        |         \
                /         |          \
               ↓          ↓           ↓
          Database      Auth       Service
               \          |          /
                \         |         /
                 └────────┼────────┘
                          ↓
                       Endpoint
                          ↓
                    Business Logic
                          ↓
                     HTTP Response