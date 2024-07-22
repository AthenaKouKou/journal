# common make vars and targets:
export PROJ_DIR = $(KOUKOU_HOME)
export REQ_DIR = $(PROJ_DIR)
export AQL_DIR = $(PROJ_DIR)/aql
export BIBLIOGRAPHY_DIR = $(PROJ_DIR)/bibliography
export CONV_DIR = $(REPORT_DIR)/converters
export CSS_DIR = $(PROJ_DIR)/static/css
export DATA_DIR = $(PROJ_DIR)/data
export DOCS_DIR = $(PROJ_DIR)/docs
export DSRC_DIR = $(PROJ_DIR)/datasource
export EMAILER_DIR = $(PROJ_DIR)/emailer
export ETL_DIR = $(PROJ_DIR)/ETL
export EXCEP_DIR = $(PROJ_DIR)/exceptions
export GLOSS_DIR = $(PROJ_DIR)/glossary
export HMDA_DIR = $(PROJ_DIR)/hmda
export JOURNAL_DIR = $(PROJ_DIR)/journal
export LIB_DIR = $(PROJ_DIR)/common
export MD_DIR = $(PROJ_DIR)/md
export REPORT_DIR = $(PROJ_DIR)/report
export SERVER_DIR = $(PROJ_DIR)/api_server
export SFA_DIR = $(PROJ_DIR)/sfa
export SUBSCRIPTION_DIR = $(PROJ_DIR)/subscription
export SECURITY_DIR = $(PROJ_DIR)/security
export TEMPLATE_DIR = $(PROJ_DIR)/templates
export USER_DATA_DIR = $(PROJ_DIR)/user_data

export PANDOC = pandoc
export HEROKU_APP = kou-kou-api
export PYLINT = flake8
export PYLINTFLAGS = --exclude=__main__.py

# make sure we test against local DB:
export LOCAL_MONGO=1

PYTHONFILES = $(shell ls *.py)
PYTESTFLAGS = -vv --verbose --cov-branch --cov-report term-missing --tb=short -W ignore::FutureWarning

MAIL_METHOD = api

FORCE:

tests: lint pytests

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	$(PYLINT) $(PYLINTFLAGS) $*.py

pytests: FORCE
	echo $(USER_DB_FILE)
	export TEST_DB=1; pytest $(PYTESTFLAGS) --cov=$(PKG)

# test a python file:
%.py: FORCE
	$(PYLINT) $(PYLINTFLAGS) $@
	export TEST_DB=1; pytest $(PYTESTFLAGS) tests/test_$*.py

nocrud:
	-rm *~
	-rm *.log
	-rm *.out
	-rm .*swp
	-rm $(TESTDIR)/*~
