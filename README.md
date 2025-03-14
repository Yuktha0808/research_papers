# research_papers
#STEP 1
#Install Poetry (for dependency management)
-->  pip install poetry

#Verify installation:
--> poetry --version




#STEP 2
#Initialize a Poetry Project
--> poetry init

#Add required dependencies
-->poetry add requests



#STEP 3
#write the code



#STEP 4
#Update pyproject.toml
#Open pyproject.toml and add this at the bottom
--> [tool.poetry.scripts]
--> get-papers-list = "cli:main"




#STEP 5
#Run the Program
#1 Install Dependencies
--> poetry install

#2 Run the CLI Tool
--> poetry run get-papers-list "cancer research"

#3 Save Results to CSV
--> poetry run get-papers-list "diabetes treatment" -f results.csv
