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
- [x] Switch to AST implementation
- [x] Find a way to do this with nested functions
- [ ] Create an example with a more complex physical calculation
- [ ] Add installation instructions
- [ ] Add example into README.md
- [ ] Add Github actions for automated formatting, testing, code coverage on deploy
- [ ] Add Github shields for
  - tests: passing
  - code coverage: 99%
  - license: MIT
  - Code style: black
  - pypi version
- [ ] Find minimum working version of dependancies
- [ ] Publish lib to PyPi
- [ ] Make a summary of all the situations in which this does not work
- [ ] Make a plan for next steps
- Nice-to-haves:
  - [ ] Caching of converted functions so that same functions are not converted multiple times
  - [ ] Template can be a string that is prepended or a function that is called on ExplainableResult object
  - [ ] Deal with `"` more elegantly in comments than having to define them as `\"`
  - [ ] Try following steps in https://github.com/typst/typst/issues/1158 to make typst compilation completely in memory
  - [ ] Have multiple subsequent lines be treated as one line (so that we can observe the character line limit)
  - [ ] It's not possible to create an explainable closure since the function will not have the local context
 
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