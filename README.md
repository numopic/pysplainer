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
- [x] Make an example with a matrix
- [ ] Create an example with some physical function ()
- [ ] Find a way to do this with nested functions
- [ ] Caching of converted functions so that same functions are not converted multiple times
- [ ] Template can be a string that is prepended or a function that is called on ExplainableResult object
- [ ] Deal with `"` more elegantly in comments than having to define them as `\"`
- [ ] Switch to a more robust implementation
  - [ ] ~~AST implementation might not be usable since AST ignores comments, and we rely on it~~
  - [ ] `tokenize` python library might be used instead
- [ ] Add installation instructions
- [ ] Add example into README.md
- [ ] Publish lib to PyPi
- [ ] ~~Implement ExplainableResult.as_dict()~~
- [ ] ~~Implement ExplainableResult.as_markdown()~~
- [ ] Make a summary of all the situations in which this does not work
- [ ] Try following steps in https://github.com/typst/typst/issues/1158 to make typst compilation completely in memory
- [ ] Make a plan for next steps
 
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