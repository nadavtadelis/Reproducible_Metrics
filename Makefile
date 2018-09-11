# Makefile
# Thanks to Jason Hiebel for the useful guide to compiling LaTex docs: https://github.com/JasonHiebel/latex.makefile

# Targets:
#    default   : compiles the document to a PDF file using the defined
#                latex generating engine. (pdflatex, xelatex, etc)
#    display   : displays the compiled document in a common PDF viewer.
#                (currently linux = evince, OSX = open)
#    clean     : removes all figures in the fig/ directory
#                removes intermediate data from results/ directory
#                removes the intermediate/ directory holding temporary files
#                removes all .pdf's
#    clean_all : same as clean, but also removes the environment


# Setting up enviroment
env : environment.yml
	conda env create -f environment.yml


# Running all notebooks
all :
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --inplace --execute data_exploration
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --inplace --execute model_fitting_1
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --inplace --execute model_fitting_2
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --inplace --execute function_testing
	make default


# Remove saved data, models, and figures
# Also removes all LaTex outputs
.PHONY : clean
clean:
	rm -f figures/*.png
	rm -f figures/*.eps
	rm -f results/*.pickle
	rm -f results/*.pkl
	rm -f data/*.pkl
	rm -rf tex_stuff/intermediate/
	rm -rf __pycache__/*
	rm -rf *.nbconvert.ipynb
	rm -f *.pdf


# Same as clean phony, but also removes the environment
.PHONY : clean_all
clean_all:
	make clean
	conda remove --name study_env --all


### LaTex Compiling
# PROJECT is subdirectory/tex_file_name
# PROJECT2 is only the tex_file_name
PROJECT = tex_stuff/reproducible_metrics
PROJECT2 = reproducible_metrics

.PHONY: default1
default1: tex_stuff/intermediate/$(PROJECT).pdf


.PHONY : default
default:
	make default1
	cp tex_stuff/intermediate/$(PROJECT2).pdf ./
	rm -f tex_stuff/intermediate/$(PROJECT2).pdf


display: default
	(${PDFVIEWER} $(PROJECT2).pdf &)


### Compilation Flags
PDFLATEX_FLAGS  = -halt-on-error -output-directory tex_stuff/intermediate/

TEXINPUTS = .:tex_stuff/intermediate/
TEXMFOUTPUT = tex_stuff/intermediate/


### File Types (for dependancies)
TEX_FILES = $(shell find . -name '*.tex' -or -name '*.sty' -or -name '*.cls')
BIB_FILES = $(shell find . -name '*.bib')
BST_FILES = $(shell find . -name '*.bst')
IMG_FILES = $(shell find . -path '*.jpg' -or -path '*.png' -or \( \! -path './tex_stuff/intermediate/*.pdf' -path '*.pdf' \) )


### Standard PDF Viewers
# Defines a set of standard PDF viewer tools to use when displaying the result
# with the display target. Currently chosen are defaults which should work on
# most linux systems with GNOME installed and on all OSX systems.

UNAME := $(shell uname)

ifeq ($(UNAME), Linux)
PDFVIEWER = evince
endif

ifeq ($(UNAME), Darwin)
PDFVIEWER = open
endif
	

### Core Latex Generation
# Performs the typical build process for latex generations so that all
# references are resolved correctly. If adding components to this run-time
# always take caution and implement the worst case set of commands.
# Example: latex, bibtex, latex, latex
#
# Note the use of order-only prerequisites (prerequisites following the |).
# Order-only prerequisites do not effect the target -- if the order-only
# prerequisite has changed and none of the normal prerequisites have changed
# then this target IS NOT run.
#
# In order to function for projects which use a subset of the provided features
# it is important to verify that optional dependancies exist before calling a
# target; for instance, see how bibliography files (.bbl) are handled as a
# dependency.

tex_stuff/intermediate/:
	mkdir -p tex_stuff/intermediate/

tex_stuff/intermediate/$(PROJECT).aux: $(TEX_FILES) $(IMG_FILES) | tex_stuff/intermediate/
	xelatex $(PDFLATEX_FLAGS) $(PROJECT)

tex_stuff/intermediate/$(PROJECT).bbl: $(BIB_FILES) | tex_stuff/intermediate/$(PROJECT2).aux
	bibtex tex_stuff/intermediate/$(PROJECT2)
	xelatex $(PDFLATEX_FLAGS) $(PROJECT)
	
tex_stuff/intermediate/$(PROJECT).pdf: tex_stuff/intermediate/$(PROJECT).aux $(if $(BIB_FILES), tex_stuff/intermediate/$(PROJECT).bbl)
	xelatex $(PDFLATEX_FLAGS) $(PROJECT)