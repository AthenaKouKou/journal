PKG = manuscripts
include ../common.mk
export TEST_DB = 1


export HEADER = "************************************************************"
export MSG = "Running tests for:"
export FOOTER = $(HEADER)

tests:
	@echo "\n$(HEADER)\n$(MSG) core\n$(FOOTER)\n"
	cd core; make tests
	@echo "\n$(HEADER)\n$(MSG) reports\n$(FOOTER)\n"
	cd reports; make tests
