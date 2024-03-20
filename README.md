# pysplainer
Explainable Python code

## Instalation

## Example

## TODO

- [x] Implement trace function
- [x] Add the @explainable decorator to function
- [x] Add an example that outputs lines in typst format
- [x] Implement ExplainableResult.as_pdf()
- [x] Add support for typst templates to generate a pretty pdf
- [ ] Create an example with some physical function ()
- [ ] Find a way to do this with nested functions
- [ ] Switch to AST implementation
  - [ ] AST implementation might not be usable since AST ignores comments, and we rely on it
  - [ ] `tokenize` python library might be used instead
- [ ] Add installation instructions
- [ ] Add example into README.md
- [ ] Implement ExplainableResult.as_dict()
- [ ] Implement ExplainableResult.as_markdown()
- [ ] Make a summary of all the situations that this does not work
- [ ] Make a plan for next steps
- [ ] Try following steps in https://github.com/typst/typst/issues/1158 to make typst compilation completely in memory
 
## Similar libraries

We can find libraries under the term _literate programming_ that serve a similar (but not exactly the same) purpose. 

- https://en.wikipedia.org/wiki/Literate_programming

In Python, literate programming libraries might be

- Jupyter notebooks
- PyLit
- PyReport (discontinued)

Similar concept is document generation:
- https://en.wikipedia.org/wiki/Documentation_generator
- https://homes.cs.washington.edu/~mernst/pubs/test-documentation-ase2011.pdf