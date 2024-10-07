# SmartChart-AI
## Style Guide
This project uses Python for the backend, React for the frontend, and MySQL for database operations.
### 1. General Best Practices
- Code Readability: Write clear, concise, and understandable code. Prefer clarity over cleverness.
- Consistency: Follow this guide across all parts of the project. Use consistent formatting, naming, and commenting conventions.
- Version Control: Use Git for version control, with clear and well-structured commit messages. 
- Documentation: Ensure that both code and the overall project are well-documented. Use markdown files (e.g., README.md) to describe how to install, configure, and run the project.
- Testing: Write unit tests for Python backend and React components. Strive for high test coverage using tools like pytest for Python and Jest for React.

### 2. Python Backend Style Guide
- Follow PEP 8 guidelines.
- Line length should not exceed 79 characters.
- Use 4 spaces per indentation level (no tabs).
- Functions and variable names should follow snake_case.
- Classes should follow CamelCase.
- Constants should be all UPPERCASE with underscores.

### 3. React Frontend Style Guide
- Use function components and React Hooks where possible.
- Use ESLint and Prettier to enforce code style.
- Use PascalCase for component file names and React components.
- Use CSS Modules or Styled Components for component-specific styling.
- Avoid global styles unless necessary. 

### 4. Database (MySQL)
- Follow these naming conventions:
  - Tables: plural, snake_case (users, orders)
  - Columns: snake_case (first_name, email_address)
  - Foreign keys: reference the parent table (user_id, order_id).
- Index columns that are frequently queried to improve performance.
