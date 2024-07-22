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

tests:
	cd manuscripts; make tests
	cd people; make tests
	cd text; make tests
