PKG = journal

github:
	-git commit -a
	git push origin main

new_core:
	pip uninstall backendcore
	pip install git+ssh://git@github.com/AthenaKouKou/BackEndCore.git

local_core:
	pip uninstall backendcore
	pip install git+file://$(MIX_HOME)/BackEndCore/

all_tests:
	cd journal_api; make tests
	cd manuscripts; make tests
	cd people; make tests
	cd text; make tests

prod: all_tests github

dev_env:
	pip3 install --upgrade pip
	pip3 install -r requirements-dev.txt
