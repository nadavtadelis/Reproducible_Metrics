#Setting up enviroment
env : environment.yml
	conda env create -f environment.yml

#Running all notebooks
all :
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --to notebook --execute data_exploration
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --to notebook --execute model_fitting_2
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --to notebook --execute model_fitting_2
	jupyter nbconvert --ExecutePreprocessor.timeout=3600 --to notebook --execute main.ipynb

#Create a phony clean target to remove saved variables and figures
.PHONY : clean
clean:
	rm -f fig/*.png
	rm -f results/*.pickle

#Create second phony clean target to remove saved variables, figures, and environments
.PHONY : clean_all
clean_all:
	clean
	conda remove --name study_env --all