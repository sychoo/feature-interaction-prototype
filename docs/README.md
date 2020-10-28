# docs/

## Directory Information
- support Python documentation generation

## Directory Hierarchies
```
├── README.md
├── source : include configuration files (conf.py, index.rst), and other .rst files (reStructuredText) generated
└── build : contains the built files
    ├── doctrees
    └── html : built HTML files
```

## Commands for Documentation Generation

### Step 1: set up the Sphinx framework
```bash
sphinx-quickstart
```
Note that after executing the command, the script will generate necessary configuration files and directory hierachy for the Sphinx framework

### Step 2: generate .rst files to facilitate html generation

```bash
# sphinx-apidoc -f -o <output-directory> <project-root-directory>

# please execute command below in the project root directory
sphinx-apidoc -f -o docs/source . 
```

### Step 3: generate the HTML file 
```bash
make html
```

## Python Style Guide
```python
class SampleClass:
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""
```