1. What Is a Multi-Agent System?
A. A multi-agent system is an AI architecture in which multiple specialized agents cooperate to solve a task. Each agent can have its own instructions, tools, context, state, and responsibilities, while coordination can be handled through patterns such as supervisors, routers, or handoffs.

2. Why Multiple Agents?
A. Multiple agents are useful when a problem contains distinct domains or responsibilities that benefit from specialized prompts, smaller tool sets, isolated context, separate permissions, or independent execution. The trade-off is additional coordination complexity, latency, and cost.

3. Supervisor vs Router
A. A router usually classifies a request and dispatches it to an appropriate specialist, while a supervisor can repeatedly delegate work to multiple agents, receive their outputs, and coordinate them until the overall task is complete.

                --- Mental Modal ---

                         USER
                          ↓
                     SUPERVISOR
                          ↓
                Decide who should work
                   /             \
                  /               \
            SPECIALIST A      SPECIALIST B
              Agent Loop        Agent Loop
              /     \             |
           Tool A  Tool B       Tool C
              \     /             |
               Result A        Result B
                   \             /
                    \           /
                     SUPERVISOR
                          ↓
                  Need more work?
                     /       \
                   YES        NO
                    ↓          ↓
                Delegate     FINAL
                            ANSWER