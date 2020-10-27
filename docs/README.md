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

### Step 1: generate .rst files to facilitate html generation

```bash
# sphinx-apidoc -f -o <output-directory> <project-root-directory>

# please execute command below in the project root directory
sphinx-apidoc -f -o docs/source . 
```

### Step 2: generate the HTML file 
```bash
make html
```