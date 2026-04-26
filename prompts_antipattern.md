# Microservice Anti-Pattern Detection Prompts (Copy & Paste)

> File di test: contiene 13(+1) prompt singoli, uno per anti-pattern.
> Ogni prompt è indipendente e copiabile/incollabile così com'è.
> Per NanoService e MegaService devi dare Repomix+LOC 

---

## NOTE DI SERVIZIO 
AP con definizione di MARS: NHC, TO, LL, No CI/CD 
AP con molte regole strutturate HE 
Alcuni AP presentano alcune regole di filtraggio ma poca roba 

---

## 1) WRONG CUTS (Input: REPOMIX) 
```text *Attento a non copiare i comandi per la formattazione* 

Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: WRONG CUTS
Definition: The system is decomposed into microservices following technical aspects, such as the presentation layer, business layer, and data access layer. Microservice should encapsulate functionalities fulfilling a single purpose.
Example: An e-commerce application that consists of several microservices. One of the microservices is responsible for handling product inventory management, and another microservice handles customer orders and payments. Now, imagine that during the initial design phase, the development team decides to divide the services based solely on the UI components of the application. They create separate microservices for the product listing page, product details page, shopping cart, and checkout process. Each microservice is developed and deployed independently.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 2) NANO-SERVICE  (Input: REPOMIX + LOC) 
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: NANO-SERVICE
Definition: The service is too fine-grained and only has a few operations. Its overhead (communications, maintenance, and so on) outweighs its utility. Nanoservices cause fragmented logic and performance issues due to communication overhead.
Example: Suppose we have a simple desk calculator with operations like add, subtract, multiply, and divide, where each operation is implemented as a separate microservice.
Exclude infrastructural services (e.g. Eureka, Config Server, Zipkin, Hystrix Dashboard) from MEGA-SERVICE and NANO-SERVICE detection unless they implement business logic. (Apply only if relevant to the chosen anti-pattern.)
Exclude non-production sample/demo/test/dummy services (e.g., hello-world, mock, sandbox) from MEGA-SERVICE and NANO-SERVICE detection unless they implement business logic or are explicitly deployed/used as part of the production system (e.g., referenced in deployment descriptors or invoked by other services).

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 3) SHARED LIBRARIES (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: SHARED LIBRARIES
Definition: Microservices should not share runtime libraries or source code that contain business logic or domain-specific functionality. Sharing such internal libraries breaks service boundaries and reduces independence, making microservices harder to evolve and deploy independently.
Example: Imagine a microservice system where multiple services depend heavily on a shared library that contains business logic and utility functions. Over time, this shared library grows in size and complexity as different services contribute to its codebase. These challenges emerge: there is a coupling between the shared library and services (library API changes force changes in multiple services); versioning issues when managing dependencies to ensure compatibility, increased complexity as the shared library grows, deployment coordination, performance bottlenecks, and finally, not all library functionality is needed by a service which results in draining its resources.
Example (naming traps: common/shared/core/domain): A repo may contain modules/folders named common/, shared/, core/, or even domain/ that are imported by multiple services. This alone is not evidence of the anti-pattern: if those modules only provide generic technical utilities (logging, HTTP clients, config, serialization, error handling, auth middleware) or just “anemic” DTOs without business rules, then it does not meet this definition. In practice, cases that match this anti-pattern typically show a shared module—regardless of its name (common, shared, core, domain)—that actually contains domain/business logic (entities with invariants/behavior, rules/policies, use-cases/process handlers) and is used by more than one service
Example (misleading “domain” naming vs real domain logic): A repo may include a package named core-domain/ (or domain/) that is used by multiple services, which can look like SHARED LIBRARIES. However, if core-domain only contains shared API contracts/schemas (e.g., OpenAPI types, protobuf-generated models, simple DTOs) and no business behavior (no rules/policies/use-cases, no entities with invariants), it does not match this anti-pattern. By contrast, a module named something innocuous like common/ can still trigger SHARED LIBRARIES if it contains real domain/business logic (e.g., pricing/discount/tax rules or order/customer lifecycle logic) and multiple services rely on it.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---
##### 4) HARDCODED ENDPOINT (Input: REPOMIX) [Variante Rule-based] 
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: HARDCODED ENDPOINT
Definition: Microservice IP addresses, ports, or full endpoint URLs are explicitly specified in source code, configuration files, or environment variables in a way that couples clients to a specific address/port. This reduces flexibility for scaling, load balancing, and environment changes, because endpoint changes require updating configuration or code in dependent services and redeploying them.
Service discovery prevents hardcoding IP addresses and port numbers. It tracks microservices endpoints and eases communication among 
microservices. Two strategies may be used for service discovery: client-side service discovery and server-side service discovery.

Example: Hardcoded endpoints occur when a service commits a concrete inter-service HTTP(S) destination (URL/host/IP/port) in runtime code or runtime config, instead of relying on service discovery (e.g., Consul/Eureka). Count only runtime communication between business/application microservices. Count cases like: 
(1) a literal URL/IP/port in code or config ("http://10.0.0.12:8080/api", ORDERS_URL=http://10.0.0.12:8080); 
(2) a hardcoded default/fallback (ORDERS_URL=${ORDERS_URL:http://10.0.0.12:8080}, env.get("ORDERS_URL","http://10.0.0.12:8080")); 
(3) host/port split and then composed at runtime (ORDERS_HOST=10.0.0.12 and ORDERS_PORT=8080 -> "http://" + ORDERS_HOST + ":" + ORDERS_PORT). Also count a committed full HTTP(S) URL (scheme + host + optional port) that targets another business microservice even if the host is a service name (e.g., http://orders-service:8080), because the client is still coupled to a specific URL/port configuration. 
Do not count placeholder-only references (${ORDERS_URL}) with no concrete value/default in the repo, endpoints that appear only in build/test tooling or API documentation (Swagger/OpenAPI host/servers), non-HTTP infrastructure endpoints (JDBC/DB URLs, Kafka/ZooKeeper/RabbitMQ), or platform/infrastructure dependencies such as API gateways (e.g., Zuul), Config Server, monitoring/tracing/logging systems, or the discovery/registry endpoints themselves (Eureka/Consul/registry).

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.
- If STATUS is PRESENT, you must explicitly name the evidence-backed Caller (component initiating the call) and Callee (endpoint target) in “SERVICES / COMPONENTS INVOLVED” as Caller -> Callee; 
- Do not analyze test artifacts, test drivers, load testing scripts, performance profiling code, or any files explicitly designed for testing purposes (e.g., files with "test", "load", "profile", "benchmark" in their name or declared purpose). Only analyze production microservice source code and deployment configuration.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: HARDCODED ENDPOINT
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services (caller/callee) or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout. 
```
---

## 4.1) HARDCODED ENDPOINT (Input: REPOMIX) [Variante semplice non inserita nelle tabelle ma abbiamo i risultati salvati] 
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: HARDCODED ENDPOINT
Definition: Microservice IP addresses, ports, or full endpoint URLs are explicitly specified in source code, configuration files, or environment variables for service-to-service business calls, coupling clients to a specific address/port. 
This reduces flexibility for scaling, load balancing, and environment changes because endpoint changes require updating configuration or code in dependent services and redeploying them.
Example - HARDCODED ENDPOINT (ANTI-PATTERN):

BAD: Hardcoded IP address in source code 
String url = "http://10.0.0.5:8080/api"; 

BAD: Hardcoded IP in config file 
SERVICE_URL=http://10.0.0.5:8080

Example - CORRECT (NOT anti-pattern):

GOOD: Logical service name resolved via service discovery
String url = "http://payment-service/api";
SERVICE_URL=http://payment-service/api

GOOD: Registry bootstrap URL (necessary for discovery, NOT service endpoint)
EUREKA_REGISTRY_URL=http://eureka:8761/eureka/

Key distinction: "payment-service" is a logical service name (not an IP/port). 
It's resolved dynamically at runtime by a service registry or DNS resolver (like Consul, Eureka, Kubernetes DNS), 
decoupling the client from infrastructure details.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.
- If STATUS is PRESENT, you must explicitly name the evidence-backed Caller (component initiating the call) and Callee (endpoint target) in “SERVICES / COMPONENTS INVOLVED” as Caller -> Callee; 
- Do not analyze test artifacts, test drivers, load testing scripts, performance profiling code, or any files explicitly designed for testing purposes (e.g., files with "test", "load", "profile", "benchmark" in their name or declared purpose). Only analyze production microservice source code and deployment configuration.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: HARDCODED ENDPOINT
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services (caller/callee) or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.  
```

---


---
 

## 6) MANUAL CONFIGURATION (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: MANUAL CONFIGURATION
Definition: Configuration of instances, services, and hosts is done manually. Microservices should separate the core codebase from the configuration management to enable automation.
Example: If we had 1000 Microservice instances deployed and had to manually update a port for the database, it would be difficult to update in production manually. Therefore a configuration file for each Microservice is not the best solution. Instead, a configuration server should be used, which automates the configuration process. A possible solution is to completely separate the configuration of an application from the actual code being deployed, build immutable application images that never change as these are promoted through environments, and finally inject any application configuration information at server startup through either environment variables or a centralized repository that the microservices read on startup.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 7) NO API GATEWAY (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: NO API GATEWAY
Definition: When a microservice-based system lacks an API gateway, the clients of the application necessarily have to invoke its microservices directly. By not having an API gateway, the system lacks a unified entry point that can provide centralized security, routing, protocol translation, and other cross-cutting functionalities. It becomes harder to enforce consistent policies across microservices and complicates the overall management and evolution of the system.
Example: A e-commerce application consists of Product Catalog, Order Management, and User Authentication microservices. Each microservice directly exposes its API to external clients without a centralized API gateway. Product Catalog has: • GET /products: Retrieves a list of products. • POST /products: Creates a new product. Order Management has: • GET /orders: Retrieves a list of orders. • POST /orders: Creates a new order. User Authentication has: • POST /login: Authenticates a user and returns a token. A client application wants to display a product catalog and allow users to add products to their shopping cart. Without an API gateway, the client application needs to make separate API calls to each microservice. The client application sends a request to the Product Catalog microservice to retrieve the list of products. When a user adds a product to their cart, the client application needs to send a request to the Order Management microservice to create a new order. If the user is not authenticated, the client application needs to send a request to the User Authentication microservice to authenticate the user. With this approach, the client application has to handle multiple API calls, manage authentication tokens separately, and deal with potential inconsistencies and complexities arising from direct communication with individual microservices. There is no centralized mechanism to handle cross-cutting concerns like authentication, request validation, logging, and rate limiting.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 8) MEGA-SERVICE (Input: REPOMIX + LOC)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: MEGA-SERVICE
Definition: Microservices should be small, independent, independently deployable units and serve a single purpose. A mega service has a high number of lines of code, modules, or files, as well as a high fan-in. Mega service could be a result of poor system decomposition when the microservice combines multiple functionalities that should be handled by multiple services. Having a mega microservice creates maintenance issues, reduced performance, and difficult testing, in addition to the complexity of the microservices infrastructure.
Example: An extreme example is a large monolithic service that tries to handle all functionality and business logic within a single codebase.
Exclude infrastructural services (e.g. Eureka, Config Server, Zipkin, Hystrix Dashboard ,thift) from MEGA-SERVICE and NANO-SERVICE detection unless they implement business logic. (Apply only if relevant to the chosen anti-pattern.)

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 9) SHARED PERSISTENCY (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: SHARED PERSISTENCY
Definition: Different microservices are accessing the same database/schema (often the same tables/entities). In the worst kind, different services use the same entities of a service. This approach couples the microservices connected to the same data and reduces the service independence. As a result, it introduces tight coupling requiring service coordination upon deployment, data inconsistency with concurrent updates, and performance bottlenecks limiting scalability and limited flexibility when modifying the data model.
Example: An e-commerce system composed of two microservices: ‘‘Order Service’’ responsible for managing customer orders and ‘‘Inventory Service’’ responsible for managing product inventory. Initially, both microservices have their separate databases, ensuring independent data management. However, as the system evolves, the development team decides to implement a new feature that requires real-time synchronization between the Order Service and Inventory Service. Specifically, they want to prevent customers from placing orders for products that are out of stock. To achieve this, the team decides to introduce a shared database table named ‘‘ProductStock’’ accessible by both microservices. Whenever an order is placed, the Order Service updates the stock quantity in the ProductStock table, and the Inventory Service reads from this table before approving an order.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 10) NO API VERSIONING (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: NO API VERSIONING
Definition: In a microservice architecture, if one or more services expose REST APIs to clients (internal or external) without any form of versioning (path-based, header-based, or query parameter), then the system suffers from the NO API VERSIONING anti-pattern. This prevents safe evolution of APIs and breaks backward compatibility when changes occur.
Example: A bank system has multiple dependent clients (branch offices). The bank system upgrades one of the services with more advanced functionality which changes the semantics of certain endpoints. However, clients were not informed of the change and their system fails upon the rollout. If the system kept the original endpoint as version 1 and rolled out version 2 of the same service, the new clients could utilize new advancements while others would not experience disruptions.
`GET /orders` instead of `GET /v1/orders`, with no alternative versioning strategy.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 11) NO HEALTH CHECK (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: No Health Check (NHC)
Definition: This antipattern describes microservices that are not periodically health-checked. Unavailable microservices may not be noticed, leading to timeouts and other errors.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

---

## 12) INSUFFICIENT MONITORING (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: INSUFFICIENT MONITORING
Definition: Performance and failure of the microservices are not tracked. Failures become more difficult to catch and tracking performance issues become more tedious. A solution is to adopt a global monitoring tool.
Example: An e-commerce application consists of multiple microservices, including a product catalog service, a shopping cart service, and a payment service. The services communicate with each other to fulfill customer orders. In this case, the development team has implemented the microservices architecture without giving much thought to monitoring and observability. They rely on simple logging statements within each service but lack a centralized monitoring system. As a result, they encounter several issues: lack of service health insights, difficulty in identifying root causes, inability to scale effectively, and reactive approach to issue resolution.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```
## 13) TIMEOUT (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: Timeouts (TO)
Definition: This antipattern happens when timeout values are set and hard-coded in HTTP requests, which leads to unnecessary disconnections or delays.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

## 14) MULTIPLE SERVICE INSTANCES PER HOST (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: MULTIPLE SERVICE INSTANCES PER HOST
Definition: A single host contains multiple microservices instances deployed to the same host.
The hints of the presence of this anti-pattern could be: (1) a single deployment platform; (2) a single version control repository; or (3) a global deployment script.
Microservices have to share the same resources that are available inside the host.
Moreover, scaling up or down a given host involves scaling all the instances that are inside this host.
Finally, possible technology-related conflicts may happen between the microservices instances that share the same host.
Example: An e-commerce application that consists of three microservices: Order Management, Inventory Management, and Payment Processing. Initially, the development team decides to deploy each microservice on separate hosts to ensure isolation and scalability. However, as the application grows, they start facing increased traffic and performance challenges. To address these challenges, the team decides to deploy multiple instances of each microservice on a single host. For instance, they run two instances of Order Management, three instances of Inventory Management, and four instances of Payment Processing on a single physical machine. This approach appears to utilize the available resources more efficiently, as multiple services can share the same hardware. However, over time, the following issues are found: - Resource contention, as all instances experience a spike in traffic simultaneously and they will compete for CPU, memory, etc. - Lack of isolation and fault tolerance. - Monitoring and troubleshooting becomes challenging to isolate and diagnose issues.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: MULTIPLE SERVICE INSTANCES PER HOST
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

## 15) LOCAL LOGGING (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: Local Logging (LL)
Definition: This antipattern results from microservices having their own logging mechanism, which prevents aggregation and analyses of their logs and the monitoring and recovery of systems.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```

## 16) No CI/CD (No Continuous Integration / Continuous Delivery) (Input: REPOMIX)
```text
Act as an expert microservice architecture analyst and reverse-engineering researcher tasked with detecting a specific Architectural Anti-Pattern in a provided software repository or codebase.

You will receive one or more input files describing a software system. Treat these inputs as the sole source of truth; do not assume the presence of any missing files or behaviors. Never respond with UNKNOWN.

Your task is to analyze the entire provided artifacts and determine whether the specified microservice architectural anti-pattern is PRESENT or ABSENT, strictly according to the exact definition and example given below.

ANTI-PATTERN
Name: No Continuous Integration (CI) / Continuous Delivery (CD) (NCI)
Definition: Continuous integration and delivery are important for microservices to automate repetitive steps during testing and deployment. Not using CI/CD undermines the microservice architectural style, which encourages automation wherever possible.

Detection Constraints:
- Follow only the provided definition and example without generalization or extension.
- Translate the definition into observable indicators only if explicitly implied.
- Cross-reference all provided inputs including services, modules, endpoints, dependencies, shared resources, and deployment descriptors.
- If any required information is missing, ambiguous, or unverifiable from the artifacts, output ABSENT and specify exactly what is missing.
- The anti-pattern name in your output must exactly match the provided Name.

Reasoning Instructions:
- Think carefully and exhaustively, based solely on the provided definition and example.
- Do not reveal your internal reasoning steps or intermediate thoughts.

Output Format (ONLY these sections, in this order, with no additional content):

ANTI-PATTERN: [Exact Name]
STATUS: PRESENT | ABSENT

SUMMARY (1–2 lines):
- PRESENT: Briefly describe what the anti-pattern is and where it manifests.
- ABSENT: Briefly explain why the analyzed artifacts do not meet the definition or example.

RATIONALE (max 4 bullets):
- PRESENT: Reasons why observed features match the definition/example; key indicators.
- ABSENT: Which required conditions are not met or unverifiable from the artifacts.

SUPPORTING INDICATORS (only if PRESENT):
- Provide 1 to 4 concrete observations anchored to specific artifacts (including filename and line number if available).
- Additional relevant observations as necessary.

SERVICES / COMPONENTS INVOLVED:
- PRESENT: Explicitly list affected services or components identifiable from the artifacts.
- ABSENT: None identified.

Ensure clarity, precision, and strict adherence to the instructions throughout.
```