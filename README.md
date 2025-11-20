# YAML Preprocessor (YPP)

YAML Preprocessor (YPP) extends standard YAML with declarative constructs for parameters, modules, conditionals, iteration, branching, and modular composition.  
All extensions are expressed as valid YAML keys (prefixed with `@`), so documents remain valid YAML before preprocessing.

---

## Features

- **`@parameters`**: define constants and expressions  
- **`@modules`**: load decorated Python functions  
- **`@if / @elif / @else`**: conditional inclusion  
- **`@foreach`**: iterate over lists  
- **`@switch`**: branch by value  
- **`@import`**: modular composition with parameter inheritance/override  

---

## Syntax Reference

### `@parameters`
Define reusable values.

```yaml
@parameters:
  debug: true
  host: "localhost"
  port: 5432
```

---

### `@modules`
Expose decorated Python functions.

```yaml
@modules:
  - ./functions.py
```

---

### Conditionals: `@if / @elif / @else`

```yaml
server:
  @if: "{{ debug }}"
    url: "http://{{ host }}:5000"
  @elif: "{{ host == 'localhost' }}"
    url: "http://127.0.0.1:5000"
  @else:
    url: "https://{{ host }}"
```

---

### Iteration: `@foreach`

```yaml
@parameters:
  users: [alice, bob]

accounts:
  @foreach: "{{ users }}"
    - name: "{{ item }}"
      email: "{{ item }}@example.com"
```

---

### Switch: `@switch`

```yaml
@parameters:
  env: "prod"

server:
  @switch: "{{ env }}"
    case dev:
      url: "http://localhost:5000"
    case test:
      url: "http://test.example.com"
    case prod:
      url: "https://example.com"
    default:
      url: "https://fallback.example.com"
```

---

### Import: `@import`

```yaml
db:
  @import: "./partials/database.yaml"
```

- Imported file inherits parent parameters.  
- Local `@parameters` inside the imported file override parent values.  

**main.yaml**
```yaml
@parameters:
  host: "localhost"
  port: 5432

db:
  @import: "./partials/database.yaml"
```

**partials/database.yaml**
```yaml
@parameters:
  host: "127.0.0.1"

url: "postgres://{{ host }}:{{ port }}"
```

**Output**
```yaml
db:
  url: "postgres://127.0.0.1:5432"
```

---

## Expression Evaluation

- All expressions use Jinja2.  
- Parameters, environment variables (`env()`), and decorated functions are available.  
- Truthiness: empty string, `"false"`, `"0"`, `"None"`, empty list/dict → falsy; everything else → truthy.  

---

## Output

- After preprocessing, the document is plain YAML.  
- Only chosen branches and expanded loops remain.  
- Jinja2 expressions are resolved to concrete values.  
- `@parameters` and `@modules` blocks are removed from the final output.

---

## Example

```yaml
@modules:
  - ./functions.py

@parameters:
  env: "test"
  users: [alice, bob]

server:
  @switch: "{{ env }}"
    case dev:
      url: "http://localhost:5000"
    case test:
      url: "http://test.example.com"
    case prod:
      url: "https://example.com"

accounts:
  @foreach: "{{ users }}"
    - @import: "./partials/account.yaml"
```

**partials/account.yaml**
```yaml
name: "{{ item }}"
role: "user"
```

**Output**
```yaml
server:
  url: "http://test.example.com"

accounts:
  - name: "alice"
    role: "user"
  - name: "bob"
    role: "user"
```

---

### 🎯 Quick Summary
YPP makes YAML expressive and composable while staying valid YAML. Use `@parameters` for values, `@modules` for functions, `@if/@elif/@else` for conditionals, `@foreach` for loops, `@switch` for branching, and `@import` for modularity.

---

Would you like me to also prepare a **one‑page cheat sheet table** (construct → syntax → example) so developers can glance at it without scrolling through the README?