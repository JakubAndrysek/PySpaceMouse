# Development guide

## Adding new features
1. Create a new branch from `master` with a descriptive name.
2. Implement your feature.
3. Create a pull request to `master` and assign a reviewer.
4. The reviewer will review your code and merge it into `master`.


## How to write documentation
To install the required dependencies, run `pip install pyspacemouse[develop]`.

Edit `README.md` only in the root folder. The documentation is automatically generated from `README.md` and `docs/` folder.
To update documentation from root to `/docs` use macro `make fixRelativeLinkDocs` which will replace all relative links from `/` to `/docs` folder.

### Building the documentation
The documentation is built using [mkdocs](https://www.mkdocs.org/). To test the documentation locally, run `make docs-serve` and open [http://localhost:8000](http://localhost:8000) in your browser.

### Deploying the documentation
The documentation is deployed automatically using GitHub Actions. Just push to the `master` branch and the documentation will be updated automatically.